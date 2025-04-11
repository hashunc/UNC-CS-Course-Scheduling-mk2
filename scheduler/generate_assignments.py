# generate_assignments.py

import pandas as pd
from collections import defaultdict

# Load files
course_cap_df = pd.read_excel("data/Input/2025ClassEnrollCap.xlsx")
availability_df = pd.read_excel("data/Input/Temple of Automatic course scheduling data sheet (Responses) - Form Responses 1.xlsx")
top_courses_df = pd.read_csv("data/CSV/top_courses_per_instructor_clean.csv")

# Clean columns
availability_df.columns = availability_df.columns.str.strip()
availability_df["Last name"] = availability_df["Last name"].str.strip()

# Build instructor -> number of courses mapping
instructor_course_counts = dict(zip(
    availability_df["Last name"],
    pd.to_numeric(availability_df["How many classes you will teach in the next semester."], errors="coerce").fillna(0).astype(int)
))

# Extract all available sections
course_cap_df["Course"] = "COMP " + course_cap_df["Course Num"].astype(str) + " - " + course_cap_df["Sec #"].astype(str)
all_courses = course_cap_df["Course"].tolist()

# Map course number -> sections, treat COMP 590/790-187 as one unified course
course_sections = defaultdict(list)
for course in all_courses:
    course_parts = course.split(" - ")
    course_prefix = course_parts[0].strip()
    section = course_parts[1].strip()
    if section == "187" and course_prefix in ["COMP 590", "COMP 790"]:
        key = "COMP 590/790-187"
    else:
        key = course_prefix
    course_sections[key].append(course)

# Extract course numbers from top course names and sort by preference score
top_courses_df["Course Num"] = top_courses_df["Course"].str.extract(r"(COMP \d+)")
top_courses_df.loc[top_courses_df["Course"].str.contains("590.*790.*187|790.*590.*187", regex=True), "Course Num"] = "COMP 590/790-187"
top_courses_sorted = top_courses_df.sort_values(by=["Instructor", "Total"], ascending=[True, False])

# Assign sections based on instructor preferences
assignments = []
used_courses = set()

for instructor_last_name, count in instructor_course_counts.items():
    preferred_course_nums = top_courses_sorted[top_courses_sorted["Instructor"] == instructor_last_name]["Course Num"].tolist()
    assigned = 0
    for course_num in preferred_course_nums:
        for section in course_sections.get(course_num, []):
            if section not in used_courses:
                assignments.append({"Instructor": instructor_last_name, "CourseID": course_num, "Sec": section.split(" - ")[1]})
                used_courses.add(section)
                assigned += 1
                if assigned == count:
                    break
        if assigned == count:
            break

# Final result DataFrame, sorted by course number
assignments_df = pd.DataFrame(assignments)
assignments_df["Course Num"] = assignments_df["CourseID"].str.extract(r"COMP (\d+)").fillna(0).astype(int)
assignments_sorted = assignments_df.sort_values(by="Course Num").drop(columns=["Course Num"]).reset_index(drop=True)

# Save to CSV
assignments_sorted.to_csv("data/CSV/new_data.csv", index=False)
print("Saved to data/CSV/new_data.csv")
