import pandas as pd
import re
import os

# -------- 1. Load the Excel file --------
file_path = "Input/(For 523 team) Copy of Undergraduate Curriculum Coverage.xlsx"
excel_data = pd.ExcelFile(file_path)

# Get all faculty sheet names (excluding the first two explanatory sheets)
faculty_sheets = excel_data.sheet_names[2:]

# -------- 2. Function to extract course data from a given sheet --------
def extract_courses(sheet_name):
    df = excel_data.parse(sheet_name)

    # Skip sheets without the expected course column
    if "Unnamed: 0" not in df.columns:
        return []

    # Drop rows without course names
    df = df.dropna(subset=["Unnamed: 0"])

    extracted = []

    for _, row in df.iterrows():
        course_full_name = str(row["Unnamed: 0"]).strip()

        # Only process rows that contain "COMP"
        if "COMP" in course_full_name:
            readiness = pd.to_numeric(row.get("Readiness / Qualification"), errors="coerce")
            frequency = pd.to_numeric(row.get("Frequency / Expectation"), errors="coerce")
            total = readiness + frequency if pd.notna(readiness) and pd.notna(frequency) else None

            # Only include courses with a non-zero total score
            if total and total > 0:
                extracted.append({
                    "Instructor": sheet_name,
                    "Course": course_full_name,  # Full course name as shown in the sheet
                    "Readiness": readiness,
                    "Frequency": frequency,
                    "Total": total
                })

    return extracted

# -------- 3. Extract course data for all faculty --------
all_course_data = []
for sheet in faculty_sheets:
    all_course_data.extend(extract_courses(sheet))

df = pd.DataFrame(all_course_data)

# -------- 4. Get top 5 courses by score for each instructor --------
top_5_per_instructor = (
    df.sort_values(by=["Instructor", "Total"], ascending=[True, False])
    .groupby("Instructor")
    .head(5)
    .reset_index(drop=True)
)

# -------- 5. Save the results to a CSV file --------
os.makedirs("CSV", exist_ok=True)
output_path = "CSV/top_courses_per_instructor.csv"
top_5_per_instructor.to_csv(output_path, index=False)
print(f"✅ Top 5 courses per instructor saved to: {output_path}")
