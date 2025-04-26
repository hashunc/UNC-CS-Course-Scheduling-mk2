# extract_and_clean_top_courses.py

import pandas as pd
import re
import os

# -------- 1. Load the Excel file --------
file_path = "data/Input/(For 523 team) Copy of Undergraduate Curriculum Coverage.xlsx"

print("\u2705 Reading file from:", os.path.abspath(file_path))

excel_data = pd.ExcelFile(file_path)
faculty_sheets = excel_data.sheet_names[2:]

# -------- 2. Extract top 5 courses per instructor --------
def extract_courses(sheet_name):
    df = excel_data.parse(sheet_name)
    if "Unnamed: 0" not in df.columns:
        return []
    df = df.dropna(subset=["Unnamed: 0"])

    extracted = []
    for _, row in df.iterrows():
        course_full_name = str(row["Unnamed: 0"]).strip()
        if "COMP" in course_full_name:
            readiness = pd.to_numeric(row.get("Readiness / Qualification"), errors="coerce")
            frequency = pd.to_numeric(row.get("Frequency / Expectation"), errors="coerce")
            total = readiness + frequency if pd.notna(readiness) and pd.notna(frequency) else None
            if total and total > 0:
                extracted.append({
                    "Instructor": sheet_name,
                    "Course": course_full_name,
                    "Readiness": readiness,
                    "Frequency": frequency,
                    "Total": total
                })
    return extracted

all_course_data = []
for sheet in faculty_sheets:
    all_course_data.extend(extract_courses(sheet))

df = pd.DataFrame(all_course_data)
top_5_per_instructor = (
    df.sort_values(by=["Instructor", "Total"], ascending=[True, False])
    .groupby("Instructor")
    .head(5)
    .reset_index(drop=True)
)

# -------- 3. Clean out instructors who are not teaching next semester --------
availability_df = pd.read_excel("data/Input/Temple of Automatic course scheduling data sheet (Responses) - Form Responses 1.xlsx")
availability_df.columns = availability_df.columns.str.strip()
availability_df["Last name"] = availability_df["Last name"].str.strip()

active_instructors = availability_df[
    pd.to_numeric(availability_df["How many classes you will teach in the next semester."], errors="coerce") > 0
]["Last name"].tolist()

# Only keep rows with Instructor in the active list
top_5_clean = top_5_per_instructor[top_5_per_instructor["Instructor"].isin(active_instructors)].reset_index(drop=True)

# -------- 4. Output --------
os.makedirs("data/CSV", exist_ok=True)
output_path = "data/CSV/top_courses_per_instructor_clean.csv"
top_5_clean.to_csv(output_path, index=False)
print(f"\u2705 Cleaned top 5 courses saved to: {output_path}")
