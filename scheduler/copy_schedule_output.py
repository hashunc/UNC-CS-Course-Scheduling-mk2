# scheduler/copy_schedule_output.py

import shutil
import pandas as pd
import re
from pathlib import Path
from config import OUTPUT_SCHEDULE_OUTPUT, OUTPUT_COPIED_SCHEDULE

# Step 1: Copy original file
source = Path(OUTPUT_SCHEDULE_OUTPUT)
destination = Path(OUTPUT_COPIED_SCHEDULE)

destination.parent.mkdir(parents=True, exist_ok=True)
shutil.copy(source, destination)
print(f"✅ schedule_output.csv copied to {destination}")

# Step 2: Deal with rows
schedule_df = pd.read_csv(destination)

def clean_time_prefix(time_str):
    if pd.isna(time_str):
        return time_str
    # Replace TTH_x, MW_x, MWF_x with TTH, MW, MWF
    cleaned = re.sub(r"^(TTH|MWF|MW)_\d+: ", r"\1: ", time_str)
    return cleaned

schedule_df["Time"] = schedule_df["Time"].apply(clean_time_prefix)

# Save back
schedule_df.to_csv(destination, index=False)
print("✅ Time column cleaned and saved.")
