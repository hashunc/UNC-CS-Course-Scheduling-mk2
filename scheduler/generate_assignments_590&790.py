# 590&790.py

import pandas as pd

# Load files
course_cap_df = pd.read_excel("data/Input/2025ClassEnrollCap.xlsx")
top_courses_df = pd.read_csv("data/CSV/top_courses_per_instructor_clean.csv")
availability_df = pd.read_excel("data/Input/Temple of Automatic course scheduling data sheet (Responses) - Form Responses 1.xlsx")

# Clean columns
course_cap_df.columns = course_cap_df.columns.str.strip()
top_courses_df["Instructor"] = top_courses_df["Instructor"].str.strip()
top_courses_df["Course"] = top_courses_df["Course"].str.strip()
availability_df.columns = availability_df.columns.str.strip()
availability_df["Last name"] = availability_df["Last name"].str.strip()

# Build instructor -> number of courses mapping
instructor_course_counts = dict(zip(
    availability_df["Last name"],
    pd.to_numeric(availability_df["How many classes you will teach in the next semester."], errors="coerce").fillna(0).astype(int)
))

# Filter only COMP 590&790 related entries from top_courses_df
top_courses_df = top_courses_df[top_courses_df["Course"].str.contains("590&790")]

# Extract section numbers from course names
top_courses_df["CourseID"] = "COMP 590&790"
top_courses_df["Sec"] = top_courses_df["Course"].str.extract(r"-(\d+)")

# Prepare course capacity mapping
course_cap_df["Course"] = "COMP " + course_cap_df["Course Num"].astype(str)
course_cap_df["Full"] = course_cap_df["Course"] + "-" + course_cap_df["Sec #"].astype(str)
cap_mapping = dict(zip(course_cap_df["Full"], course_cap_df["Enroll Cap"]))

# Assign
assignments = []
used_courses = set()

for instructor, group in top_courses_df.groupby("Instructor"):
    count = instructor_course_counts.get(instructor, 0)
    assigned = 0
    for _, row in group.iterrows():
        full_course = f"COMP 590&790-{row['Sec']}"
        if full_course not in cap_mapping or full_course in used_courses:
            continue
        assignments.append({
            "CourseID": row["CourseID"],
            "Sec": row["Sec"],
            "EnrollCapacity": cap_mapping[full_course],
            "ProfessorName": instructor
        })
        used_courses.add(full_course)
        assigned += 1
        if assigned == count:
            break

# Save to CSV
assignments_df = pd.DataFrame(assignments)
assignments_df.to_csv("data/CSV/new_data_590&790_only.csv", index=False)
print("✅ Saved new_data_590&790_only.csv")

# Merge with faculty time preferences
faculty_pref_df = pd.read_csv("data/CSV/faculty_time_preferences.csv")
merged_df = assignments_df.merge(
    faculty_pref_df[["Last Name", "Available Time Slots"]],
    left_on="ProfessorName",
    right_on="Last Name",
    how="left"
)
merged_df = merged_df.drop(columns=["Last Name"])
merged_df.rename(columns={"Available Time Slots": "Professor_PreferredTimeSlots"}, inplace=True)
merged_df = merged_df[["CourseID", "Sec", "EnrollCapacity", "ProfessorName", "Professor_PreferredTimeSlots"]]
merged_df.to_csv("data/CSV/merged_assignments_590&790_only.csv", index=False)
print("✅ Saved merged_assignments_590&790_only.csv")
