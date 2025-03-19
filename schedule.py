import pandas as pd
from pulp import LpProblem, LpVariable, LpMinimize, lpSum

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
    "MW_2": "9:30 – 10:45 a.m.",
    "MW_3": "11:00 – 12:15 p.m.",
    "MW_4": "12:30 – 1:45 p.m.",
    "MW_5": "2:00 – 3:15 p.m.",
    "MW_6": "3:30 – 4:45 p.m.",
    "MW_7": "5:00 – 6:15 p.m.",
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


def read_rooms(rooms_file):
    print("read file: room.csv")
    data = pd.read_csv(rooms_file)

    data.columns = data.columns.str.strip().str.replace(" ", "")

    return data


def read_scores(scores_file):
    print("read file: scores.csv")
    scores = pd.read_csv(scores_file)
    
    scores.columns = scores.columns.str.strip().str.replace(" ", "")
    
    # create map of professor-course-ability_score-willingness_score
    prof_course_scores = {}
    for _, row in scores.iterrows():
        prof = row['ProfessorName']
        course = row['CourseID']
        teaching_ability = row['TeachingAbility']
        teaching_willingness = row['TeachingWillingness']
        
        prof_course_scores[(prof, course)] = (teaching_ability, teaching_willingness)
    
    return prof_course_scores


def get_professor_score(professor, course, prof_course_scores):
    # if there's no record of scores, it means the professor is unable & unwilling to teach the course
    # so we can return (0, 0)
    scores = prof_course_scores.get((professor, course), (0, 0))
    return scores[0] + scores[1]


def schedule_courses(data_file, rooms_file, scores_file, output_file):
    data = read_data(data_file)
    rooms_data = read_rooms(rooms_file)
    prof_course_scores = read_scores(scores_file)

    course_ids = data["CourseID"].tolist()
    secs = data["Sec"].tolist()
    time_slots = list(
        set(data["Professor_PreferredTimeSlots"].str.split(";").explode())
    )
    print()
    room_ids = rooms_data["RoomID"].tolist()

    X = {
        (c, s, t, r): LpVariable(f"X_{c}_{s}_{t}_{r}", cat="Binary")
        for c, s in zip(course_ids, secs)
        for t in time_slots
        for r in room_ids
    }

    prob = LpProblem("Course_Scheduling", LpMinimize)
    prob += lpSum(
        X[c, s, t, r] for c, s in zip(course_ids, secs) for t in time_slots for r in room_ids
    )

    
    # Constraint 1：Courses should be scheduled within the professor's available time slots BUT NOT NECESSARY

    # create preference penalty variables
    preference_penalties = {}
    for idx, row in data.iterrows():
        preference_penalties[row["CourseID"], row["Sec"]] = LpVariable(f"Penalty_{row['CourseID']}_{row['Sec']}", lowBound=0)

    # use big weight 100
    prob += 100 * lpSum(preference_penalties.values())

    # use soft constraint
    for idx, row in data.iterrows():
        # make sure every course would be arranged to 1 time slot and 1 room
        prob += lpSum(X[row["CourseID"], row["Sec"], t, r] for t in time_slots for r in room_ids) == 1

        # get preference and non-preference time slots
        preferred_times = row["Professor_PreferredTimeSlots"].split(";")
        non_preferred_times = [t for t in time_slots if t not in preferred_times]

        # if the professor has non-preference time slots
        if len(non_preferred_times) > 0:
            prob += lpSum(X[row["CourseID"], row["Sec"], t, r] for t in non_preferred_times for r in room_ids) <= preference_penalties[row["CourseID"], row["Sec"]]
        # if the professor has preference time slots
        if len(preferred_times) > 0:
            # encourage to use preference time slots
            prob += lpSum(X[row["CourseID"], row["Sec"], t, r] for t in preferred_times for r in room_ids) + preference_penalties[row["CourseID"], row["Sec"]] >= 1

    # for _, row in data.iterrows():
    #     preferred_times = row["Professor_PreferredTimeSlots"].split(";")
    #     prob += lpSum(X[row["CourseID"], row["Sec"], t, r] for t in preferred_times for r in room_ids) == 1


    # Constraint 2: The same CourseID with different Sec cannot be scheduled at the same time
    for c in set(course_ids):
        for t in time_slots:
            prob += lpSum(X[c, s, t, r] for s in data[data["CourseID"] == c]["Sec"] for r in room_ids) <= 1

    
    # Constraint 3: The same professor cannot teach multiple courses at the same time
    for professor in set(data["ProfessorName"]):
        for t in time_slots:
            prob += (
                lpSum(
                    X[c, s, t, r]
                    for c, s in zip(course_ids, secs)
                    for r in room_ids
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
                X[c, s, t, r]
                for c, s in zip(course_ids, secs)
                for r in room_ids
                if c in [301, 211]
            )
            <= 1
        )

    
    # Constraint 5: MoWeFr 3x50-min courses can only be scheduled in MoWe periods (excluding Period 1 and Period 10)
    for c, s in zip(course_ids, secs):
        for t in time_slots:
            if "MWF" in t and (t.endswith("_1") or t.endswith("_10")):
                for r in room_ids:
                    prob += X[c, s, t, r] == 0

    
    # Constraint 6: MoWe 2x75-min courses must start in Periods 3, 5, 7, 9
    for c, s in zip(course_ids, secs):
        for t in time_slots:
            if "MW" in t and not any(t.endswith(f"_{p}") for p in [3, 5, 7, 9]):
                for r in room_ids:
                    prob += X[c, s, t, r] == 0
        
    
    # Constraint 7: The number of courses scheduled in MWF_4,5,6,7 / MW_3,4,5 / TTH_3,4,5 should be at most 65% of total courses
    # note, if this constraint lead no solution, then this constrain will be skip.
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
        X[c, s, t, r]
        for c, s in zip(course_ids, secs)
        for t in time_slots
        for r in room_ids
        if any(period in t for period in high_demand_periods)
    )

    # skip constraint 7 if there is no solution
    prob += high_demand_courses <= max_allowed
    
    
    # Constraint 8: Core course must be taught in a semester
    core_courses = [
        # waiting to add core courses...
    ]
    for c in core_courses:
        related_secs = [s for c_id, s in zip(course_ids, secs) if c_id == c]
        prob += lpSum(X[c, s, t, r] 
            for s in related_secs 
            for t in time_slots 
            for r in room_ids
        ) >= 1


    # Constraint 9: Every room in a time slot can only be arranged at most one course
    for t in time_slots:
        for r in room_ids:
            prob += lpSum(X[(c, s, t, r)] for c, s in zip(data["CourseID"], data["Sec"])) <= 1
    

    # Constraint 10: The enroll capacity of a course must be lower than the arranged room capacity.
    for c, s in zip(data["CourseID"], data["Sec"]):
        course_capacity = data.loc[(data["CourseID"] == c) & (data["Sec"] == s), "EnrollCapacity"].values[0]
        for t in time_slots:
            for r in room_ids:
                # check if the room capacity is smaller than enroll capacity of the course
                if rooms_data.loc[rooms_data["RoomID"] == r, "Capacity"].values[0] < course_capacity:
                    prob += X[c, s, t, r] == 0 



    try:
        prob.solve()
    except:
        print("At most 65 '%' in 11am-3pm failed, the program skipped the constrain 7.")

    # Calculate unscheduled classes
    assigned_courses = set((c, s) for c, s, t, r in X if X[c, s, t, r].varValue == 1)
    all_courses = set(zip(course_ids, secs))
    unassigned_courses = all_courses - assigned_courses

    if unassigned_courses:
        print("The following courses are not scheduled:")
        for c, s in unassigned_courses:
            print(f"CourseID: {c}, Sec: {s}")

    schedule = []
    for c, s in zip(course_ids, secs):
        for t in time_slots:
            for r in room_ids:
                if X[c, s, t, r].varValue == 1:
                    professor_name = data.loc[
                        (data["CourseID"] == c) & (data["Sec"] == s), "ProfessorName"
                    ].values[0]
                    section = s
                    formatted_time = f"{t}: {time_slot_mapping.get(t, t)}"
                    room = r
                    schedule.append([c, section, professor_name, formatted_time, room])

    schedule_df = pd.DataFrame(
        schedule, columns=["CourseID", "Sec", "ProfessorName", "Time", "Room"]
    )
    schedule_df.drop_duplicates(inplace=True)

    schedule_df.to_csv(output_file, index=False)

    # print("============testing============")
    # print(rooms_data.loc[rooms_data["RoomID"] == "Other", "Capacity"].values[0])

    return schedule_df


data_file = "CSV/data.csv"
rooms_file = "CSV/room.csv"
scores_file = "CSV/scores.csv"
output_file = "CSV/schedule_output.csv"

schedule_courses(data_file, rooms_file, scores_file, output_file)