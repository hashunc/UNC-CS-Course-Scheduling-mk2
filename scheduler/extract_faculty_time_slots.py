import pandas as pd

# Load the Excel file from the correct relative path
file_path = "../data/Input/Temple of Automatic course scheduling data sheet (Responses) - Form Responses 1.xlsx"
df = pd.read_excel(file_path)

# Mapping from original column names to time slot codes
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
df.columns = [col.strip() for col in df.columns]

# Filter only the relevant columns
required_columns = ["Last name", "First name"] + list(column_to_slot.keys())
filtered_df = df[required_columns]

# Extract available time slots
results = []
for _, row in filtered_df.iterrows():
    last = row["Last name"]
    first = row["First name"]
    time_slots = []

    for col, slot in column_to_slot.items():
        if str(row[col]).strip().upper() == "V":
            time_slots.append(slot)

    if time_slots:
        results.append([f"{last} {first}", ",".join(time_slots)])

# Output to CSV
output_df = pd.DataFrame(results, columns=["Name", "Available Time Slots"])
output_df.to_csv("../data/CSV/faculty_time_preferences.csv", index=False)
print(output_df)
