import subprocess
import pandas as pd
import sys
import os
import glob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import *

def run_script(script_path, step_number, description):
    print(f"\n▶ Running Step {step_number}: {description} ({script_path}) ...")
    subprocess.run(["python", script_path], check=True)
    print(f"✅ Step {step_number} completed successfully!")

def clear_folder(folder_path):
    """Delete all files under a folder."""
    files = glob.glob(os.path.join(folder_path, "*"))
    for f in files:
        try:
            os.remove(f)
        except IsADirectoryError:
            pass  # Ignore subfolders (safe)

# 🔵 Clear folders before running anything
print("🧹 Clearing data/CSV and data/Output folders...")
clear_folder("data/CSV")
clear_folder("data/Output")
print("✅ Folders cleared successfully!")

print("🔵 Starting full all_generate pipeline...")

# Step 1: Convert classroom data to room.csv
run_script(CONVERT_CLASSROOM_SCRIPT, 1, "Convert ClassRoom.xlsx to room.csv")

# Step 2: Extraction scripts
run_script(EXTRACT_TOP_COURSES_SCRIPT, 2, "Extract and clean top courses")
run_script(EXTRACT_TIME_SLOTS_SCRIPT, 3, "Extract faculty time slots")

# Step 3: Generation scripts
run_script(GENERATE_NO_590_790_SCRIPT, 4, "Generate assignments (no 590/790)")
run_script(GENERATE_590_790_SCRIPT, 5, "Generate assignments (590/790)")
run_script(GENERATE_590_AND_790_SCRIPT, 6, "Generate assignments (590&790 combined)")

print("\n✅ All assignment scripts executed. Now merging results...\n")

# Step 4: Merge all generated CSVs
merged_no_590_790 = pd.read_csv(OUTPUT_MERGED_NO_590_790)
merged_590_790 = pd.read_csv(OUTPUT_MERGED_590_790)
merged_590_and_790 = pd.read_csv(OUTPUT_MERGED_590_AND_790)

full_assignments = pd.concat([merged_no_590_790, merged_590_790, merged_590_and_790], ignore_index=True)

# Step 5: Sort by CourseID number and Sec
full_assignments["Course Num"] = full_assignments["CourseID"].str.extract(r"COMP (\d+)").fillna(0).astype(int)
full_assignments["Sec"] = full_assignments["Sec"].astype(int)

full_assignments = full_assignments.sort_values(by=["Course Num", "Sec"]).drop(columns=["Course Num"]).reset_index(drop=True)

# Step 6: Save final new_data.csv
full_assignments.to_csv(OUTPUT_NEW_DATA_CSV, index=False)
print(f"✅ Final merged output saved to: {OUTPUT_NEW_DATA_CSV}")

# Step 7: Run check_unassigned_courses
print("\n🔵 Running course assignment check...")
run_script(CHECK_UNASSIGNED_SCRIPT, 7, "Check unassigned courses")

# Step 8: Run schedule.py to generate schedule_output.csv
print("\n🔵 Running scheduling optimizer...")
run_script(SCHEDULE_SCRIPT, 8, "Generate schedule_output.csv")

# Step 8.5: Split COMP 590&790
print("\n🔵 Splitting COMP 590&790 into COMP 590 and COMP 790...")
run_script(SPLIT_590_790_SCRIPT, 8.5, "Split 590&790 in schedule_output.csv")

# Step 8.6: Copy schedule_output.csv to Output folder
print("\n🔵 Copying schedule_output.csv to data/Output/...")
run_script(COPY_SCHEDULE_OUTPUT_SCRIPT, 8.6, "Copy schedule_output.csv to Output")

# Step 9: Create Google Calendar format
print("\n🔵 Converting schedule to Google Calendar format...")
run_script(CONVERT_TO_CALENDAR_SCRIPT, 9, "Generate google_calendar_format.csv")

print("\n🎯 All steps completed successfully! The system is fully updated and schedule generated.")
