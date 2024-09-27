from constraint import Problem, AllDifferentConstraint
import itertools
professors = {
    'Montek Singh': {
        'qualified_courses': ['COMP541', 'COMP572'],
        'availability': time_slots  # Adjust availability if needed
    },
    'Kurt M. Potter': {
        'qualified_courses': ['COMP301', 'COMP426'],
        'availability': time_slots
    },
    'Muhammad Ghani': {
        'qualified_courses': ['COMP210'],
        'availability': time_slots
    },
    'Praveen Kumar': {
        'qualified_courses': ['COMP455'],
        'availability': time_slots
    },
    'Jasleen Kaur': {
        'qualified_courses': ['COMP431'],
        'availability': time_slots
    },
    'Saba Eskandarian': {
        'qualified_courses': ['COMP537', 'COMP455', 'COMP435', 'COMP590', 'COMP790'],
        'availability': time_slots
    },
    'Ron Alterovitz': {
        'qualified_courses': ['COMP581', 'COMP781', 'COMP782'],
        'availability': time_slots
    },
    'Cynthia Sturton': {
        'qualified_courses': ['COMP435'],
        'availability': time_slots
    },
    'Marc Niethammer': {
        'qualified_courses': ['COMP775'],
        'availability': time_slots
    },
    'Samarjit Chakraborty': {
        'qualified_courses': ['COMP545', 'COMP790'],
        'availability': time_slots
    },
    'Donald Porter': {
        'qualified_courses': ['COMP530'],
        'availability': time_slots
    },
    'John Majikes': {
        'qualified_courses': ['COMP421', 'COMP550', 'COMP116'],
        'availability': time_slots
    },
    'Alyssa Byrnes': {
        'qualified_courses': ['COMP110', 'COMP116', 'COMP210', 'COMP283'],
        'availability': time_slots
    },
    'Gedas Bertasius': {
        'qualified_courses': ['COMP590', 'COMP790'],
        'availability': time_slots
    },
    'Roni Sengupta': {
        'qualified_courses': ['COMP590'],
        'availability': time_slots
    },
    'Kangning Sun': {
        'qualified_courses': ['COMP283', 'COMP455', 'COMP550'],
        'availability': time_slots
    },
    'Jim McMahon': {
        'qualified_courses': ['COMP311', 'COMP541'],
        'availability': time_slots
    },
    'Shahriar Nirjon': {
        'qualified_courses': ['COMP433'],
        'availability': time_slots
    },
    'Jack Snoeyink': {
        'qualified_courses': ['COMP283', 'DATA140'],
        'availability': time_slots
    },
    'Brent Munsell': {
        'qualified_courses': ['COMP211', 'COMP590', 'COMP530', 'COMP311', 'COMP116'],
        'availability': time_slots
    },
    'James Anderson': {
        'qualified_courses': ['COMP737', 'COMP750'],
        'availability': time_slots
    },
    'Danielle Szafir': {
        'qualified_courses': ['COMP790'],
        'availability': time_slots
    },
    'Daniel Szafir': {
        'qualified_courses': ['COMP581'],
        'availability': time_slots
    },
    'Praneeth Chakravarthula': {
        'qualified_courses': ['COMP089', 'COMP790'],
        'availability': time_slots
    },
    'Ben Lee': {
        'qualified_courses': ['COMP790'],
        'availability': time_slots
    },
    'Shubhra Srivastava': {
        'qualified_courses': ['COMP664'],
        'availability': time_slots
    },
    'Chase P. Kline': {
        'qualified_courses': ['COMP790'],
        'availability': time_slots
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

time_slots = ['TuTh 8:00AM - 9:15AM',
    'TuTh 9:30AM - 10:45AM',
    'TuTh 11:00AM - 12:15PM',
    'TuTh 12:30PM - 1:45PM',
    'TuTh 2:00PM - 3:15PM',
    'TuTh 3:30PM - 4:45PM',
    'TuTh 5:00PM - 6:15PM',
    'MoWe 3:35PM - 4:50PM',
    'MoWe 5:05PM - 6:20PM',
    'MoFr 3:35PM - 4:50PM',
    'MoFr 5:05PM - 6:20PM',
    'WeFr 3:35PM - 4:50PM',
    'WeFr 5:05PM - 6:20PM',
    'MoWeFr 8:00AM - 8:50AM',
    'MoWeFr 9:05AM - 9:55AM',
    'MoWeFr 10:10AM - 11:00AM',
    'MoWeFr 11:15AM - 12:05PM',
    'MoWeFr 12:20PM - 1:10PM',
    'MoWeFr 1:25PM - 2:15PM',
    'MoWeFr 2:30PM - 3:20PM',
    'MoWeFr 3:35PM - 4:25PM',
    'MoWeFr 4:40PM - 5:30PM',
    'MoWeFr 5:45PM - 6:35PM'
]

# Assume all professors are available at all time slots for simplicity
for prof in professors.values():
    prof['availability'] = time_slots

# Create a list of course sections to schedule
course_sections = []
for course_code, course_info in courses.items():
    for section in course_info['sections']:
        course_sections.append({
            'course_code': course_code,
            'section_number': section['section_number'],
            'seat_capacity': section['seat_capacity']
        })

# Initialize the problem
problem = Problem()

# Variables: Each course section needs to be assigned a (professor, room, time_slot)
for section in course_sections:
    variable_name = f"{section['course_code']}_Section_{section['section_number']}"
    problem.addVariable(variable_name, [])

# Build domains for each variable
for section in course_sections:
    variable_name = f"{section['course_code']}_Section_{section['section_number']}"
    domain = []
    course_code = section['course_code']
    seat_capacity = section['seat_capacity']

    # Determine eligible professors
    eligible_professors = [
        prof_name for prof_name, prof_info in professors.items()
        if course_code in prof_info['qualified_courses']
    ]

    # If no professors are qualified, skip this section
    if not eligible_professors:
        continue

    # Determine eligible rooms
    if seat_capacity is None:
        seat_capacity = 30  # Default seat capacity if not specified

    if seat_capacity > 100:
        eligible_rooms = ['university']
    else:
        eligible_rooms = [
            room_name for room_name, room_info in rooms.items()
            if room_info['capacity'] >= seat_capacity and room_name != 'university'
        ]

    # Build the domain (professor, room, time_slot)
    for prof in eligible_professors:
        for room in eligible_rooms:
            for time in time_slots:
                # Check professor availability
                if time in professors[prof]['availability']:
                    # For simplicity, assume all rooms are available at all times
                    domain.append((prof, room, time))

    problem.addVariable(variable_name, domain)

# Constraints

# 1. Professors cannot teach more than one class at the same time
for time in time_slots:
    sections_at_time = []
    for section in course_sections:
        variable_name = f"{section['course_code']}_Section_{section['section_number']}"
        # Filter variables that have time in their domain
        if any(assignment[2] == time for assignment in problem._variables[variable_name]):
            sections_at_time.append(variable_name)
    if sections_at_time:
        problem.addConstraint(
            lambda *assignments: len(set(prof for prof, _, _ in assignments if prof != '')) == len(assignments),
            sections_at_time
        )

# 2. Rooms cannot host more than one class at the same time (except 'university' room)
for time in time_slots:
    sections_at_time = []
    for section in course_sections:
        variable_name = f"{section['course_code']}_Section_{section['section_number']}"
        # Filter variables that have time in their domain
        if any(assignment[2] == time for assignment in problem._variables[variable_name]):
            sections_at_time.append(variable_name)
    if sections_at_time:
        problem.addConstraint(
            lambda *assignments: len(set(
                room for _, room, _ in assignments if room != 'university'
            )) == len([
                room for _, room, _ in assignments if room != 'university'
            ]),
            sections_at_time
        )

# Solve the problem
solution = problem.getSolution()

# Display the schedule
if solution:
    print("Schedule created successfully!\n")
    for variable, assignment in solution.items():
        course_code, section = variable.split('_Section_')
        professor, room, time = assignment
        print(f"Course: {course_code}, Section: {section}")
        print(f"  Professor: {professor}")
        print(f"  Room: {room}")
        print(f"  Time: {time}")
        print()
else:
    print("No valid schedule found.")