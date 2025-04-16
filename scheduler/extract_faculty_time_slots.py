import pandas as pd

# Load Excel
file_path = "data/Input/Temple of Automatic course scheduling data sheet (Responses) - Form Responses 1.xlsx"
availability_df = pd.read_excel(file_path)

# Time slot header → code mapping
column_to_slot = {
    "M/W/F schedule [8:00 - 8:50 a.m.]": "MWF_1",
    "M/W/F schedule [9:05 - 9:55 a.m.]": "MWF_2",
    "M/W/F schedule [10:10 - 11:00 a.m.]": "MWF_3",
    "M/W/F schedule [11:15 - 12:05 p.m.]": "MWF_4",
    "M/W/F schedule [12:20 - 1:10 p.m.]": "MWF_5",
    "M/W/F schedule [1:25 - 2:15 p.m.]": "MWF_6",
    "M/W/F schedule [2:30 - 3:20 p.m.]": "MWF_7",
    "M/W/F schedule [3:35 - 4:25 p.m.]": "MWF_8",
    "M/W/F schedule [4:40 - 5:30 p.m.]": "MWF_9",
    "M/W/F schedule [5:45 - 6:35 p.m.]": "MWF_10",
    "M/W schedule [8:05 - 9:15 a.m.]": "MW_12",
    "M/W schedule [10:10 - 11:25 a.m.]": "MW_34",
    "M/W schedule [12:20 - 1:35 p.m.]": "MW_56",
    "M/W schedule [2:30 - 3:45 p.m.]": "MW_78",
    "M/W schedule [4:40 - 5:55 p.m.]": "MW_90",
    "T/TH schedule [8:00 - 9:15 a.m.]": "TTH_1",
    "T/TH schedule [9:30 - 10:45  a.m.]": "TTH_2",
    "T/TH schedule [11:00 - 12:15 p.m.]": "TTH_3",
    "T/TH schedule [12:30 - 1:45 p.m.]": "TTH_4",
    "T/TH schedule [2:00 - 3:15 p.m.]": "TTH_5",
    "T/TH schedule [3:30 - 4:45 p.m.]": "TTH_6",
    "T/TH schedule [5:00 - 6:15 p.m.]": "TTH_7"
}

# Clean column names
availability_df.columns = [col.strip() for col in availability_df.columns]

# Select relevant columns
time_slot_cols = list(column_to_slot.keys())
required_columns = [
    "Last name", "First name",
    "How many classes you will teach in the next semester.",
    "If you are teaching a single two-hour class, please click this button. (If not, please skip this question.)"
] + time_slot_cols

filtered_df = availability_df[required_columns]

# Parse availability
results = []
skipped = []

for _, row in filtered_df.iterrows():
    last = str(row["Last name"]).strip()
    first = str(row["First name"]).strip()
    full_name = f"{last} {first}"

    # Check teaching load
    try:
        course_count = int(row["How many classes you will teach in the next semester."])
    except:
        reason = "invalid class count"
        skipped.append([full_name, reason])
        continue

    if course_count == 0:
        reason = "teaching 0 classes"
        skipped.append([full_name, reason])
        continue

    # Gather time slots
    time_slots = []
    for col in time_slot_cols:
        val = str(row[col]).strip().upper()
        if val == "V":
            time_slots.append(column_to_slot[col])

    # 2H course flag
    two_hour = str(row["If you are teaching a single two-hour class, please click this button. (If not, please skip this question.)"]).strip()
    if two_hour == "Yes, I only teach one 2-hour course.":
        time_slots.append("2H_class")

    if time_slots:
        results.append([full_name, ",".join(time_slots)])
    else:
        reason = "no time preferences marked"
        skipped.append([full_name, reason])

# Export valid preferences
output_df = pd.DataFrame(results, columns=["Name", "Available Time Slots"])
output_df.to_csv("data/CSV/faculty_time_preferences.csv", index=False)

# Export skipped reasons
skipped_df = pd.DataFrame(skipped, columns=["Name", "Reason Skipped"])
skipped_df.to_csv("data/CSV/skipped_faculty.csv", index=False)

print("✅ Exported:")
print("  • data/CSV/faculty_time_preferences.csv")
print("  • data/CSV/skipped_faculty.csv")
