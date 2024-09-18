# Course Scheduling Program using PuLP

# Import PuLP library
import pulp
from collections import defaultdict

# -----------------------------
# Data Definitions
# -----------------------------

# Define M/W/F periods
mwf_periods = {
    'Period_1': '8:00 – 8:50 a.m.',
    'Period_2': '9:05 – 9:55 a.m.',
    'Period_3': '10:10 – 11:00 a.m.',
    'Period_4': '11:15 – 12:05 p.m.',
    'Period_5': '12:20 – 1:10 p.m.',
    'Period_6': '1:25 – 2:15 p.m.',
    'Period_7': '2:30 – 3:20 p.m.',
    'Period_8': '3:35 – 4:25 p.m.',
    'Period_9': '4:40 – 5:30 p.m.',
    'Period_10': '5:45 – 6:35 p.m.'
}

# Define T/TH periods
tth_periods = {
    'Period_1': '8:00 – 9:15 a.m.',
    'Period_2': '9:30 – 10:45 a.m.',
    'Period_3': '11:00 – 12:15 p.m.',
    'Period_4': '12:30 – 1:45 p.m.',
    'Period_5': '2:00 – 3:15 p.m.',
    'Period_6': '3:30 – 4:45 p.m.',
    'Period_7': '5:00 – 6:15 p.m.'
}

# Create time slots combining days and periods
time_slots = []

# For M/W/F
for day in ['Monday', 'Wednesday', 'Friday']:
    for period in mwf_periods:
        time_slots.append(f"{day}_{period}")

# For T/TH
for day in ['Tuesday', 'Thursday']:
    for period in tth_periods:
        time_slots.append(f"{day}_{period}")

# Define meeting patterns
meeting_patterns = {
    'MWF_Period_1': ['Monday_Period_1', 'Wednesday_Period_1', 'Friday_Period_1'],
    'MWF_Period_2': ['Monday_Period_2', 'Wednesday_Period_2', 'Friday_Period_2'],
    'MWF_Period_3': ['Monday_Period_3', 'Wednesday_Period_3', 'Friday_Period_3'],
    'MWF_Period_4': ['Monday_Period_4', 'Wednesday_Period_4', 'Friday_Period_4'],
    'MWF_Period_5': ['Monday_Period_5', 'Wednesday_Period_5', 'Friday_Period_5'],
    'MWF_Period_6': ['Monday_Period_6', 'Wednesday_Period_6', 'Friday_Period_6'],
    'MWF_Period_7': ['Monday_Period_7', 'Wednesday_Period_7', 'Friday_Period_7'],
    'MWF_Period_8': ['Monday_Period_8', 'Wednesday_Period_8', 'Friday_Period_8'],
    'MWF_Period_9': ['Monday_Period_9', 'Wednesday_Period_9', 'Friday_Period_9'],
    'MWF_Period_10': ['Monday_Period_10', 'Wednesday_Period_10', 'Friday_Period_10'],
    'TTH_Period_1': ['Tuesday_Period_1', 'Thursday_Period_1'],
    'TTH_Period_2': ['Tuesday_Period_2', 'Thursday_Period_2'],
    'TTH_Period_3': ['Tuesday_Period_3', 'Thursday_Period_3'],
    'TTH_Period_4': ['Tuesday_Period_4', 'Thursday_Period_4'],
    'TTH_Period_5': ['Tuesday_Period_5', 'Thursday_Period_5'],
    'TTH_Period_6': ['Tuesday_Period_6', 'Thursday_Period_6'],
    'TTH_Period_7': ['Tuesday_Period_7', 'Thursday_Period_7']
}

# Professors with their qualifications and availability
professors = {
    'Prof_A': {
        'qualified_courses': ['CS101', 'CS102'],
        'availability': [
            'Monday_Period_1', 'Wednesday_Period_1', 'Friday_Period_1',
            'Monday_Period_2', 'Wednesday_Period_2', 'Friday_Period_2',
            'Tuesday_Period_1', 'Thursday_Period_1'
        ],
        # Preferences can be added here
    },
    'Prof_B': {
        'qualified_courses': ['CS101', 'CS103'],
        'availability': [
            'Tuesday_Period_1', 'Thursday_Period_1',
            'Tuesday_Period_2', 'Thursday_Period_2',
            'Monday_Period_3', 'Wednesday_Period_3', 'Friday_Period_3'
        ],
    },
    # Add other professors as needed
}

# Courses with the number of sections and meeting patterns
courses = {
    'CS101': {
        'sections': 2,
        'meeting_pattern': 'MWF',
    },
    'CS102': {
        'sections': 1,
        'meeting_pattern': 'TTH',
    },
    'CS103': {
        'sections': 1,
        'meeting_pattern': 'MWF',
    },
    # Add other courses as needed
}

# Rooms available
rooms = ['Room1', 'Room2']

# -----------------------------
# ILP Model Setup
# -----------------------------

# Create the LP problem
prob = pulp.LpProblem("Course_Scheduling_Problem", pulp.LpMaximize)

# Decision variables
# x[p][c][t][r] = 1 if professor p teaches course c at time t in room r
x = pulp.LpVariable.dicts(
    "x", (professors.keys(), courses.keys(), time_slots, rooms), cat='Binary'
)

# Objective function: Maximize the number of scheduled classes (you can adjust this)
prob += pulp.lpSum([
    x[p][c][t][r] for p in professors for c in courses for t in time_slots for r in rooms
])

# -----------------------------
# Constraints
# -----------------------------

# 1. Each section of a course must be scheduled once
for c in courses:
    prob += pulp.lpSum([
        x[p][c][t][r] for p in professors for t in time_slots for r in rooms
    ]) == courses[c]['sections']

# 2. Professors can only teach courses they're qualified for
for p in professors:
    for c in courses:
        if c not in professors[p]['qualified_courses']:
            for t in time_slots:
                for r in rooms:
                    prob += x[p][c][t][r] == 0

# 3. Professors can only teach at times they're available
for p in professors:
    unavailable_times = set(time_slots) - set(professors[p]['availability'])
    for t in unavailable_times:
        for c in courses:
            for r in rooms:
                prob += x[p][c][t][r] == 0

# 4. A professor cannot teach more than one class at the same time
for p in professors:
    for t in time_slots:
        prob += pulp.lpSum([
            x[p][c][t][r] for c in courses for r in rooms
        ]) <= 1

# 5. A room cannot have more than one class at the same time
for r in rooms:
    for t in time_slots:
        prob += pulp.lpSum([
            x[p][c][t][r] for p in professors for c in courses
        ]) <= 1

# 6. Room scheduling constraint for meeting patterns
for r in rooms:
    for mp, slots in meeting_patterns.items():
        prob += pulp.lpSum([
            x[p][c][t][r]
            for p in professors
            for c in courses
            for t in slots
            if courses[c]['meeting_pattern'] in mp
        ]) <= 1

# 7. Courses can only be scheduled in their designated meeting patterns
for c in courses:
    allowed_slots = []
    for mp, slots in meeting_patterns.items():
        if courses[c]['meeting_pattern'] in mp:
            allowed_slots.extend(slots)
    disallowed_slots = set(time_slots) - set(allowed_slots)
    for t in disallowed_slots:
        for p in professors:
            for r in rooms:
                prob += x[p][c][t][r] == 0

# 8. Even distribution of classes across time slots (optional)
total_classes = sum([courses[c]['sections'] for c in courses])
total_time_slots = len(time_slots)
desired_classes_per_slot = total_classes / total_time_slots

for t in time_slots:
    prob += pulp.lpSum([
        x[p][c][t][r] for p in professors for c in courses for r in rooms
    ]) <= desired_classes_per_slot + 1  # Adjust the buffer as needed

# -----------------------------
# Solve the Problem
# -----------------------------

# Solve the problem
prob.solve()

# -----------------------------
# Output the Schedule
# -----------------------------

# -----------------------------
# Output the Schedule
# -----------------------------

if pulp.LpStatus[prob.status] == 'Optimal':
    schedule = defaultdict(list)
    for p in professors:
        for c in courses:
            for t in time_slots:
                for r in rooms:
                    if pulp.value(x[p][c][t][r]) == 1:
                        schedule[t].append({
                            'Course': c,
                            'Professor': p,
                            'Room': r
                        })

    # Print the time slots for debugging
    print("Time Slots in Schedule:")
    for ts in schedule.keys():
        print(f"'{ts}'")

    # Sort the time slots with error handling
    def sort_key(x):
        try:
            day = x.split('_')[0]
            day_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].index(day)
            period_part = x.split('_')[1]
            period_number = int(period_part.split('Period_')[1])
            return (day_index, period_number)
        except (IndexError, ValueError):
            # Handle unexpected formats by assigning them a lower priority in sorting
            return (999, 999)

    sorted_time_slots = sorted(schedule.keys(), key=sort_key)

    # Print the schedule
    for t in sorted_time_slots:
        if schedule[t]:
            print(f"Time Slot: {t}")
            for entry in schedule[t]:
                print(f"  Course: {entry['Course']}, Professor: {entry['Professor']}, Room: {entry['Room']}")
            print()
else:
    print("No feasible solution found. Solver Status:", pulp.LpStatus[prob.status])
