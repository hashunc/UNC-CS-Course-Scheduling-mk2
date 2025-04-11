# clean_top_courses.py

import pandas as pd

# Load original top courses file
top_courses_df = pd.read_csv("data/CSV/top_courses_per_instructor.csv")

# Load instructor availability (includes class counts)
availability_df = pd.read_excel("data/Input/Temple of Automatic course scheduling data sheet (Responses) - Form Responses 1.xlsx")
availability_df.columns = availability_df.columns.str.strip()
availability_df["Last name"] = availability_df["Last name"].str.strip()

# Extract instructors who are teaching at least 1 course
available_instructors = availability_df[
    pd.to_numeric(availability_df["How many classes you will teach in the next semester."], errors="coerce") > 0
]["Last name"].tolist()

# Filter top_courses based on instructor presence
top_courses_clean = top_courses_df[top_courses_df["Instructor"].isin(available_instructors)].reset_index(drop=True)

# Save to CSV
top_courses_clean.to_csv("data/CSV/top_courses_per_instructor_clean.csv", index=False)
print("Saved cleaned top courses to data/CSV/top_courses_per_instructor_clean.csv")
