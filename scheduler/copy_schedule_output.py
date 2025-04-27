# scheduler/copy_schedule_output.py

import shutil
from pathlib import Path
import pandas as pd
import re

# Step 1: 复制原文件
source = Path("data/CSV/schedule_output.csv")
destination = Path("data/Output/schedule_output.csv")

destination.parent.mkdir(parents=True, exist_ok=True)
shutil.copy(source, destination)
print(f"✅ schedule_output.csv copied to {destination}")

# Step 2: 清理 Time 列
schedule_df = pd.read_csv(destination)

def clean_time_prefix(time_str):
    if pd.isna(time_str):
        return time_str
    # 替换 TTH_x, MW_x, MWF_x 成 TTH, MW, MWF
    cleaned = re.sub(r"^(TTH|MWF|MW)_\d+: ", r"\1: ", time_str)
    return cleaned

schedule_df["Time"] = schedule_df["Time"].apply(clean_time_prefix)

# 保存回去
schedule_df.to_csv(destination, index=False)
print("✅ Time column cleaned and saved.")
