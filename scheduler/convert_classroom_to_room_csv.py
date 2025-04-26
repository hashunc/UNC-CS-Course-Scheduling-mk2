# scheduler/convert_classroom_to_room_csv.py

import pandas as pd
from pathlib import Path

input_path = Path("data/Input/ClassRoom.xlsx")
output_path = Path("data/CSV/room.csv")

print(f"📥 Reading: {input_path}")
df = pd.read_excel(input_path)

df.columns = df.columns.str.strip()

df.to_csv(output_path, index=False)
print(f"✅ Saved full room info to {output_path}")
