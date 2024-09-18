# Course Scheduling Program using PuLP

# Import PuLP library
import pulp
from collections import defaultdict

# -----------------------------
# Data Definitions
# -----------------------------

# Define days
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# Define periods with start times and durations (in minutes)
# For simplicity, we'll represent periods as integers

# MWF periods (50 minutes each)
mwf_periods = {
    1: {'start_time': '8:00AM', 'duration': 50},
    2: {'start_time': '9:05AM', 'duration': 50},
    3: {'start_time': '10:10AM', 'duration': 50},
    4: {'start_time': '11:15AM', 'duration': 50},
    5: {'start_time': '12:20PM', 'duration': 50},
    6: {'start_time': '1:25PM', 'duration': 50},
    7: {'start_time': '2:30PM', 'duration': 50},
    8: {'start_time': '3:35PM', 'duration': 50},
    9: {'start_time': '4:40PM', 'duration': 50},
    10: {'start_time': '5:45PM', 'duration': 50}
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
    2: {'start_time': '9:05AM', 'duration': 75},
    3: {'start_time': '10:10AM', 'duration': 75},
    4: {'start_time': '11:15AM', 'duration': 75},
    5: {'start_time': '12:20PM', 'duration': 75},
    6: {'start_time': '1:25PM', 'duration': 75},
    7: {'start_time': '2:30PM', 'duration': 75},
    8: {'start_time': '3:35PM', 'duration': 75},
    9: {'start_time': '4:40PM', 'duration': 75},
    10: {'start_time': '5:45PM', 'duration': 75}
}

# Define meeting patterns with their corresponding days and periods
meeting_patterns = {
    'MWF': {'days': ['Monday', 'Wednesday', 'Friday'], 'periods': mwf_periods},
    'TTH': {'days': ['Tuesday', 'Thursday'], 'periods': tth_periods},
    'MW': {'days': ['Monday', 'Wednesday'], 'periods': mw_periods}
}

# Create time slots: (day, period)
time_slots = []
for mp in meeting_patterns.values():
    for day in mp['days']:
        for period in mp['periods'].keys():
            time_slots.append((day, period))

# Professors with their qualifications and availability
# For this example, let's assume professors are available for all time slots
# You can customize this based on actual availability

professors = {
    'Prof_A': {
        'qualified_courses': ['COMP110'],
        'availability': time_slots  # Available for all time slots
    },
    'Prof_B': {
        'qualified_courses': ['COMP210'],
        'availability': time_slots
    },
    # Add other professors
}

# Courses with number of sections, title, and seat capacity
courses = {
    'COMP110': {
        'title': 'Introduction to Programming and Data Science',
        'sections': 3,
        'seat_capacity': 300
    },
    'COMP210': {
        'title': 'Data Structures and Analysis',
        'sections': 2,
        'seat_capacity': 210
    },
    # Add other courses
}

# Rooms with capacities
rooms = {
    'Room_A': {'capacity': 300},
    'Room_B': {'capacity': 210},
    # Add other rooms
}

# Possible meeting patterns for classes
possible_meeting_patterns = ['MWF', 'TTH', 'MW']

# -----------------------------
# Helper Functions
# -----------------------------

def is_time_slot_in_meeting_pattern(ts, mp):
    day, period = ts
    return day in meeting_patterns[mp]['days'] and period in meeting_patterns[mp]['periods']

def is_prof_available_and_qualified(p, c, ts):
    return int(ts in professors[p]['availability'] and c in professors[p]['qualified_courses'])

# -----------------------------
# ILP Model Setup
# -----------------------------

# Course Scheduling Program using PuLP

# Import PuLP library
import pulp
from collections import defaultdict

# -----------------------------
# Data Definitions
# -----------------------------

# (Data definitions remain the same as before)

# (Define days, periods, meeting_patterns, time_slots, professors, courses, rooms, possible_meeting_patterns)

# -----------------------------
# Helper Functions
# -----------------------------

def is_time_slot_in_meeting_pattern(ts, mp):
    day, period = ts
    return day in meeting_patterns[mp]['days'] and period in meeting_patterns[mp]['periods']

def is_prof_available_and_qualified(p, c, ts):
    return int(ts in professors[p]['availability'] and c in professors[p]['qualified_courses'])

# -----------------------------
# ILP Model Setup
# -----------------------------

# Create the LP problem
prob = pulp.LpProblem("Course_Scheduling_Problem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts(
    "x", (courses.keys(),
          [s for c in courses for s in range(courses[c]['sections'])],
          possible_meeting_patterns,
          time_slots,
          rooms.keys()),
    cat='Binary'
)

# -----------------------------
# Constraints
# -----------------------------

# 1. Each section must be assigned to one meeting pattern, time slot, and room
for c in courses:
    for s in range(courses[c]['sections']):
        prob += pulp.lpSum([
            x[c][s][mp][ts][r]
            for mp in possible_meeting_patterns
            for ts in time_slots
            for r in rooms
            if is_time_slot_in_meeting_pattern(ts, mp)
        ]) == 1

# 2. Professors assigned to sections must be qualified and available
for c in courses:
    for s in range(courses[c]['sections']):
        for mp in possible_meeting_patterns:
            for ts in time_slots:
                if is_time_slot_in_meeting_pattern(ts, mp):
                    for r in rooms:
                        # At least one qualified professor must be available
                        prob += pulp.lpSum([
                            is_prof_available_and_qualified(p, c, ts)
                            for p in professors
                        ]) >= x[c][s][mp][ts][r]

# 3. A professor cannot teach more than one class at the same time
for p in professors:
    for ts in time_slots:
        prob += pulp.lpSum([
            x[c][s][mp][ts][r]
            for c in professors[p]['qualified_courses']
            for s in range(courses[c]['sections'])
            for mp in possible_meeting_patterns
            for r in rooms
            if is_time_slot_in_meeting_pattern(ts, mp)
        ]) <= 1

# 4. A room cannot have more than one class at the same time
for r in rooms:
    for ts in time_slots:
        prob += pulp.lpSum([
            x[c][s][mp][ts][r]
            for c in courses
            for s in range(courses[c]['sections'])
            for mp in possible_meeting_patterns
            if is_time_slot_in_meeting_pattern(ts, mp)
        ]) <= 1

# 5. Room capacity must be sufficient for the course
for c in courses:
    for s in range(courses[c]['sections']):
        for mp in possible_meeting_patterns:
            for ts in time_slots:
                if is_time_slot_in_meeting_pattern(ts, mp):
                    for r in rooms:
                        if rooms[r]['capacity'] < courses[c]['seat_capacity']:
                            prob += x[c][s][mp][ts][r] == 0

# 6. Meeting patterns must align with time slots
for c in courses:
    for s in range(courses[c]['sections']):
        for mp in possible_meeting_patterns:
            for ts in time_slots:
                if not is_time_slot_in_meeting_pattern(ts, mp):
                    for r in rooms:
                        prob += x[c][s][mp][ts][r] == 0

# -----------------------------
# Objective Function
# -----------------------------

# Maximize the total number of classes scheduled
prob += pulp.lpSum([
    x[c][s][mp][ts][r]
    for c in courses
    for s in range(courses[c]['sections'])
    for mp in possible_meeting_patterns
    for ts in time_slots
    for r in rooms
    if is_time_slot_in_meeting_pattern(ts, mp)
])

# -----------------------------
# Solve the Problem
# -----------------------------

# Solve the problem
prob.solve()

# -----------------------------
# Output the Schedule
# -----------------------------

if pulp.LpStatus[prob.status] == 'Optimal':
    schedule = []
    for c in courses:
        for s in range(courses[c]['sections']):
            for mp in possible_meeting_patterns:
                for ts in time_slots:
                    if is_time_slot_in_meeting_pattern(ts, mp):
                        for r in rooms:
                            if pulp.value(x[c][s][mp][ts][r]) == 1:
                                # Find an available professor
                                assigned_professor = None
                                for p in professors:
                                    if is_prof_available_and_qualified(p, c, ts):
                                        assigned_professor = p
                                        break
                                day, period = ts
                                start_time = meeting_patterns[mp]['periods'][period]['start_time']
                                schedule.append({
                                    'Course': c,
                                    'Section': s + 1,
                                    'Title': courses[c]['title'],
                                    'Professor': assigned_professor,
                                    'Meeting Pattern': mp,
                                    'Day': day,
                                    'Period': period,
                                    'Start Time': start_time,
                                    'Room': r
                                })

    # Print the schedule
    for entry in schedule:
        print(f"Course: {entry['Course']} Section {entry['Section']}, Title: {entry['Title']}")
        print(f"  Professor: {entry['Professor']}")
        print(f"  Meeting Pattern: {entry['Meeting Pattern']}")
        print(f"  Day: {entry['Day']}, Period: {entry['Period']}, Start Time: {entry['Start Time']}")
        print(f"  Room: {entry['Room']}")
        print()
else:
    print("No feasible solution found. Solver Status:", pulp.LpStatus[prob.status])
