# Install PuLP if you haven't already
# !pip install pulp

import pulp

# Professors with their available times and qualified courses
professors = {
    'Prof_A': {
        'qualified_courses': ['CS101', 'CS102'],
        'availability': ['Monday_9', 'Monday_10', 'Wednesday_9'],
    },
    'Prof_B': {
        'qualified_courses': ['CS101', 'CS103'],
        'availability': ['Tuesday_9', 'Thursday_9'],
    },
    # Add other professors as needed
}

# Courses with the number of sections needed
courses = {
    'CS101': {
        'sections': 2,
        'time_blocks': ['Morning'],
    },
    'CS102': {
        'sections': 1,
        'time_blocks': ['Morning'],
    },
    'CS103': {
        'sections': 1,
        'time_blocks': ['Morning'],
    },
    # Add other courses as needed
}

# Rooms available
rooms = ['Room1', 'Room2']

# Time slots available
time_slots = ['Monday_9', 'Monday_10', 'Tuesday_9', 'Wednesday_9', 'Thursday_9']

# For simplicity, let's assume all time slots are 1-hour blocks
# Create the LP problem
prob = pulp.LpProblem("Course_Scheduling_Problem", pulp.LpMaximize)

# Decision variables
# x[p][c][t][r] = 1 if professor p teaches course c at time t in room r
x = pulp.LpVariable.dicts("x", (professors.keys(), courses.keys(), time_slots, rooms), cat='Binary')

# Objective function (e.g., maximize the number of scheduled classes)
prob += pulp.lpSum([x[p][c][t][r] for p in professors for c in courses for t in time_slots for r in rooms])

# Constraints

# 1. Each section of a course must be scheduled once
for c in courses:
    for s in range(courses[c]['sections']):
        prob += pulp.lpSum([x[p][c][t][r] for p in professors for t in time_slots for r in rooms]) == courses[c]['sections']

# 2. A professor can only teach one class at a time
for p in professors:
    for t in time_slots:
        prob += pulp.lpSum([x[p][c][t][r] for c in courses for r in rooms]) <= 1

# 3. A room can only have one class at a time
for r in rooms:
    for t in time_slots:
        prob += pulp.lpSum([x[p][c][t][r] for p in professors for c in courses]) <= 1

# 4. Professors can only teach courses they are qualified for
for p in professors:
    for c in courses:
        if c not in professors[p]['qualified_courses']:
            for t in time_slots:
                for r in rooms:
                    prob += x[p][c][t][r] == 0

# 5. Professors can only teach at times they are available
for p in professors:
    unavailable_times = set(time_slots) - set(professors[p]['availability'])
    for t in unavailable_times:
        for c in courses:
            for r in rooms:
                prob += x[p][c][t][r] == 0

# 6. Courses can only be scheduled in their allowed time blocks
# Assuming 'Morning' time block corresponds to all time slots in our example
# If you have specific time blocks, you can add constraints accordingly

# Solve the problem
prob.solve()
from collections import defaultdict

# Check if a feasible solution was found
if pulp.LpStatus[prob.status] == 'Optimal':
    schedule = defaultdict(list)  # Keyed by time slot
    for p in professors:
        for c in courses:
            for t in time_slots:
                for r in rooms:
                    if pulp.value(x[p][c][t][r]) == 1:
                        schedule[t].append({
                            'Professor': p,
                            'Course': c,
                            'Room': r
                        })
    # Format and print the schedule
    for t in sorted(schedule):
        print(f"Time Slot: {t}")
        for entry in schedule[t]:
            print(f"  Course: {entry['Course']}, Professor: {entry['Professor']}, Room: {entry['Room']}")
        print()
else:
    print("No feasible solution found.")
