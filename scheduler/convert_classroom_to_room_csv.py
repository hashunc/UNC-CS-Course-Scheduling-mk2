# scheduler/convert_classroom_to_room_csv.py

import pandas as pd
from pathlib import Path
from config import INPUT_CLASSROOM, OUTPUT_ROOM_CSV

input_path = Path(INPUT_CLASSROOM)
output_path = Path(OUTPUT_ROOM_CSV)

print(f"📥 Reading: {input_path}")
df = pd.read_excel(input_path)

df.columns = df.columns.str.strip()

df.to_csv(output_path, index=False)
print(f"✅ Saved full room info to {output_path}")
