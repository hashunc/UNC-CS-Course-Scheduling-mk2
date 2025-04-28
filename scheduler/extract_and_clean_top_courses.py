import pandas as pd
import os
from config import (
    INPUT_CURRICULUM_COVERAGE,
    INPUT_AVAILABILITY,
    OUTPUT_TOP_COURSES,
    OUTPUT_SKIPPED_FACULTY,
    OUTPUT_MISSING_FACULTYQUALIFICATION,  # 加了这个
)

# -------- 1. Load the Excel file --------
print("Reading file from:", os.path.abspath(INPUT_CURRICULUM_COVERAGE))

excel_data = pd.ExcelFile(INPUT_CURRICULUM_COVERAGE)
faculty_sheets = excel_data.sheet_names[2:]  # Skip first two sheets

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
            if pd.notna(readiness) and pd.notna(frequency):
                total = readiness + frequency
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

# -------- 2.5 Filter low Readiness or Frequency courses --------
before_filter = len(df)
df = df[(df["Readiness"] > 1) & (df["Frequency"] > 1)].reset_index(drop=True)
after_filter = len(df)
print(f"✅ Filtered out {before_filter - after_filter} courses with Readiness <= 1 or Frequency <= 1.")

# -------- Continue: Extract top 5 per instructor --------
top_5_per_instructor = (
    df.sort_values(by=["Instructor", "Total"], ascending=[True, False])
    .groupby("Instructor")
    .head(5)
    .reset_index(drop=True)
)

# -------- 3. Filter active instructors based on Responses --------
availability_df = pd.read_excel(INPUT_AVAILABILITY)
availability_df.columns = availability_df.columns.str.strip()
availability_df["Last name"] = availability_df["Last name"].str.strip()
availability_df["First name"] = availability_df["First name"].str.strip()

active_instructors = availability_df[
    pd.to_numeric(availability_df["How many classes you will teach in the next semester."], errors="coerce") > 0
][["Last name", "First name"]].rename(columns={"Last name": "LastName", "First name": "FirstName"})

# -------- 4. Check for missing instructors --------
faculty_in_curriculum = set(faculty_sheets)
faculty_in_responses = set(active_instructors["LastName"].tolist())

missing_last_names = sorted(list(faculty_in_responses - faculty_in_curriculum))

missing_full_info = active_instructors[
    active_instructors["LastName"].isin(missing_last_names)
]

if not missing_full_info.empty:
    print("\n⚠️ Warning: These instructors are in Responses but not in FacultyQualificationPreference:")
    for _, row in missing_full_info.iterrows():
        print(f" - {row['LastName']}, {row['FirstName']}")
    
    os.makedirs(os.path.dirname(OUTPUT_MISSING_FACULTYQUALIFICATION), exist_ok=True)
    missing_full_info.to_csv(OUTPUT_MISSING_FACULTYQUALIFICATION, index=False)
    print(f"✅ Missing instructors saved to {OUTPUT_MISSING_FACULTYQUALIFICATION}")
else:
    print("\n✅ No missing instructors detected between Responses and FacultyQualificationPreference.")

# -------- 5. Keep only active instructors --------
top_5_clean = top_5_per_instructor[
    top_5_per_instructor["Instructor"].isin(active_instructors["LastName"].tolist())
].reset_index(drop=True)

# -------- 6. Save cleaned top 5 courses --------
os.makedirs(os.path.dirname(OUTPUT_TOP_COURSES), exist_ok=True)
top_5_clean.to_csv(OUTPUT_TOP_COURSES, index=False)
print(f"✅ Cleaned top 5 courses saved to: {OUTPUT_TOP_COURSES}")
