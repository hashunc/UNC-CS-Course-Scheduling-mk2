# Course Scheduling Program using PuLP

# Import PuLP library
import pulp
from collections import defaultdict

# -----------------------------
# Data Definitions
# -----------------------------

# Define days
days = ['Monday', 'Tuesday', 'Wednesday']

# Define periods with start times and durations (in minutes)
# For simplicity, we'll represent periods as integers

# MWF periods (50 minutes each)
mwf_periods = {
    1: {'start_time': '8:00AM', 'duration': 50, 'end_time': '8:50AM'},
    2: {'start_time': '9:05AM', 'duration': 50, 'end_time': '9:55AM'},
    3: {'start_time': '10:10AM', 'duration': 50, 'end_time': '11:00AM'},
    4: {'start_time': '11:15AM', 'duration': 50, 'end_time': '12:05PM'},
    5: {'start_time': '12:20PM', 'duration': 50, 'end_time': '1:10PM'},
    6: {'start_time': '1:25PM', 'duration': 50, 'end_time': '2:15PM'},
    7: {'start_time': '2:30PM', 'duration': 50, 'end_time': '3:20PM'},
    8: {'start_time': '3:35PM', 'duration': 50, 'end_time': '4:25PM'},
}

# TTH periods (75 minutes each)
tth_periods = {
    1: {'start_time': '8:00AM', 'duration': 75, 'end_time': '9:15AM'},
    2: {'start_time': '9:30AM', 'duration': 75, 'end_time': '10:45AM'},
    3: {'start_time': '11:00AM', 'duration': 75, 'end_time': '12:15PM'},
    4: {'start_time': '12:30PM', 'duration': 75, 'end_time': '1:45PM'},
    5: {'start_time': '2:00PM', 'duration': 75, 'end_time': '3:15PM'},
    6: {'start_time': '3:30PM', 'duration': 75, 'end_time': '4:45PM'},
    7: {'start_time': '5:00PM', 'duration': 75, 'end_time': '6:15PM'}
}

# MW periods (75 minutes each)
mw_periods = {
    1: {'start_time': '8:00AM', 'duration': 75, 'end_time': '9:15AM'},
    3: {'start_time': '10:10AM', 'duration': 75, 'end_time': '11:25AM'},
    5: {'start_time': '12:20PM', 'duration': 75, 'end_time': '1:35PM'},
    7: {'start_time': '2:30PM', 'duration': 75, 'end_time': '3:45PM'},
}



# Define meeting patterns with their corresponding days and periods
meeting_patterns = {
    'MWF': {'days': ['Monday', 'Wednesday', "Friday"], 'periods': mwf_periods},
    'TTH': {'days': ['Tuesday', 'Thursday'], 'periods': tth_periods},
    'MW': {'days': ['Monday', "Wednesday"], 'periods': mw_periods},
    #'WF': {'days': ['Wednesday', 'Friday'], 'periods': wf_periods}
}

# Create time slots: (day, period)
time_slots = []
for mp in meeting_patterns.values():
    for day in mp['days']:
        for period in mp['periods'].keys():
            time_slots.append((day, period))
print(time_slots)

# Create time slots specific to each meeting pattern
def get_time_slots(mp):
    periods = sorted(meeting_patterns[mp]['periods'].keys())
    time_slots = [(mp, period) for period in periods]
    return time_slots

# Generate time slots for each meeting pattern
mwf= get_time_slots('MWF')
th = get_time_slots('TTH')
mw = get_time_slots('MW')


def is_prof_available_for_time_slot(p, mp, period):
    return (mp, period) in professors[p]['availability']






# Union of all availability
all_availability = mwf + th + mw

# Professors with their qualifications and availability
# For this example, let's assume professors are available for all time slots
# You can customize this based on actual availability

print(mwf)
print(th)
print(mw)

professors = {
    'Montek Singh': {
        'qualified_courses': ['COMP541', 'COMP572'],
        'availability': th,  # Changed from time_slots to th
        'max_classes': 1
    },
    'Tessa Joseph-Nicholas': {
        'qualified_courses': ['COMP126', "COMP380", "COMP380H"],
        'availability': mwf[0],  # Changed from time_slots to mwf
        'max_classes': 3
    },
    'Ketan Mayer-Patel': {
        'qualified_courses': ['COMP301', 'COMP426'],
        'availability': mw,  # Changed from time_slots to mw
        'max_classes': 1
    },
    'Prairie Goodwin': {
        'qualified_courses': ['COMP301'],
        'availability': all_availability,  # No change
        'max_classes': 2
    },
    'Sayeed Ghani': {
        'qualified_courses': ['COMP210'],
        'availability': th,  # Changed from all_availability to th
        'max_classes': 2
    },
    'P.S. Thiagarajan': {
        'qualified_courses': ['COMP455'],
        'availability': all_availability,  # No change
        'max_classes': 2
    },
    'Jasleen Kaur': {
        'qualified_courses': ['COMP431'],
        'availability': mwf[0],  # Changed from time_slots to mwf
        'max_classes': 0
    },
    'Saba Eskandarian': {
        'qualified_courses': ['COMP537', 'COMP455', 'COMP435', 'COMP590', 'COMP790'],
        'availability': all_availability,  # No change
        'max_classes': 1
    },
    'Ron Alterovitz': {
        'qualified_courses': ['COMP581', 'COMP781', 'COMP782'],
        'availability': mw,  # Changed from time_slots to mw
        'max_classes': 1
    },
    'Cynthia Sturton': {
        'qualified_courses': ['COMP435'],
        'availability': all_availability,  # No change
        'max_classes': 1
    },
    'Marc Niethammer': {
        'qualified_courses': ['COMP775'],
        'availability': th,  # Changed from time_slots to th
        'max_classes': 1
    },
    'Izzi Hinks': {
        'qualified_courses': ['COMP110'],
        'availability': all_availability,  # No change
        'max_classes': 2
    },
    'Samarjit Chakraborty': {
        'qualified_courses': ['COMP545', 'COMP790-148'],
        'availability': mwf,  # Changed from time_slots to mwf
        'max_classes': 2
    },
    'Donald Porter': {
        'qualified_courses': ['COMP530'],
        'availability': mwf,  # No change
        'max_classes': 1
    },
    'John Majikes': {
        'qualified_courses': ['COMP421', 'COMP550', 'COMP116'],
        'availability': mw,  # Changed from time_slots to mw
        'max_classes': 2
    },
    'Alyssa Byrnes': {
        'qualified_courses': ['COMP110', 'COMP116', 'COMP210', 'COMP283'],
        'availability': all_availability,  # No change
        'max_classes': 2
    },
    'Gedas Bertasius': {
        'qualified_courses': ['COMP790-170'],
        'availability': th,  # Changed from time_slots to th
        'max_classes': 1
    },
    'Roni Sengupta': {
        'qualified_courses': ['COMP590-177'],
        'availability': all_availability,  # No change
        'max_classes': 1
    },
    'Kevin Sun': {
        'qualified_courses': ['COMP283', 'COMP455', 'COMP550'],
        'availability': [('MW', 3)],  # Changed from time_slots to mwf
        'max_classes': 2
    },
    'Cece McMahon': {
        'qualified_courses': ['COMP311', 'COMP541'],
        'availability': all_availability,  # No change
        'max_classes': 2
    },
    'Shahriar Nirjon': {
        'qualified_courses': ['COMP433'],
        'availability': th[4:5],  # Changed from time_slots to th
        'max_classes': 1
    },
    'Jack Snoeyink': {
        'qualified_courses': ['COMP283', 'DATA140'],
        'availability': all_availability,  # No change
        'max_classes': 1
    },
    'Brent Munsell': {
        'qualified_courses': ['COMP211', 'COMP590', 'COMP530', 'COMP311', 'COMP116'],
        'availability': mw,  # Changed from time_slots to mw
        'max_classes': 2
    },
    'James Anderson': {
        'qualified_courses': ['COMP737', 'COMP750'],
        'availability': all_availability,  # No change
        'max_classes': 2
    },
    'Danielle Szafir': {
        'qualified_courses': ['COMP790-172'],
        'availability': mwf,  # Changed from time_slots to mwf
        'max_classes': 1
    },
    'Daniel Szafir': {
        'qualified_courses': ['COMP581'],
        'availability': all_availability,  # No change
        'max_classes': 1
    },
    'Parasara Sridhar Duggirala': {
        'qualified_courses': ['COMP089', 'COMP790-144'],
        'availability': all_availability,  # No change
        'max_classes': 1
    },
    'Praneeth Chakravarthula': {
        'qualified_courses': ['COMP790-175'],
        'availability': th,  # Changed from time_slots to th
        'max_classes': 1
    },
    'Ben Berg': {
        'qualified_courses': ['COMP790-178'],
        'availability': all_availability,  # No change
        'max_classes': 1
    },
    'Shashank Srivastava': {
        'qualified_courses': ['COMP664'],
        'availability': mwf,  # Changed from time_slots to mwf
        'max_classes': 1
    },
    'Snigdha Chaturvedi': {
        'qualified_courses': ['COMP790-158'],
        'availability': mwf[:3],  # No change
        'max_classes': 1
    },
    'Huaxiu Yao': {
        'qualified_courses': ['COMP790-183'],
        'availability': th,  # Changed from time_slots to th
        'max_classes': 1
    },
    'Andrew Kwong': {
        'qualified_courses': ['COMP790-185'],
        'availability': all_availability,  # No change
        'max_classes': 1
    },
    'Mike Reed': {
        'qualified_courses': ['COMP475'],
        'availability': mw,  # Changed from time_slots to mw
        'max_classes': 1
    },
    'Paul Stotts': {
        'qualified_courses': ['COMP590-59', 'COMP523'],
        'availability': all_availability,  # No change
        'max_classes': 3
    },
    'Prasun Dewan': {
        'qualified_courses': ['COMP524'],
        'availability': mwf,  # Already mwf, no change
        'max_classes': 1
    },
    'Jorge Silva': {
        'qualified_courses': ['COMP562'],
        'availability': th,  # Changed from time_slots to th
        'max_classes': 1
    },
    'Kris Jordan': {
        'qualified_courses': ['COMP590-140'],
        'availability': all_availability,  # No change
        'max_classes': 1
    },
    'Junier Oliva': {
        'qualified_courses': ['COMP755'],
        'availability': mwf,  # Changed from time_slots to mwf
        'max_classes': 1
    },
    'TBD': {
        'qualified_courses': ['COMP421'],
        'availability': all_availability,  # No change
        'max_classes': 1
    },
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
        'title': 'COMP283/283H Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 204}
            # Combined 283H section and increased the seat capacity by 24 from 180 to 204
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
            {'section_number': 1, 'seat_capacity': 60}
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
    # 'COMP590': {
    #     'title': 'COMP590 Class',
    #     'sections': [
    #         {'section_number': 59, 'seat_capacity': 90},
    #         {'section_number': 139, 'seat_capacity': 10},
    #         {'section_number': 140, 'seat_capacity': 280},
    #         {'section_number': 158, 'seat_capacity': 4},
    #         {'section_number': 170, 'seat_capacity': 30},
    #         {'section_number': 172, 'seat_capacity': 30},
    #         {'section_number': 177, 'seat_capacity': 60}
    #     ]
    # },
    'COMP590-59': {
        'title': 'COMP590-59 Class',
        'sections': [
            {'section_number': 59, 'seat_capacity': 90}
        ]
    },
    'COMP590-139': {
        'title': 'COMP590-139 Class',
        'sections': [
            {'section_number': 139, 'seat_capacity': 10}
        ]
    },
    'COMP590-140': {
        'title': 'COMP590-140 Class',
        'sections': [
            {'section_number': 140, 'seat_capacity': 280}
        ]
    },
    'COMP590-158': {
        'title': 'COMP590-158 Class',
        'sections': [
            {'section_number': 158, 'seat_capacity': 4}
        ]
    },
    'COMP590-170': {
        'title': 'COMP590-170 Class',
        'sections': [
            {'section_number': 170, 'seat_capacity': 30}
        ]
    },
    'COMP590-172': {
        'title': 'COMP590-172 Class',
        'sections': [
            {'section_number': 172, 'seat_capacity': 30}
        ]
    },
    'COMP590-177': {
        'title': 'COMP590-177 Class',
        'sections': [
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
    'COMP790-139': {
        'title': 'COMP790-139 Class',
        'sections': [
            {'section_number': 139, 'seat_capacity': 20},
        ]
    },
    'COMP790-144': {
        'title': 'COMP790-144 Class',
        'sections': [
            {'section_number': 144, 'seat_capacity': 30},
        ]
    },
    'COMP790-148': {
        'title': 'COMP790-148 Class',
        'sections': [
            {'section_number': 148, 'seat_capacity': 25},
        ]
    },
    'COMP790-158': {
        'title': 'COMP790-158 Class',
        'sections': [
            {'section_number': 158, 'seat_capacity': 21},
        ]
    },
    'COMP790-170': {
        'title': 'COMP790-170 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 30},
        ]
    },
    'COMP790-172': {
        'title': 'COMP790-172 Class',
        'sections': [
            {'section_number': 172, 'seat_capacity': 30},
        ]
    },
    'COMP790-173': {
        'title': 'COMP790-173 Class',
        'sections': [
            {'section_number': 173, 'seat_capacity': 30},
        ]
    },
    'COMP790-175': {
        'title': 'COMP790-175 Class',
        'sections': [
            {'section_number': 175, 'seat_capacity': 30},
        ]
    },
    'COMP790-178': {
        'title': 'COMP790-178 Class',
        'sections': [
            {'section_number': 178, 'seat_capacity': 20},
        ]
    },
    'COMP790-183': {
        'title': 'COMP790-183 Class',
        'sections': [
            {'section_number': 183, 'seat_capacity': 30},
        ]
    },
    'COMP790-185': {
        'title': 'COMP790-185 Class',
        'sections': [
            {'section_number': 185, 'seat_capacity': 30},
        ]
    },
    'COMP915': {
        'title': 'COMP915 Class',
        'sections': [
            {'section_number': 1, 'seat_capacity': 20}
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

# -----------------------------
# Manually Scheduled Classes (Constraints)
# -----------------------------

# Manually scheduled classes (constraints)
# Each entry can have partial or full specifications
manually_scheduled_classes = [
    # Example of a fully specified manual schedule
    {
        'course': 'COMP110',
        'section': 3,
        'professor': 'Alyssa Byrnes',
        'meeting_pattern': 'MWF',
        'period': 1,  # Period within the 'MWF' meeting pattern
        'room': 'university'
    },
    # Example of a partial specification (only professor assigned)
    {
        'course': 'COMP541',
        'section': 1,
        'professor': 'Montek Singh',
        'room': 'FB-F009'
        # 'meeting_pattern', 'time_slot', and 'room' are unspecified
    },
    {'course': 'COMP421',
     'section': 1,
     'professor:': "TBD",
     }
    
    # You can add more manually scheduled classes here
]

# Extract the set of manually scheduled classes for easy reference
manual_classes_set = set((entry['course'], entry['section']) for entry in manually_scheduled_classes)

# -----------------------------
# Helper Functions
# -----------------------------

def is_prof_available_and_qualified(p, c, ts):
    return int(ts in professors[p]['availability'] and c in professors[p]['qualified_courses'])

# -----------------------------
# ILP Model Setup
# -----------------------------

# Create the LP problem (Maximize the number of classes scheduled)
prob = pulp.LpProblem("Course_Scheduling_Problem", pulp.LpMaximize)

# Create time slots specific to each meeting pattern
# Create time slots specific to each meeting pattern
time_slots_mp = {}
for mp in meeting_patterns:
    mp_time_slots = []
    for period in meeting_patterns[mp]['periods'].keys():
        mp_time_slots.append((mp, period))
    time_slots_mp[mp] = mp_time_slots

# Define the threshold for small classes
small_class_threshold = 100

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

# Decision variables for scheduling classes in time slots and rooms
x = {}
for idx in x_indices:
    var_name = "x_%s_%s_%s_%s_%s" % idx
    x[idx] = pulp.LpVariable(var_name, cat='Binary')
# Binary variables for class scheduling
y = {}
for c in courses:
    for section in courses[c]['sections']:
        s = section['section_number']
        y[(c, s)] = pulp.LpVariable(f"y_{c}_{s}", cat='Binary')

# Binary variables for professor assignments
z = {}
for c in courses:
    for section in courses[c]['sections']:
        s = section['section_number']
        for p in professors:
            if c in professors[p]['qualified_courses']:
                z[(c, s, p)] = pulp.LpVariable(f"z_{c}_{s}_{p}", cat='Binary')


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

# 1. Link x and y variables: If a class is scheduled (y=1), it must be assigned to one meeting pattern, time slot, and room
for c in courses:
    for section in courses[c]['sections']:
        s = section['section_number']
        print(y[(c,s)])
        
        # Ensure that if a class is scheduled (y[c,s] = 1), exactly one scheduling combination (x[idx] = 1) is chosen
        # If y[c,s] = 0, then all corresponding x[idx] must be 0, meaning the class is not scheduled
        prob += pulp.lpSum([
            x[idx]
            for idx in x_indices
            if idx[0] == c and idx[1] == s
        ]) == y[(c, s)], f"Link_x_y_{c}_{s}"
        # Equation: Σ x[c,s,mp,ts,r] = y[c,s]

# 2. Professors assigned to sections must be qualified and available
for c in courses:
    for section in courses[c]['sections']:
        s = section['section_number']
        qualified_professors = [p for p in professors if c in professors[p]['qualified_courses']]
        
        # Ensure that if a class is scheduled (y[c,s] = 1), exactly one qualified professor is assigned to it
        # If y[c,s] = 0, no professor should be assigned
        prob += pulp.lpSum([
            z[(c, s, p)]
            for p in qualified_professors
        ]) == y[(c, s)], f"Prof_Assignment_{c}_{s}"
        # Equation: Σ z[c,s,p] = y[c,s]


# 3. Limit professors to maximum number of classes
for p in professors:
    
    # Ensure that no professor is assigned to more classes than their maximum allowed
    prob += pulp.lpSum([
        z[(c, s, p)]
        for c in courses
        for section in courses[c]['sections']
        for s in [section['section_number']]
        if (c, s, p) in z
    ]) <= professors[p]['max_classes'], f"Max_Classes_{p}"
    # Equation: Σ z[c,s,p] ≤ max_classes_p


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





for r in rooms:
    for d in days:
        # Get sorted list of periods for the day based on 'MW' meeting patterns
        periods = sorted(meeting_patterns['MW']['periods'].keys())
        # print("awiubfewabfiwauebfwaoiefbwaoiefbiewbf")
        # print(periods)
        for p in periods:
            next_p = p + 1
            if next_p in meeting_patterns['MW']['periods'].keys():
                # Define the current and next time slots
                current_ts = (d, p)
                next_ts = (d, next_p)
                
                # Sum of 'MW' classes in current time slot in room r
                mw_current = pulp.lpSum([
                    x[idx] for idx in x_indices
                    if idx[2] == 'MW' and idx[3] == current_ts and idx[4] == r
                ])
                
                # Sum of 'MWF' classes in next time slot in room r
                mwf_next = pulp.lpSum([
                    x[idx] for idx in x_indices
                    if idx[2] == 'MWF' and idx[3] == next_ts and idx[4] == r
                ])
                
                # Sum of 'MW' classes in next time slot in room r
                mw_next = pulp.lpSum([
                    x[idx] for idx in x_indices
                    if idx[2] == 'MW' and idx[3] == next_ts and idx[4] == r
                ])
                
                # Add the constraint: MW at p + MWF/MW at p+1 <= 1
                prob += mw_current + mwf_next + mw_next <= 1, f"Room_Overlap_{r}_{d}_{p}"
                # This ensures that if a MW class is scheduled at p, no MWF or MW class can be scheduled at p+1 in the same room

rush_hour_time_slots = set()

for mp in meeting_patterns:
    for day in meeting_patterns[mp]['days']:
        for period, info in meeting_patterns[mp]['periods'].items():
            start_time = info['start_time']
            
            # Convert start_time to minutes since midnight for easy comparison
            time_parts = start_time[:-2].split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            am_pm = start_time[-2:]
            
            if am_pm == 'PM' and hour != 12:
                hour += 12
            elif am_pm == 'AM' and hour == 12:
                hour = 0
            
            start_minutes = hour * 60 + minute
            
            # Define rush-hour as 11:00 AM (600 minutes) to 2:00 PM (900 minutes)
            if 600 <= start_minutes < 900:
                rush_hour_time_slots.add((day, period))
                # Example: ('Monday', 3) represents Monday, Period 3

# Identify x indices in rush-hour
rush_hour_x_indices = [
    idx for idx in x_indices
    if idx[3] in rush_hour_time_slots  # idx[3] is the time_slot tuple (day, period)
]

# Define a penalty coefficient for rush-hour classes
# Adjust this value to control the severity of the penalty
rush_hour_penalty = 0
room_cost = {}
for idx in x_indices:
    c, s, mp, ts, r = idx
    if r == 'university' and (c, s) in small_classes:
        room_cost[idx] = 1  # Assign a penalty cost
    else:
        room_cost[idx] = 0

# Modify the objective function
# -----------------------------
# 9. Modifying the Objective Function
# -----------------------------

# Define a penalty coefficient for rush-hour classes
# Adjust this value to control the severity of the penalty
rush_hour_penalty = 0  # You can experiment with different values like 0.5, 1, or 2

# Modify the objective function to include rush-hour penalties
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

# Explanation:
# Maximize the number of classes scheduled (Σ y[c,s])
# Minimize the room costs (Σ room_cost[idx] * x[idx])
# Minimize the number of rush-hour classes (rush_hour_penalty * Σ x[rush_hour_x_indices])

# -----------------------------
# Solve the Problem
# -----------------------------

prob.solve()

# -----------------------------
# Output the Schedule and Store Assignments
# -----------------------------

# Output the Schedule and Store Assignments
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
                        end_time = meeting_patterns[mp]['periods'][period]['end_time']
                        schedule.append({
                            'Course': c,
                            'Section': s,
                            'Title': courses[c]['title'],
                            'Professor': assigned_professor,
                            'Meeting Pattern': mp,
                            'Days': days,
                            'Period': period,
                            'Start Time': start_time,
                            'End Time': end_time,
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
    
    # Print the initial schedule
    for entry in schedule:
        print(f"Course: {entry['Course']} Section {entry['Section']}, Title: {entry['Title']}")
        print(f"  Professor: {entry['Professor']}")
        print(f"  Meeting Pattern: {entry['Meeting Pattern']}")
        print(f"  Days: {', '.join(entry['Days'])}, Period: {entry['Period']}, Start Time: {entry['Start Time']}, End Time: {entry['End Time']}")
        print(f"  Room: {entry['Room']}")
        print(f"  Seat Capacity: {entry['Seat Capacity']}\n")

    
    # Print unscheduled classes
    if unscheduled_classes:
        print("Unscheduled Classes:")
        for c, s in unscheduled_classes:
            print(f"Course: {c}, Section: {s}, Title: {courses[c]['title']}")
    
    # -----------------------------
    # New Code to Print Professors with No Classes Scheduled
    # -----------------------------
    
#     # Initialize a dictionary to count classes assigned to each professor
#     professor_class_counts = {p: 0 for p in professors}
    
#     # Iterate over the assignment variables z to count classes
#     for (c, s, p) in z:
#         if pulp.value(z[(c, s, p)]) == 1:
#             professor_class_counts[p] += 1
    
#     # List of professors with no classes assigned
#     professors_with_no_classes = [p for p, count in professor_class_counts.items() if count == 0]
    
#     # Print professors with no classes scheduled
#     if professors_with_no_classes:
#         print("\nProfessors with no classes scheduled:")
#         for p in professors_with_no_classes:
#             print(f"Professor: {p}")
#     else:
#         print("\nAll professors have at least one class scheduled.")
    
# else:
#     print("No feasible solution found. Solver Status:", pulp.LpStatus[prob.status])
# print("All Time Slots:", time_slots)
# print("MWF Segments:", mwf, "MW Segments:", mwf, "TTH Segments:", th)
# print("Time Slots per Meeting Pattern:", time_slots_mp)


# def remove_and_reassign(prob, x, y, z, x_indices, assignment, c_remove, s_remove, new_mp, new_ts, new_r):
#     """
#     Removes a course section from its current assignment and attempts to reassign it to a new meeting pattern, time slot, and room.

#     :param prob: The PuLP problem instance.
#     :param x: Dictionary of x variables.
#     :param y: Dictionary of y variables.
#     :param z: Dictionary of z variables.
#     :param x_indices: List of all x indices.
#     :param assignment: Dictionary storing current assignments.
#     :param c_remove: Course code to remove.
#     :param s_remove: Section number to remove.
#     :param new_mp: New meeting pattern (e.g., 'MWF', 'TTH', 'MW').
#     :param new_ts: New time slot tuple (day, period).
#     :param new_r: New room code.
#     :return: True if reassignment is possible, False otherwise.
#     """
#     key = (c_remove, s_remove)
#     if key not in assignment:
#         print(f"Course {c_remove} Section {s_remove} is not scheduled. No action taken.")
#         return False
    
#     # Get the current assignment index
#     current_idx = assignment[key]
    
#     # Remove the current assignment by setting x[current_idx] == 0
#     prob += x[current_idx] == 0, f"Remove_Assignment_{c_remove}_{s_remove}"
    
#     # Remove the current professor assignment if any
#     assigned_professor = None
#     for p in professors:
#         if (c_remove, s_remove, p) in z and pulp.value(z[(c_remove, s_remove, p)]) == 1:
#             assigned_professor = p
#             # Set z[c,s,p] == 0
#             prob += z[(c_remove, s_remove, p)] == 0, f"Remove_Professor_Assigned_{c_remove}_{s_remove}_{p}"
#             break
    
#     # Allow the class to be rescheduled elsewhere by keeping y[c,s] ==1
#     prob += y[key] == 1, f"Ensure_Class_Scheduled_{c_remove}_{s_remove}"
    
#     # Attempt to assign to the new meeting pattern, time slot, and room
#     # Find the index corresponding to the new assignment
#     new_idx = (c_remove, s_remove, new_mp, new_ts, new_r)
#     if new_idx not in x:
#         print(f"Warning: The new assignment ({new_mp}, {new_ts}, {new_r}) for Course {c_remove} Section {s_remove} is invalid.")
#         return False
    
#     # Add constraint to set x[new_idx] ==1
#     prob += x[new_idx] == 1, f"Assign_New_Schedule_{c_remove}_{s_remove}_{new_mp}_{new_ts}_{new_r}"
    
#     # Find a qualified and available professor for the new assignment
#     qualified_professors = [p for p in professors if c_remove in professors[p]['qualified_courses']]
    
#     # Attempt to assign a professor
#     professor_assigned = False
#     for p in qualified_professors:
#         if new_ts in professors[p]['availability']:
#             # Check if the professor is available at the new time slot
#             conflict = False
#             for idx in x_indices:
#                 if idx[3] == new_ts and (idx[0], idx[1], p) in z and pulp.value(z[(idx[0], idx[1], p)]) == 1:
#                     conflict = True
#                     break
#             if not conflict:
#                 # Assign this professor
#                 prob += z[(c_remove, s_remove, p)] == 1, f"Assign_New_Professor_{c_remove}_{s_remove}_{p}"
#                 professor_assigned = True
#                 break
    
#     if not professor_assigned:
#         print(f"No available and qualified professor found for Course {c_remove} Section {s_remove} at the new time slot.")
#         # Remove the constraint we just added since no professor can be assigned
#         prob.constraints.pop(f"Assign_New_Schedule_{c_remove}_{s_remove}_{new_mp}_{new_ts}_{new_r}", None)
#         # Revert removal of current assignment
#         prob.constraints.pop(f"Remove_Assignment_{c_remove}_{s_remove}", None)
#         if assigned_professor:
#             prob.constraints.pop(f"Remove_Professor_Assigned_{c_remove}_{s_remove}_{assigned_professor}", None)
#         return False
    
#     # Re-solve the problem
#     prob.solve()
    
#     if pulp.LpStatus[prob.status] == 'Optimal':
#         # Verify the new assignment
#         if pulp.value(x[new_idx]) == 1:
#             # Update the assignment dictionary
#             assignment[key] = new_idx
#             print(f"Course {c_remove} Section {s_remove} has been successfully reassigned to:")
#             print(f"  Meeting Pattern: {new_mp}")
#             print(f"  Time Slot: {new_ts}")
#             print(f"  Room: {new_r}")
#             print(f"  Professor: {p}\n")
#             return True
#         else:
#             print(f"Failed to assign Course {c_remove} Section {s_remove} to the new schedule.")
#             return False
#     else:
#         print(f"Unable to reassign Course {c_remove} Section {s_remove} due to constraints.")
#         return False
# # Example Usage of remove_and_reassign Function

# # Suppose you want to remove and reassign COMP110 Section 3 to ('Tuesday', 2) in room 'FB-F009' with meeting pattern 'TTH'
# c_to_remove = 'COMP110'
# s_to_remove = 3
# new_meeting_pattern = 'TTH'
# new_time_slot = ('Tuesday', 3)
# new_room = 'FB-F009'

# print(f"\nAttempting to remove and reassign Course {c_to_remove} Section {s_to_remove}...\n")
# result = remove_and_reassign(prob, x, y, z, x_indices, assignment, 
#                              c_to_remove, s_to_remove, 
#                              new_meeting_pattern, new_time_slot, new_room)

# if result:
#     print(f"\nSuccessfully reassigned Course {c_to_remove} Section {s_to_remove}.\n")
# else:
#     print(f"\nFailed to reassign Course {c_to_remove} Section {s_to_remove}.\n")

