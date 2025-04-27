# scheduler/split_590_790.py

import pandas as pd

# Load original schedule
df = pd.read_csv("data/CSV/schedule_output.csv")

# Create a list to collect the processed rows
processed_rows = []

for idx, row in df.iterrows():
    if row["CourseID"] == "COMP 590&790":
        row_590 = row.copy()
        row_590["CourseID"] = "COMP 590"
        processed_rows.append(row_590)

        row_790 = row.copy()
        row_790["CourseID"] = "COMP 790"
        processed_rows.append(row_790)
    else:
        processed_rows.append(row)

# Create new DataFrame
new_df = pd.DataFrame(processed_rows)

# --- Sort ---
new_df["Course Num"] = new_df["CourseID"].str.extract(r"COMP (\d+)").fillna(0).astype(int)
new_df["Sec"] = new_df["Sec"].astype(int)

new_df = new_df.sort_values(by=["Course Num", "Sec"]).drop(columns=["Course Num"]).reset_index(drop=True)

# Save back
new_df.to_csv("data/CSV/schedule_output.csv", index=False)
print("✅ Finished splitting COMP 590&790, sorted, and saved to schedule_output.csv")
