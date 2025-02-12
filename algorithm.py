import pulp
import sqlite3
def load_days():
    return ['Monday', 'Tuesday', 'Wednesday']

def load_periods():
    mwf_periods = {
        1: {'start_time': '8:00AM', 'duration': 50},
        2: {'start_time': '9:05AM', 'duration': 50},
        3: {'start_time': '10:10AM', 'duration': 50},
        4: {'start_time': '11:15AM', 'duration': 50},
        5: {'start_time': '12:20PM', 'duration': 50},
        6: {'start_time': '1:25PM', 'duration': 50},
        7: {'start_time': '2:30PM', 'duration': 50},
        8: {'start_time': '3:35PM', 'duration': 50},
}

# TTH periods (75 minutes each)
    tth_periods = {
        1: {'start_time': '8:00AM', 'duration': 75},
        2: {'start_time': '9:30AM', 'duration': 75},
        3: {'start_time': '11:00AM', 'duration': 75},
        4: {'start_time': '12:30PM', 'duration': 75},
        5: {'start_time': '2:00PM', 'duration': 75},
        6: {'start_time': '3:30PM', 'duration': 75},
        7: {'start_time': '5:00PM', 'duration': 75}
    }

# MW periods (75 minutes each)
    mw_periods = {
    1: {'start_time': '8:00AM', 'duration': 75},
    3: {'start_time': '10:10AM', 'duration': 75},
    5: {'start_time': '12:20PM', 'duration': 75},
    7: {'start_time': '2:30PM', 'duration': 75},
}
    return mwf_periods, tth_periods, mw_periods


def load_meeting_patterns(mwf_periods, tth_periods, mw_periods):
    meeting_patterns = {
    'MWF': {'days': ['Monday', 'Wednesday', "Friday"], 'periods': mwf_periods},
    'TTH': {'days': ['Tuesday', 'Thursday'], 'periods': tth_periods},
    'MW': {'days': ['Monday', "Wednesday"], 'periods': mw_periods},
    #'WF': {'days': ['Wednesday', 'Friday'], 'periods': wf_periods}
}
    return meeting_patterns



def create_professors_data():
    # Fetch qualified courses
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM QualifiedCourses")
        qcourses = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as error:
        print(f"Error occurred while fetching qualified courses: {error}")
        qcourses = []
    finally:
        connection.close()

    # Fetch distinct professors from Availability
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT DISTINCT Prof FROM Availability")
        profs = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as error:
        print(f"Error occurred while fetching professors: {error}")
        profs = []
    finally:
        connection.close()

    # Convert list of dicts to a list of professor names
    new_profs = [prof['Prof'] for prof in profs]

    # Initialize the final structure
    professors_json = {}
    for prof in new_profs:
        professors_json[prof] = {
            'qualified_courses': [],
            'availability': [],
            'max_classes': 0
        }

    # Assign qualified courses to professors
    for qcourse in qcourses:
        professor = qcourse['Prof']
        if professor in professors_json:
            professors_json[professor]['qualified_courses'].append(qcourse['Course'])

    # Fetch availabilities
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM Availability")
        availabilities = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as error:
        print(f"Error occurred while fetching availabilities: {error}")
        availabilities = []
    finally:
        connection.close()

    # Assign availability to professors
    for availability in availabilities:
        professor = availability['Prof']
        if professor in professors_json:
            professors_json[professor]['availability'].append((availability['AvailableMP'], availability['AvailablePeriod']))

    # Fetch max courses
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM MaxCourses")
        max_courses = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as error:
        print(f"Error occurred while fetching max courses: {error}")
        max_courses = []
    finally:
        connection.close()

    # Assign max_classes to professors
    for m in max_courses:
        professor = m['Prof']
        if professor in professors_json:
            professors_json[professor]['max_classes'] = m['MaxCourses']

    # Return the final dictionary
    return professors_json


import sqlite3

def create_rooms_data():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    
    cursor = connection.cursor()
    try:
        # Fetch both Room and SeatCapacity in a single query
        query = "SELECT Room, SeatCapacity FROM Rooms"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Convert fetched rows into a dictionary
        rooms_json = {}
        for row in rows:
            room_name = row["Room"]
            capacity = row["SeatCapacity"]
            rooms_json[room_name] = {
                "capacity": capacity
            }

        return rooms_json
    except sqlite3.Error as error:
        print(f"Error occurred: {error}")
        return {}
    finally:
        connection.close()
        print("Database connection closed.")

import sqlite3

def create_courses_data():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    try:
        # Fetch all courses and their details
        query = "SELECT * FROM CoursesAndSections"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Build the dictionary
        courses_json = {}
        for row in rows:
            course_name = row["Course"]
            title = row["Title"]
            # Convert section to int if it's numeric
            section_number = int(row["Section"]) if str(row["Section"]).isdigit() else row["Section"]
            seat_capacity = row["SeatCapacity"]

            # If this is the first time seeing this course, initialize its structure
            if course_name not in courses_json:
                courses_json[course_name] = {
                    "title": title,
                    "sections": []
                }

            # Append the section information
            courses_json[course_name]["sections"].append({
                "section_number": section_number,
                "seat_capacity": seat_capacity
            })

        return courses_json
    except sqlite3.Error as error:
        print(f"Error occurred while fetching courses: {error}")
        return {}
    finally:
        connection.close()
        print("Database connection closed.")


import sqlite3

def create_manually_scheduled_data():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    try:
        query = "SELECT Course, Section, Prof, Start, MeetingPattern, Room FROM CourseSchedule WHERE Type = 'MANUAL'"
        cursor.execute(query)
        rows = cursor.fetchall()
        key_mapping = {
            "Course": "course",
            "Section": "section",
            "Prof": "professor",
            "Start": "start",
            "MeetingPattern": "meeting_pattern",
            "Room": "room"
        }
        result = [
            {key_mapping[k]: v for k, v in dict(row).items()}
            for row in rows
        ]
        return result
    except sqlite3.Error as error:
        print(f"Error occurred: {error}")
        return []
    finally:
        connection.close()
        print("Database connection closed.")
    

def is_prof_available_for_time_slot(p, mp, period):
    professors = create_professors_data()
    return (mp, period) in professors[p]['availability']

def is_prof_available_and_qualified(p, c, ts):
    professors = create_professors_data()
    return int(ts in professors[p]['availability'] and c in professors[p]['qualified_courses'])

def run_scheduling_algorithm (
    days,
    meeting_patterns,
    professors,
    courses,
    rooms,
    manually_scheduled_classes,
    small_class_threshold=100,
    rush_hour_penalty=0,
    possible_meeting_patterns=['MWF', 'TTH', 'MW']
):
    # -----------------------------
    # Initialize Variables
    # -----------------------------
    if manually_scheduled_classes is None:
        manually_scheduled_classes = []

    # Create the LP problem (Maximize the number of classes scheduled)
    prob = pulp.LpProblem("Course_Scheduling_Problem", pulp.LpMaximize)

    # Create time slots specific to each meeting pattern
    time_slots_mp = {}
    for mp in meeting_patterns:
        mp_time_slots = []
        for period in meeting_patterns[mp]['periods'].keys():
            mp_time_slots.append((mp, period))
        time_slots_mp[mp] = mp_time_slots

    # Identify small and large classes based on seat capacity
    small_classes = []
    large_classes = []
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            seat_capacity = section['seat_capacity']
            if seat_capacity is not None:
                if seat_capacity >= small_class_threshold:
                    large_classes.append((c, s))
                else:
                    small_classes.append((c, s))

    # Generate all valid combinations of indices for x
    x_indices = []
    
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            seat_capacity = section['seat_capacity']
            for mp in possible_meeting_patterns:
                for period in meeting_patterns[mp]['periods'].keys():
                    ts = (mp, period)
                    for r in rooms.keys():
                        # Enforce large classes to use 'university' room only
                        if (c, s) in large_classes and r != 'university':
                            continue  # Skip this combination
                        # Enforce small classes not to use 'university' room
                        if (c, s) in small_classes and r == 'university':
                            continue  # Skip this combination
                        # Enforce room capacity constraints
                        if seat_capacity is not None and rooms[r]['capacity'] < seat_capacity:
                            continue  # Skip this combination
                        idx = (c, s, mp, period, r)
                        x_indices.append(idx)

    # Define the decision variables
    x = {}
    for idx in x_indices:
        var_name = "x_%s_%s_%s_%s_%s" % idx
        x[idx] = pulp.LpVariable(var_name, cat='Binary')

    y = {}
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            y[(c, s)] = pulp.LpVariable(f"y_{c}_{s}", cat='Binary')

    z = {}
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            for p in professors:
                if c in professors[p]['qualified_courses']:
                    z[(c, s, p)] = pulp.LpVariable(f"z_{c}_{s}_{p}", cat='Binary')

    # -----------------------------
    # Manually Scheduled Classes (Constraints)
    # -----------------------------
    # Process manually scheduled classes
    for entry in manually_scheduled_classes:
        c = entry['course']
        s = entry['section']
        # Ensure the class is scheduled
        prob += y[(c, s)] == 1, f"Manual_Class_Scheduled_{c}_{s}"

        # Fix professor assignment if specified
        if 'professor' in entry:
            p = entry['professor']
            # Ensure the professor is assigned to the class
            prob += z[(c, s, p)] == 1, f"Manual_Professor_Assigned_{c}_{s}_{p}"

        # Fix meeting pattern, period, and room if specified
        if 'meeting_pattern' in entry and 'period' in entry and 'room' in entry:
            mp = entry['meeting_pattern']
            period = entry['period']
            r = entry['room']
            idx = (c, s, mp, period, r)
            if idx in x:
                prob += x[idx] == 1, f"Manual_Schedule_{c}_{s}_{mp}_{period}_{r}"
            else:
                print(f"Warning: Invalid manual schedule for class {c} section {s}.")
        else:
            # Fix meeting pattern if specified
            if 'meeting_pattern' in entry:
                mp = entry['meeting_pattern']
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if idx[0] == c and idx[1] == s and idx[2] == mp
                ]) == y[(c, s)], f"Manual_Meeting_Pattern_{c}_{s}_{mp}"

            # Fix period if specified
            if 'period' in entry:
                period = entry['period']
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if idx[0] == c and idx[1] == s and idx[3] == period
                ]) == y[(c, s)], f"Manual_Period_{c}_{s}_{period}"

            # Fix room if specified
            if 'room' in entry:
                r = entry['room']
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if idx[0] == c and idx[1] == s and idx[4] == r
                ]) == y[(c, s)], f"Manual_Room_{c}_{s}_{r}"

    # -----------------------------
    # Constraints
    # -----------------------------

    # 1. Link x and y variables
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            prob += pulp.lpSum([
                x[idx]
                for idx in x_indices
                if idx[0] == c and idx[1] == s
            ]) == y[(c, s)], f"Link_x_y_{c}_{s}"

    # 2. Professors assigned to sections must be qualified and available
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            qualified_professors = [p for p in professors if c in professors[p]['qualified_courses']]
            prob += pulp.lpSum([
                z[(c, s, p)]
                for p in qualified_professors
            ]) == y[(c, s)], f"Prof_Assignment_{c}_{s}"

    # 3. Limit professors to maximum number of classes
    for p in professors:
        prob += pulp.lpSum([
            z[(c, s, p)]
            for c in courses
            for section in courses[c]['sections']
            for s in [section['section_number']]
            if (c, s, p) in z
        ]) <= professors[p]['max_classes'], f"Max_Classes_{p}"

    # 4. A professor cannot teach more than one class at the same time
    for p in professors:
        for mp in meeting_patterns:
            for period in meeting_patterns[mp]['periods']:
                constraint_name = f"Prof_Time_Conflict_{p}_{mp}_{period}"
                # Sum over all classes assigned to professor p at (mp, period)
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if (idx[0], idx[1], p) in z
                    and idx[2] == mp
                    and idx[3] == period
                ]) <= 1, constraint_name

    # 5a. If z[(c, s, p)] == 1, then x[idx] == 1 for some idx
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            for p in professors:
                if (c, s, p) in z:
                    constraint_name = f"Link_z_x_{c}_{s}_{p}"
                    
                    prob += pulp.lpSum([
                        x[idx]
                        for idx in x_indices
                        if idx[0] == c and idx[1] == s and is_prof_available_for_time_slot(p, idx[2], idx[3])
                    ]) >= z[(c, s, p)], constraint_name

    # 5b. If x[idx] == 1, then z[(c, s, p)] == 1 for some p
    for idx in x_indices:
        c, s, mp, period, r = idx
        constraint_name = f"Link_x_z_{c}_{s}_{mp}_{period}_{r}"
        
        prob += x[idx] <= pulp.lpSum([
            z[(c, s, p)]
            for p in professors
            if (c, s, p) in z and is_prof_available_for_time_slot(p, mp, period)
        ]), constraint_name

    # 6. Room capacity constraints (no double booking)
    # Collect all unique day-period combinations
    all_day_periods = set()
    for mp in meeting_patterns:
        days = meeting_patterns[mp]['days']
        periods = meeting_patterns[mp]['periods'].keys()
        for day in days:
            for period in periods:
                all_day_periods.add((day, period))

    # 6. Room capacity constraints (no double booking)
    for r in rooms:
        if r != 'university':
            for mp in meeting_patterns:
                for period in meeting_patterns[mp]['periods']:
                    constraint_name = f"Room_Capacity_{r}_{mp}_{period}"
                    prob += pulp.lpSum([
                        x[idx]
                        for idx in x_indices
                        if idx[4] == r
                        and idx[2] == mp
                        and idx[3] == period
                    ]) <= 1, constraint_name
    # 7. Room overlap constraints
    for r in rooms:
        for d in days:
            periods = sorted(meeting_patterns['MW']['periods'].keys())
            for p in periods:
                next_p = p + 1
                if next_p in meeting_patterns['MW']['periods'].keys():
                    current_ts = (d, p)
                    next_ts = (d, next_p)
                    mw_current = pulp.lpSum([
                        x[idx] for idx in x_indices
                        if idx[2] == 'MW' and idx[3] == current_ts and idx[4] == r
                    ])
                    mwf_next = pulp.lpSum([
                        x[idx] for idx in x_indices
                        if idx[2] == 'MWF' and idx[3] == next_ts and idx[4] == r
                    ])
                    mw_next = pulp.lpSum([
                        x[idx] for idx in x_indices
                        if idx[2] == 'MW' and idx[3] == next_ts and idx[4] == r
                    ])
                    prob += mw_current + mwf_next + mw_next <= 1, f"Room_Overlap_{r}_{d}_{p}"

    # 8. Rush-hour penalties and objective function
    rush_hour_time_slots = set()
    for mp in meeting_patterns:
        for day in meeting_patterns[mp]['days']:
            for period, info in meeting_patterns[mp]['periods'].items():
                start_time = info['start_time']
                # Convert start_time to minutes since midnight
                time_parts = start_time[:-2].split(':')
                hour = int(time_parts[0])
                minute = int(time_parts[1])
                am_pm = start_time[-2:]
                if am_pm == 'PM' and hour != 12:
                    hour += 12
                elif am_pm == 'AM' and hour == 12:
                    hour = 0
                start_minutes = hour * 60 + minute
                # Define rush-hour as 11:00 AM (660 minutes) to 2:00 PM (840 minutes)
                if 660 <= start_minutes < 840:
                    rush_hour_time_slots.add((day, period))

    # Identify x indices in rush-hour
    rush_hour_x_indices = [
        idx for idx in x_indices
        if idx[3] in rush_hour_time_slots
    ]

    # Define room costs
    room_cost = {}
    for idx in x_indices:
        c, s, mp, ts, r = idx
        if r == 'university' and (c, s) in small_classes:
            room_cost[idx] = 1  # Assign a penalty cost
        else:
            room_cost[idx] = 0

    # Modify the objective function
    prob += (
        pulp.lpSum([
            y[(c, s)]
            for c in courses
            for section in courses[c]['sections']
            for s in [section['section_number']]
        ])
        - pulp.lpSum([
            room_cost[idx] * x[idx]
            for idx in x_indices
        ])
        - rush_hour_penalty * pulp.lpSum([
            x[idx]
            for idx in rush_hour_x_indices
        ])
    ), "Objective_Function"

    # -----------------------------
    # Solve the Problem
    # -----------------------------
    prob.solve()

    # -----------------------------
    # Output the Schedule and Store Assignments
    # -----------------------------
    if pulp.LpStatus[prob.status] == 'Optimal':
        schedule = []
        unscheduled_classes = []
        assignment = {}  # Dictionary to store current assignments
        for c in courses:
            for section in courses[c]['sections']:
                s = section['section_number']
                if pulp.value(y[(c, s)]) == 1:
                    # Class is scheduled
                    assigned = False
                    for idx in x_indices:
                        if idx[0] == c and idx[1] == s and pulp.value(x[idx]) == 1:
                            c, s, mp, period, r = idx
                            section = next(sec for sec in courses[c]['sections'] if sec['section_number'] == s)
                            seat_capacity = section['seat_capacity']
                            # Find the assigned professor
                            assigned_professor = None
                            for p in professors:
                                if (c, s, p) in z and pulp.value(z[(c, s, p)]) == 1:
                                    assigned_professor = p
                                    break
                            days = meeting_patterns[mp]['days']
                            start_time = meeting_patterns[mp]['periods'][period]['start_time']
                            schedule.append({
                                'Course': c,
                                'Section': s,
                                'Title': courses[c]['title'],
                                'Professor': assigned_professor,
                                'Meeting Pattern': mp,
                                'Days': days,
                                'Period': period,
                                'Start Time': start_time,
                                'Room': r,
                                'Seat Capacity': seat_capacity
                            })
                            assignment[(c, s)] = idx  # Store the current assignment
                            assigned = True
                            break
                    if not assigned:
                        unscheduled_classes.append((c, s))
                else:
                    # Class is not scheduled
                    unscheduled_classes.append((c, s))

        # Initialize a dictionary to count classes assigned to each professor
        professor_class_counts = {p: 0 for p in professors}

        # Iterate over the assignment variables z to count classes
        for (c, s, p) in z:
            if pulp.value(z[(c, s, p)]) == 1:
                professor_class_counts[p] += 1

        # List of professors with no classes assigned
        professors_with_no_classes = [p for p, count in professor_class_counts.items() if count == 0]

        # Return the results
        result = {
            'schedule': schedule,
            'unscheduled_classes': unscheduled_classes,
            'professors_with_no_classes': professors_with_no_classes,
            'assignment': assignment,
            'prob_status': pulp.LpStatus[prob.status]
        }
        assignment_serializable = {str(k): list(v) if isinstance(v, tuple) else v for k, v in assignment.items()}
        result['assignment'] = assignment_serializable
        return result
    else:
        # No feasible solution found
        result = {
            'schedule': [],
            'unscheduled_classes': [],
            'professors_with_no_classes': [],
            'assignment': {},
            'prob_status': pulp.LpStatus[prob.status],
            'message': f"No feasible solution found. Solver Status: {pulp.LpStatus[prob.status]}"
        }
        return result