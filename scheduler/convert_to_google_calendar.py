# scheduler/convert_to_google_calendar.py

import pandas as pd
from datetime import datetime

schedule_df = pd.read_csv("data/CSV/schedule_output.csv")

day_mapping = {
    "MWF": ["Monday", "Wednesday", "Friday"],
    "MW": ["Monday", "Wednesday"],
    "TTH": ["Tuesday", "Thursday"],
    "2H_M": ["Monday"],
    "2H_T": ["Tuesday"],
    "2H_W": ["Wednesday"],
    "2H_TH": ["Thursday"],
    "2H_F": ["Friday"],
}

start_week_date = {
    "Monday": "2025-08-18",
    "Tuesday": "2025-08-19",
    "Wednesday": "2025-08-20",
    "Thursday": "2025-08-21",
    "Friday": "2025-08-22",
}

calendar_events = []

for idx, row in schedule_df.iterrows():
    course_id = row["CourseID"]
    sec = row["Sec"]
    professor = row["ProfessorName"]
    room = row["Room"]
    time_info = row["Time"]

    time_info = time_info.replace("–", "-").replace("—", "-")

    if ":" not in time_info:
        continue

    try:
        period_code, hours = time_info.split(": ", 1)
        if "-" not in hours:
            continue
        start_raw, end_raw = hours.split("-")
        start_raw = start_raw.strip()
        end_raw = end_raw.strip()

        if "a.m." in end_raw.lower():
            end_am_pm = "AM"
        elif "p.m." in end_raw.lower():
            end_am_pm = "PM"
        else:
            continue

        if "a.m." in start_raw.lower() or "p.m." in start_raw.lower():
            start_am_pm = None
        else:
            start_am_pm = end_am_pm

        start_clean = start_raw.replace(".", "").replace("a.m", "AM").replace("p.m", "PM")
        end_clean = end_raw.replace(".", "").replace("a.m", "AM").replace("p.m", "PM")

        if start_am_pm:
            start_clean += " " + start_am_pm

        start_time_dt = datetime.strptime(start_clean, "%I:%M %p")
        end_time_dt = datetime.strptime(end_clean, "%I:%M %p")

        if start_time_dt > end_time_dt and end_am_pm == "PM":
            start_time_dt = datetime.strptime(start_raw + " AM", "%I:%M %p")

        start_time_24h = start_time_dt.strftime("%H:%M")
        end_time_24h = end_time_dt.strftime("%H:%M")

        found = False
        for prefix, days in day_mapping.items():
            if period_code.startswith(prefix):
                for day in days:
                    calendar_events.append({
                        "CourseID": course_id,
                        "Subject": f"{course_id} Sec {sec}",
                        "Start Date": start_week_date[day],
                        "Start Time": start_time_24h,
                        "End Date": start_week_date[day],
                        "End Time": end_time_24h,
                        "Description": f"Instructor: {professor}",
                        "Location": room,
                        "Weekly Repeats": "Yes"
                    })
                found = True
                break

    except Exception as e:
        print(f"⚠️ Error at row {idx}: {e}")
        continue

calendar_df = pd.DataFrame(calendar_events)

# deal with Course Number
calendar_df["Course Num"] = calendar_df["CourseID"].str.extract(r"COMP (\d+)").astype(float)

# split undergraduate 和 graduate
undergrad_df = calendar_df[calendar_df["Course Num"] < 600].drop(columns=["Course Num"]).reset_index(drop=True)
grad_df = calendar_df[calendar_df["Course Num"] >= 600].drop(columns=["Course Num"]).reset_index(drop=True)

# save
undergrad_df.to_csv("data/Output/google_calendar_undergraduate.csv", index=False)
grad_df.to_csv("data/Output/google_calendar_graduated.csv", index=False)

print("✅ Saved undergraduate_calendar.csv and graduate_calendar.csv in data/CSV/")
