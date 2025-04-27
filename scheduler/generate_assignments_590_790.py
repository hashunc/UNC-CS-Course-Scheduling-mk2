import pandas as pd
from collections import defaultdict
from config import (
    INPUT_COURSE_CAP,
    INPUT_AVAILABILITY,
    OUTPUT_TOP_COURSES,
    OUTPUT_NEW_DATA_590_790,
    OUTPUT_MERGED_590_790,
    OUTPUT_FACULTY_PREF
)

# Load files
course_cap_df = pd.read_excel(INPUT_COURSE_CAP)
availability_df = pd.read_excel(INPUT_AVAILABILITY)
top_courses_df = pd.read_csv(OUTPUT_TOP_COURSES)

# Clean columns
availability_df.columns = availability_df.columns.str.strip()
availability_df["Last name"] = availability_df["Last name"].str.strip()
course_cap_df.columns = course_cap_df.columns.str.strip()
top_courses_df["Instructor"] = top_courses_df["Instructor"].str.strip()
top_courses_df["Course"] = top_courses_df["Course"].str.strip()

# Build instructor -> number of courses mapping
instructor_course_counts = dict(zip(
    availability_df["Last name"],
    pd.to_numeric(availability_df["How many classes you will teach in the next semester."], errors="coerce").fillna(0).astype(int)
))

# Construct all available section keys
course_cap_df["Course"] = "COMP " + course_cap_df["Course Num"].astype(str)
course_cap_df["Section"] = course_cap_df["Sec #"].astype(str)
course_cap_df["Full"] = course_cap_df["Course"] + "-" + course_cap_df["Section"]

# Map: course_key -> sections
course_sections = defaultdict(list)
for _, row in course_cap_df.iterrows():
    full = row["Full"]
    base = row["Course"]
    sec = row["Section"]

    if base in ["COMP 590", "COMP 790"]:
        key = full
    elif sec == "187" and base in ["COMP 590", "COMP 790"]:
        key = "COMP 590/790-187"
    elif base == "COMP 590&790":
        key = base + "-" + sec
    else:
        continue  # Skip non-590/790

    course_sections[key].append(full)

# Extract course numbers for 590/790
top_courses_df["Course Num"] = top_courses_df["Course"].str.extract(r"(COMP \d+(?:/790)?(?:&790)?(?:-\d+)?)")
top_courses_df.loc[top_courses_df["Course"].str.contains("590.*790.*187|790.*590.*187|590&790", regex=True), "Course Num"] = "COMP 590&790"
top_courses_sorted = top_courses_df.sort_values(by=["Instructor", "Total"], ascending=[True, False])

# Assign sections only for COMP 590 and 790
assignments = []
used_courses = set()

for instructor_last_name, count in instructor_course_counts.items():
    preferred_course_nums = top_courses_sorted[top_courses_sorted["Instructor"] == instructor_last_name]["Course Num"].dropna().tolist()
    assigned = 0
    for course_num in preferred_course_nums:
        if not ("590" in course_num or "790" in course_num):
            continue
        for section in course_sections.get(course_num, []):
            if section not in used_courses:
                cap_row = course_cap_df[course_cap_df["Full"] == section]
                capacity = int(cap_row["Enroll Cap"].values[0]) if not cap_row.empty else None

                if "-" in section:
                    base_course, sec = section.split("-")
                else:
                    base_course, sec = section, ""

                assignments.append({
                    "CourseID": base_course.strip(),
                    "Sec": sec.strip(),
                    "EnrollCapacity": capacity,
                    "ProfessorName": instructor_last_name
                })
                used_courses.add(section)
                assigned += 1
                if assigned == count:
                    break
        if assigned == count:
            break

# Final result
assignments_df = pd.DataFrame(assignments)
assignments_sorted = assignments_df.reset_index(drop=True)
assignments_sorted.to_csv(OUTPUT_NEW_DATA_590_790, index=False)
print(f"✅ Saved 590/790 assignments to {OUTPUT_NEW_DATA_590_790}")

# Merge time slots
faculty_pref_df = pd.read_csv(OUTPUT_FACULTY_PREF)
new_data_df = pd.read_csv(OUTPUT_NEW_DATA_590_790)

merged_df = new_data_df.merge(
    faculty_pref_df[["Last Name", "Available Time Slots"]],
    left_on="ProfessorName",
    right_on="Last Name",
    how="left"
)
merged_df = merged_df.drop(columns=["Last Name"])
merged_df.rename(columns={"Available Time Slots": "Professor_PreferredTimeSlots"}, inplace=True)
merged_df = merged_df[["CourseID", "Sec", "EnrollCapacity", "ProfessorName", "Professor_PreferredTimeSlots"]]
merged_df.to_csv(OUTPUT_MERGED_590_790, index=False)
print(f"✅ Saved merged 590/790 assignment with time slots: {OUTPUT_MERGED_590_790}")
