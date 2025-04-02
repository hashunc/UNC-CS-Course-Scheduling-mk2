import pandas as pd
import re

# Load Excel file
file_path = "Input/(For 523 team) Copy of Undergraduate Curriculum Coverage.xlsx"

excel_data = pd.ExcelFile(file_path)

# Get all form names (excluding the first two for explanatory purposes)
faculty_sheets = excel_data.sheet_names[2:]

# Extract function: extract course data from a worksheet
def extract_courses(sheet_name):
    df = excel_data.parse(sheet_name)
    
    # Delete rows which numbers=0
    df = df.dropna(subset=["Unnamed: 0"])
    
    extracted = []
    
    for _, row in df.iterrows():
        # Match course number 
        match = re.match(r"(COMP \d+)", str(row["Unnamed: 0"]))
        if match:
            readiness = pd.to_numeric(row.get("Readiness / Qualification"), errors="coerce")
            frequency = pd.to_numeric(row.get("Frequency / Expectation"), errors="coerce")
            total = readiness + frequency if pd.notna(readiness) and pd.notna(frequency) else None
            
            # Only keep records with a non-zero or NaN sum
            if total and total > 0:
                extracted.append({
                    "Instructor": sheet_name,
                    "Course": match.group(1),
                    "Readiness": readiness,
                    "Frequency": frequency,
                    "Total": total
                })
    
    return extracted

all_course_data = []
for sheet in faculty_sheets:
    all_course_data.extend(extract_courses(sheet))

df = pd.DataFrame(all_course_data)

# Take the top 5 courses (in descending order of total score) for each teacher.
top_5_per_instructor = (
    df.sort_values(by=["Instructor", "Total"], ascending=[True, False])
    .groupby("Instructor")
    .head(5)
    .reset_index(drop=True)
)

# 打印结果或保存为 CSV 文件
print(top_5_per_instructor)
top_5_per_instructor.to_csv("CSV/top_courses_per_instructor.csv", index=False)
