# scheduler/all_generate.py

import subprocess
import pandas as pd

def run_script(script_path, step_number, description):
    print(f"\n▶ Running Step {step_number}: {description} ({script_path}) ...")
    subprocess.run(["python", script_path], check=True)
    print(f"✅ Step {step_number} completed successfully!")

print("🔵 Starting full all_generate pipeline...")

# Step 1: Convert classroom data to room.csv
run_script("scheduler/convert_classroom_to_room_csv.py", 1, "Convert ClassRoom.xlsx to room.csv")

# Step 2: Extraction scripts
run_script("scheduler/extract_and_clean_top_courses.py", 2, "Extract and clean top courses")
run_script("scheduler/extract_faculty_time_slots.py", 3, "Extract faculty time slots")

# Step 3: Generation scripts
run_script("scheduler/generate_assignments_no_590_790.py", 4, "Generate assignments (no 590/790)")
run_script("scheduler/generate_assignments_590_790.py", 5, "Generate assignments (590/790)")
run_script("scheduler/generate_assignments_590&790.py", 6, "Generate assignments (590&790 combined)")

print("\n✅ All assignment scripts executed. Now merging results...\n")

# Step 4: Merge all generated CSVs
merged_no_590_790 = pd.read_csv("data/CSV/merged_assignments_no_590_790.csv")
merged_590_790 = pd.read_csv("data/CSV/merged_assignments_590_790.csv")
merged_590_and_790 = pd.read_csv("data/CSV/merged_assignments_590&790_only.csv")

full_assignments = pd.concat([merged_no_590_790, merged_590_790, merged_590_and_790], ignore_index=True)

# Step 5: Sort by CourseID number and Sec
full_assignments["Course Num"] = full_assignments["CourseID"].str.extract(r"COMP (\d+)").fillna(0).astype(int)
full_assignments["Sec"] = full_assignments["Sec"].astype(int)

full_assignments = full_assignments.sort_values(by=["Course Num", "Sec"]).drop(columns=["Course Num"]).reset_index(drop=True)

# Step 6: Save final new_data.csv
full_assignments.to_csv("data/CSV/new_data.csv", index=False)
print("✅ Final merged output saved to: data/CSV/new_data.csv")

# Step 7: Run check_unassigned_courses
print("\n🔵 Running course assignment check...")
run_script("scheduler/check_unassigned_courses.py", 7, "Check unassigned courses")

# Step 8: Run schedule.py to generate schedule_output.csv
print("\n🔵 Running scheduling optimizer...")
run_script("scheduler/schedule.py", 8, "Generate schedule_output.csv")

print("\n🎯 All steps completed successfully! The system is fully updated and schedule generated.")
