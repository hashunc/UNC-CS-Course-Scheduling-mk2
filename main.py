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
    'Montek Singh': {
        'qualified_courses': ['COMP541', 'COMP572'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Kurt M. Potter': {
        'qualified_courses': ['COMP301', 'COMP426'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Muhammad Ghani': {
        'qualified_courses': ['COMP210'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Praveen Kumar': {
        'qualified_courses': ['COMP455'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Jasleen Kaur': {
        'qualified_courses': ['COMP431'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Saba Eskandarian': {
        'qualified_courses': ['COMP537', 'COMP455', 'COMP435', 'COMP590', 'COMP790'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Ron Alterovitz': {
        'qualified_courses': ['COMP581', 'COMP781', 'COMP782'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Cynthia Sturton': {
        'qualified_courses': ['COMP435'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Marc Niethammer': {
        'qualified_courses': ['COMP775'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Samarjit Chakraborty': {
        'qualified_courses': ['COMP545', 'COMP790'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Donald Porter': {
        'qualified_courses': ['COMP530'],
        'availability': time_slots,
        'max_classes': 2
    },
    'John Majikes': {
        'qualified_courses': ['COMP421', 'COMP550', 'COMP116'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Alyssa Byrnes': {
        'qualified_courses': ['COMP110', 'COMP116', 'COMP210', 'COMP283'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Gedas Bertasius': {
        'qualified_courses': ['COMP590', 'COMP790'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Roni Sengupta': {
        'qualified_courses': ['COMP590'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Kangning Sun': {
        'qualified_courses': ['COMP283', 'COMP455', 'COMP550'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Cece McMahon': {
        'qualified_courses': ['COMP311', 'COMP541'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Shahriar Nirjon': {
        'qualified_courses': ['COMP433'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Jack Snoeyink': {
        'qualified_courses': ['COMP283', 'DATA140'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Brent Munsell': {
        'qualified_courses': ['COMP211', 'COMP590', 'COMP530', 'COMP311', 'COMP116'],
        'availability': time_slots,
        'max_classes': 2
    },
    'James Anderson': {
        'qualified_courses': ['COMP737', 'COMP750'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Danielle Szafir': {
        'qualified_courses': ['COMP790'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Daniel Szafir': {
        'qualified_courses': ['COMP581'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Praneeth Chakravarthula': {
        'qualified_courses': ['COMP089', 'COMP790'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Ben Lee': {
        'qualified_courses': ['COMP790'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Shubhra Srivastava': {
        'qualified_courses': ['COMP664'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Chase P. Kline': {
        'qualified_courses': ['COMP790'],
        'availability': time_slots,
        'max_classes': 2
    }
}



# Courses with number of sections, title, and seat capacity
courses = {
    'COMP110': {
        'title': 'COMP110 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 300},
            {'section_number': 2, 'seat_capacity': 300},
            {'section_number': 3, 'seat_capacity': 150},
            {'section_number': 4, 'seat_capacity': 150}
        ]
    },
    'COMP116': {
        'title': 'COMP116 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': None}
        ]
    },
    'COMP126': {
        'title': 'COMP126 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 120}
        ]
    },
    'COMP210': {
        'title': 'COMP210 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 210},
            {'section_number': 2, 'seat_capacity': 210}
        ]
    },
    'COMP211': {
        'title': 'COMP211 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 200},
            {'section_number': 2, 'seat_capacity': 200}
        ]
    },
    'COMP227': {
        'title': 'COMP227 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 30}
        ]
    },
    'COMP283': {
        'title': 'COMP283 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 180}
        ]
    },
    'COMP283H': {
        'title': 'COMP283H Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 24}
        ]
    },
    'COMP301': {
        'title': 'COMP301 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 200},
            {'section_number': 2, 'seat_capacity': 200}
        ]
    },
    'COMP311': {
        'title': 'COMP311 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 225}
        ]
    },
    'COMP380': {
        'title': 'COMP380 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 60}
        ]
    },
    'COMP380H': {
        'title': 'COMP380H Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 24}
        ]
    },
    'COMP421': {
        'title': 'COMP421 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 200}  # Assuming maximum capacity
        ]
    },
    'COMP426': {
        'title': 'COMP426 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 200}  # Assuming maximum capacity
        ]
    },
    'COMP431': {
        'title': 'COMP431 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 60}
        ]
    },
    'COMP433': {
        'title': 'COMP433 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 75}
        ]
    },
    'COMP435': {
        'title': 'COMP435 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 70}
        ]
    },
    'COMP455': {
        'title': 'COMP455 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 125},
            {'section_number': 2, 'seat_capacity': 125}
        ]
    },
    'COMP475': {
        'title': 'COMP475 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 60}
        ]
    },
    'COMP488': {
        'title': 'COMP488 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': None}
        ]
    },
    'COMP520': {
        'title': 'COMP520 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': None}
        ]
    },
    'COMP523': {
        'title': 'COMP523 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 60}
        ]
    },
    'COMP524': {
        'title': 'COMP524 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 60}
        ]
    },
    'COMP530': {
        'title': 'COMP530 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 75}
        ]
    },
    'COMP533': {
        'title': 'COMP533 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': None}
        ]
    },
    'COMP537': {
        'title': 'COMP537 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 90}
        ]
    },
    'COMP541': {
        'title': 'COMP541 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 45},
            {'section_number': 2, 'seat_capacity': 45}
        ]
    },
    'COMP545': {
        'title': 'COMP545 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 25}
        ]
    },
    'COMP550': {
        'title': 'COMP550 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 125},
            {'section_number': 2, 'seat_capacity': 125}
        ]
    },
    'COMP560': {
        'title': 'COMP560 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 60}
        ]
    },
    'COMP562': {
        'title': 'COMP562 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 75}
        ]
    },
    'COMP581': {
        'title': 'COMP581 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 60}
        ]
    },
    'COMP590': {
        'title': 'COMP590 Class',
        'sections': [
            {'section_number': 59, 'seat_capacity': 90},
            {'section_number': 139, 'seat_capacity': 10},
            {'section_number': 140, 'seat_capacity': 280},
            {'section_number': 158, 'seat_capacity': 4},
            {'section_number': 170, 'seat_capacity': 30},
            {'section_number': 172, 'seat_capacity': 30},
            {'section_number': 177, 'seat_capacity': 60}
        ]
    },
    'COMP730': {
        'title': 'COMP730 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': None}
        ]
    },
    'COMP664': {
        'title': 'COMP664 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 60}
        ]
    },
    'COMP737': {
        'title': 'COMP737 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 30}
        ]
    },
    'COMP750': {
        'title': 'COMP750 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 30}
        ]
    },
    'COMP755': {
        'title': 'COMP755 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 30}
        ]
    },
    'COMP775': {
        'title': 'COMP775 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 30}
        ]
    },
    'COMP790': {
        'title': 'COMP790 Class',
        'sections': [
            {'section_number': 139, 'seat_capacity': 20},
            {'section_number': 144, 'seat_capacity': 30},
            {'section_number': 148, 'seat_capacity': 25},
            {'section_number': 158, 'seat_capacity': 21},
            {'section_number': 170, 'seat_capacity': 30},
            {'section_number': 172, 'seat_capacity': 30},
            {'section_number': 173, 'seat_capacity': 30},
            {'section_number': 175, 'seat_capacity': 30},
            {'section_number': 178, 'seat_capacity': 20},
            {'section_number': 183, 'seat_capacity': 30},
            {'section_number': 185, 'seat_capacity': 30}
        ]
    },
    'COMP915': {
        'title': 'COMP915 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': None}
        ]
    }
}

# Rooms with capacities
rooms = {
    'SN-0014': {'capacity': 128},
    'FB-F009': {'capacity': 86},
    'SN-0011': {'capacity': 66},
    'FB-F007': {'capacity': 50},
    'FB-F141': {'capacity': 50},
    'SN-0115': {'capacity': 25},
    'FB-F008': {'capacity': 20},
    'SN-0252': {'capacity': 20},
    'SN-0006': {'capacity': 15},
    'SN-0325': {'capacity': 15},
    'SN-0155': {'capacity': 14},
    'FB-F120': {'capacity': 12},
    'SN-0277': {'capacity': 10},
    'FB-F331': {'capacity': 16},
    'university': {'capacity': 300}  # Special room
}


# Possible meeting patterns for classes
possible_meeting_patterns = ['MWF', 'TTH', 'MW']

# -----------------------------
# Helper Functions
# -----------------------------


# Import PuLP library
import pulp
from collections import defaultdict


def is_prof_available_and_qualified(p, c, ts):
    return int(ts in professors[p]['availability'] and c in professors[p]['qualified_courses'])

# -----------------------------
# ILP Model Setup
# -----------------------------

# Create the LP problem (Maximize the number of classes scheduled)
prob = pulp.LpProblem("Course_Scheduling_Problem", pulp.LpMaximize)

# Create time slots specific to each meeting pattern
time_slots = {}
for mp in meeting_patterns:
    mp_time_slots = []
    for day in meeting_patterns[mp]['days']:
        for period in meeting_patterns[mp]['periods'].keys():
            mp_time_slots.append((day, period))
    time_slots[mp] = mp_time_slots

# Identify small and large classes based on seat capacity
small_classes = []
large_classes = []
for c in courses:
    for section in courses[c]['sections']:
        s = section['section_number']
        seat_capacity = section['seat_capacity']
        if seat_capacity is not None:
            if seat_capacity > 100:
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
            for ts in time_slots[mp]:
                for r in rooms.keys():
                    # Enforce large classes to use 'university' room only
                    if (c, s) in large_classes and r != 'university':
                        continue  # Skip this combination
                    # Enforce room capacity constraints
                    if seat_capacity is not None and rooms[r]['capacity'] < seat_capacity:
                        continue  # Skip this combination
                    idx = (c, s, mp, ts, r)
                    x_indices.append(idx)

# Define the decision variables
x = {}
for idx in x_indices:
    var_name = "x_%s_%s_%s_%s_%s" % idx
    x[idx] = pulp.LpVariable(var_name, cat='Binary')

# Define binary variables for class scheduling
y = {}
for c in courses:
    for section in courses[c]['sections']:
        s = section['section_number']
        y[(c, s)] = pulp.LpVariable(f"y_{c}_{s}", cat='Binary')

# Define binary variables for professor assignments
z = {}
for c in courses:
    for section in courses[c]['sections']:
        s = section['section_number']
        for p in professors:
            if c in professors[p]['qualified_courses']:
                z[(c, s, p)] = pulp.LpVariable(f"z_{c}_{s}_{p}", cat='Binary')

# -----------------------------
# Constraints
# -----------------------------

# 1. Link x and y variables: If a class is scheduled (y=1), it must be assigned to one meeting pattern, time slot, and room
for c in courses:
    for section in courses[c]['sections']:
        s = section['section_number']
        prob += pulp.lpSum([
            x[idx]
            for idx in x_indices
            if idx[0] == c and idx[1] == s
        ]) == y[(c, s)]

# 2. Professors assigned to sections must be qualified and available
for c in courses:
    for section in courses[c]['sections']:
        s = section['section_number']
        qualified_professors = [p for p in professors if c in professors[p]['qualified_courses']]
        prob += pulp.lpSum([
            z[(c, s, p)]
            for p in qualified_professors
        ]) == y[(c, s)]

# 3. Limit professors to maximum number of classes
for p in professors:
    prob += pulp.lpSum([
        z[(c, s, p)]
        for c in courses
        for section in courses[c]['sections']
        for s in [section['section_number']]
        if (c, s, p) in z
    ]) <= professors[p]['max_classes']

# Constraint 4: A professor cannot teach more than one class at the same time
for p in professors:
    for ts in professors[p]['availability']:
        prob += pulp.lpSum([
            x[idx]
            for idx in x_indices
            if idx[3] == ts and (idx[0], idx[1], p) in z
        ]) <= 1

# Constraint 5: Link x and z variables
# a) If z[(c, s, p)] == 1, then x[idx] == 1 for some idx
for c in courses:
    for section in courses[c]['sections']:
        s = section['section_number']
        for p in professors:
            if (c, s, p) in z:
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if idx[0] == c and idx[1] == s and idx[3] in professors[p]['availability']
                ]) >= z[(c, s, p)]
# b) If x[idx] == 1, then z[(c, s, p)] == 1 for some p
for idx in x_indices:
    c, s, mp, ts, r = idx
    prob += x[idx] <= pulp.lpSum([
        z[(c, s, p)]
        for p in professors
        if (c, s, p) in z and ts in professors[p]['availability']
    ])

for r in rooms:
    if r != 'university':
        for mp in possible_meeting_patterns:
            for ts in time_slots[mp]:
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if idx[4] == r and idx[3] == ts
                ]) <= 1
# -----------------------------
# Objective Function
# -----------------------------

# Objective Function: Maximize the number of classes scheduled
prob += pulp.lpSum([
    y[(c, s)]
    for c in courses
    for section in courses[c]['sections']
    for s in [section['section_number']]
])

# -----------------------------
# Solve the Problem
# -----------------------------

prob.solve()

# -----------------------------
# Output the Schedule
# -----------------------------

if pulp.LpStatus[prob.status] == 'Optimal':
    schedule = []
    unscheduled_classes = []
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            if pulp.value(y[(c, s)]) == 1:
                # Class is scheduled
                # Find the scheduled time slot and room
                assigned = False
                for idx in x_indices:
                    if idx[0] == c and idx[1] == s and pulp.value(x[idx]) == 1:
                        c, s, mp, ts, r = idx
                        section = next(sec for sec in courses[c]['sections'] if sec['section_number'] == s)
                        seat_capacity = section['seat_capacity']
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
                            'Section': s,
                            'Title': courses[c]['title'],
                            'Professor': assigned_professor,
                            'Meeting Pattern': mp,
                            'Day': day,
                            'Period': period,
                            'Start Time': start_time,
                            'Room': r,
                            'Seat Capacity': seat_capacity
                        })
                        assigned = True
                        break
                if not assigned:
                    unscheduled_classes.append((c, s))
            else:
                # Class is not scheduled
                unscheduled_classes.append((c, s))

    # Print the schedule
    for entry in schedule:
        print(f"Course: {entry['Course']} Section {entry['Section']}, Title: {entry['Title']}")
        print(f"  Professor: {entry['Professor']}")
        print(f"  Meeting Pattern: {entry['Meeting Pattern']}")
        print(f"  Day: {entry['Day']}, Period: {entry['Period']}, Start Time: {entry['Start Time']}")
        print(f"  Room: {entry['Room']}")
        print(f"  Seat Capacity: {entry['Seat Capacity']}")
        print()
    
    # Print unscheduled classes
    if unscheduled_classes:
        print("Unscheduled Classes:")
        for c, s in unscheduled_classes:
            print(f"Course: {c}, Section: {s}, Title: {courses[c]['title']}")
else:
    print("No feasible solution found. Solver Status:", pulp.LpStatus[prob.status])