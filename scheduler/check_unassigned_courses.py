# scheduler/check_unassigned_courses.py

import pandas as pd

# Load both files
new_data = pd.read_csv("data/CSV/new_data.csv")
class_cap = pd.read_excel("data/Input/2025ClassEnrollCap.xlsx")

# Prepare 'CourseID' and 'Sec' in class_cap
class_cap.columns = class_cap.columns.str.strip()
class_cap["CourseID"] = "COMP " + class_cap["Course Num"].astype(str)
class_cap["Sec"] = class_cap["Sec #"].astype(str)

# Prepare 'CourseID' and 'Sec' in new_data
new_data["CourseID"] = new_data["CourseID"].str.strip()
new_data["Sec"] = new_data["Sec"].astype(str)

# Build (CourseID, Sec) sets
assigned_courses = set(zip(new_data["CourseID"], new_data["Sec"]))
all_courses = set(zip(class_cap["CourseID"], class_cap["Sec"]))

# Find unassigned courses
unassigned_courses = all_courses - assigned_courses

# Output
if unassigned_courses:
    print(f"\n❗ Found {len(unassigned_courses)} unassigned course(s):")
    for course_id, sec in sorted(unassigned_courses):
        print(f"{course_id} - {sec}")
else:
    print("\n✅ All courses have been successfully assigned!")

# Save missing to CSV
unassigned_df = pd.DataFrame(list(unassigned_courses), columns=["CourseID", "Sec"])
unassigned_df = unassigned_df.sort_values(by=["CourseID", "Sec"]).reset_index(drop=True)
unassigned_df.to_csv("data/Output/unassigned_courses.csv", index=False)
print("\n✅ Saved missing courses list to: data/Output/unassigned_courses.csv")
