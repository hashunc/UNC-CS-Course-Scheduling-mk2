import pandas as pd
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpStatus
import os

time_slot_mapping = {
    "MWF_1": "8:00 – 8:50 a.m.",
    "MWF_2": "9:05 – 9:55 a.m.",
    "MWF_3": "10:10 – 11:00 a.m.",
    "MWF_4": "11:15 – 12:05 p.m.",
    "MWF_5": "12:20 – 1:10 p.m.",
    "MWF_6": "1:25 – 2:15 p.m.",
    "MWF_7": "2:30 – 3:20 p.m.",
    "MWF_8": "3:35 – 4:25 p.m.",
    "MWF_9": "4:40 – 5:30 p.m.",
    "MWF_10": "5:45 – 6:35 p.m.",
    "MW_1": "8:00 – 9:15 a.m.",
    "MW_2": "9:05 – 10:20 a.m.",
    "MW_3": "10:10 – 11:25 a.m.",
    "MW_4": "11:15 – 12:30 p.m.",
    "MW_5": "12:20 – 1:35 p.m.",
    "MW_6": "1:25 – 2:40 p.m.",
    "MW_7": "2:30 – 3:45 p.m.",
    "MW_8": "3:35 – 4:50 p.m.",
    "MW_9": "4:40 – 5:55 p.m.",
    "TTH_1": "8:00 – 9:15 a.m.",
    "TTH_2": "9:30 – 10:45 a.m.",
    "TTH_3": "11:00 – 12:15 p.m.",
    "TTH_4": "12:30 – 1:45 p.m.",
    "TTH_5": "2:00 – 3:15 p.m.",
    "TTH_6": "3:30 – 4:45 p.m.",
    "TTH_7": "5:00 – 6:15 p.m.",
}


def expand_time_slots(time_slots):
    expanded_slots = []
    for slot in str(time_slots).split(";"):
        parts = slot.split("_")
        if len(parts) == 2 and "," in parts[1]:
            base = parts[0] + "_"
            expanded_slots.extend([base + num for num in parts[1].split(",")])
        else:
            expanded_slots.append(slot)
    return ";".join(expanded_slots)


def read_data(data_file):
    print("read file: data.csv")
    data = pd.read_csv(data_file)

    data.columns = data.columns.str.strip().str.replace(" ", "")

    data["Professor_PreferredTimeSlots"] = data["Professor_PreferredTimeSlots"].apply(
        expand_time_slots
    )

    return data


def schedule_courses(data_file, output_file):
    data = read_data(data_file)

    course_ids = data["CourseID"].tolist()
    time_slots = list(
        set(data["Professor_PreferredTimeSlots"].str.split(";").explode())
    )

    X = {
        (c, s, t): LpVariable(f"X_{c}_{s}_{t}", cat="Binary")
        for c, s in zip(data["CourseID"], data["Sec"])
        for t in time_slots
    }

    prob = LpProblem("Course_Scheduling", LpMinimize)
    prob += lpSum(
        X[(c, s, t)] for c, s in zip(data["CourseID"], data["Sec"]) for t in time_slots
    )

    for _, row in data.iterrows():
        preferred_times = row["Professor_PreferredTimeSlots"].split(";")
        # Constraint 1: Courses must be scheduled within the professor's available time slots
        prob += lpSum(X[row["CourseID"], row["Sec"], t] for t in preferred_times) == 1

        # Constraint 2: The same CourseID with different Sec cannot be scheduled at the same time
    for c in set(data["CourseID"]):
        for t in time_slots:
            prob += lpSum(X[c, s, t] for s in data[data["CourseID"] == c]["Sec"]) <= 1

        # Constraint 3: The same professor cannot teach multiple courses at the same time
    for professor in set(data["ProfessorName"]):
        for t in time_slots:
            prob += (
                lpSum(
                    X[c, s, t]
                    for c, s in zip(data["CourseID"], data["Sec"])
                    if data.loc[
                        (data["CourseID"] == c) & (data["Sec"] == s), "ProfessorName"
                    ].values[0]
                    == professor
                )
                <= 1
            )

        # Constraint 4: Courses 301 and 211 cannot be scheduled at the same time
    for t in time_slots:
        prob += (
            lpSum(
                X[c, s, t]
                for c, s in zip(data["CourseID"], data["Sec"])
                if c in [301, 211]
            )
            <= 1
        )

        # Constraint 5: MoWeFr 3x50-min courses can only be scheduled in MoWe periods (excluding Period 1 and Period 10)
    for c, s in zip(data["CourseID"], data["Sec"]):
        for t in time_slots:
            if "MWF" in t and (t.endswith("_1") or t.endswith("_10")):
                prob += X[c, s, t] == 0

        # Constraint 6: MoWe 2x75-min courses must start in Periods 3, 5, 7, 9
    for c, s in zip(data["CourseID"], data["Sec"]):
        for t in time_slots:
            if "MW" in t and not any(t.endswith(f"_{p}") for p in [3, 5, 7, 9]):
                prob += X[c, s, t] == 0
        # Constraint 7: The number of courses scheduled in MWF_4,5,6,7 / MW_3,4,5 / TTH_3,4,5 should be at most 65% of total courses
        #               note, if this constraint lead no solution, then this constrain will be skip.
    high_demand_periods = [
        "MWF_4",
        "MWF_5",
        "MWF_6",
        "MWF_7",
        "MW_3",
        "MW_4",
        "MW_5",
        "TTH_3",
        "TTH_4",
        "TTH_5",
    ]
    total_courses = len(data)
    max_allowed = int(0.65 * total_courses)

    high_demand_courses = lpSum(
        X[c, s, t]
        for c, s in zip(data["CourseID"], data["Sec"])
        for t in time_slots
        if any(period in t for period in high_demand_periods)
    )

    # skip constrain 7 is no solution
    prob += high_demand_courses <= max_allowed

    try:
        prob.solve()
    except:
        print("At most 65 '%' in 11am-3pm failed, the program skipped the constrain 7.")

    # Calculate unscheduled classes
    assigned_courses = set((c, s) for c, s, t in X if X[c, s, t].varValue == 1)
    all_courses = set(zip(data["CourseID"], data["Sec"]))
    unassigned_courses = all_courses - assigned_courses

    if unassigned_courses:
        print("The following courses are not scheduled:")
        for c, s in unassigned_courses:
            print(f"CourseID: {c}, Sec: {s}")

    schedule = []
    for c, s in zip(data["CourseID"], data["Sec"]):
        for t in time_slots:
            if X[c, s, t].varValue == 1:
                professor_name = data.loc[
                    (data["CourseID"] == c) & (data["Sec"] == s), "ProfessorName"
                ].values[0]
                section = s
                formatted_time = f"{t}: {time_slot_mapping.get(t, t)}"
                schedule.append([c, section, professor_name, formatted_time])

    schedule_df = pd.DataFrame(
        schedule, columns=["CourseID", "Sec", "ProfessorName", "Time"]
    )
    schedule_df.drop_duplicates(inplace=True)

    schedule_df.to_csv(output_file, index=False)

    return schedule_df


data_file = "CSV/data.csv"
output_file = "CSV/schedule_output.csv"

schedule_courses(data_file, output_file)
