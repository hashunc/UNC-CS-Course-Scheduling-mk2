import shutil
from fastapi import HTTPException
import pulp
from collections import defaultdict
import json

def load_days():
    return ['Monday', 'Tuesday', 'Wednesday']

def load_periods():
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
        2: {'start_time': '9:05AM', 'duration': 75, 'end_time': '10:20AM'},
        3: {'start_time': '10:10AM', 'duration': 75, 'end_time': '11:25AM'},
        4: {'start_time': '11:15AM', 'duration': 75, 'end_time': '12:30PM'},
        5: {'start_time': '12:20PM', 'duration': 75, 'end_time': '1:35PM'},
        6: {'start_time': '1:25PM', 'duration': 75, 'end_time': '2:40PM'},
        7: {'start_time': '2:30PM', 'duration': 75, 'end_time': '3:45PM'},
        8: {'start_time': '3:35PM', 'duration': 75, 'end_time': '4:50PM'},
    }
    return mwf_periods, tth_periods, mw_periods


def load_meeting_patterns(mwf_periods, tth_periods, mw_periods):
    meeting_patterns = {
        'MWF': {'days': ['Monday'], 'periods': mwf_periods},
        'TTH': {'days': ['Tuesday'], 'periods': tth_periods},
        'MW': {'days': ['Monday'], 'periods': mw_periods},
        }  
    return meeting_patterns


def backup_data():
    FILE_PATH = "professors.json"
    BACKUP_PATH = "professors_backup.json"
    try:
        shutil.copy(FILE_PATH, BACKUP_PATH)
    except FileNotFoundError:
        with open(BACKUP_PATH, "w") as backup_file:
            json.dump({}, backup_file, indent=4)

def restore_backup():
    FILE_PATH = "professors.json"
    BACKUP_PATH = "professors_backup.json"
    try:
        shutil.copy(BACKUP_PATH, FILE_PATH)
        print("Rollback successful. Changes have been undone.")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Backup file not found. Cannot restore.")

def get_professordata():
    file_path = "professors.json"

    with open(file_path) as file:
        data = json.load(file)
    return data

def add_professor(name, qualified_courses, availability, max_classes):
    backup_data()
    file_path = "professors.json"

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if name in data:
        print(f"Professor {name} already exists in the dataset.")
        return data
    data[name] = {
        "qualified_courses": qualified_courses,
        "availability": availability,
        "max_classes": max_classes
    }
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data

def update_professor(name, qualified_courses = None, availability = None, max_classes = None):
    backup_data()
    file_path = "professors.json"
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No data file found. Cannot update.")
    if name not in data:
        raise HTTPException(status_code=404, detail=f"Professor {name} not found.")
    professor = data[name]
    if qualified_courses is not None:
        professor["qualified_courses"] = qualified_courses
    if availability is not None:
        professor["availability"] = availability
    if max_classes is not None:
        professor["max_classes"] = max_classes
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data

def delete_professor(name):
    backup_data()
    file_path = "professors.json"
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No data file found. Cannot delete.")
    if name not in data:
        raise HTTPException(status_code=404, detail=f"Professor {name} not found.")  
    del data[name]
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)    
    return data 

def backup_courses():
    FILE_PATH = "course.json"
    BACKUP_PATH = "courses_backup.json"
    try:
        shutil.copy(FILE_PATH, BACKUP_PATH)
    except FileNotFoundError:
        with open(BACKUP_PATH, "w") as backup_file:
            json.dump({}, backup_file, indent=4)

def restore_courses():
    FILE_PATH = "courses.json"
    BACKUP_PATH = "courses_backup.json"
    try:
        shutil.copy(BACKUP_PATH, FILE_PATH)
        print("Rollback successful. Changes have been undone.")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Backup file not found. Cannot restore.")

def get_coursedata():
    file_path = "courses.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)    
    except FileNotFoundError: 
        raise HTTPException(status_code=404, detail = "No data file found.") 
    return data

def add_courses(title, sections):
    #backup_courses()
    file_path = "courses.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if title in data:
        print(f"Course {title} already exists in the dataset.")
        return data
    data[title] = {
        "sections": sections
    }
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data

def update_course(title, sections):
    #backup_courses()
    file_path = "courses.json"
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No data file found. Cannot update.")
    if title not in data:
        raise HTTPException(status_code=404, detail=f"Professor {name} not found.")
    course = data[title]
    if sections is not None:
        course["sections"] = sections

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data

def delete_course(title):
    #backup_courses()
    file_path = "courses.json"
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No data file found. Cannot delete.")
    if title not in data:
        raise HTTPException(status_code=404, detail=f"Course {title} not found.")  
    del data[title]
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)    
    return data 

def get_roomdata():
    file_path = "rooms.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)    
    except FileNotFoundError: 
        raise HTTPException(status_code=404, detail = "No data file found.") 
    return data

def add_room(name, capacity):
    file_path = "rooms.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if name in data:
        print(f"Room {name} already exists in the dataset.")
        return data
    data[name] = {
        "capacity": capacity
    }
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data    

def update_room(name, capacity):
    file_path = "rooms.json"
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No data file found. Cannot update.")
    if name not in data:
        raise HTTPException(status_code=404, detail=f"Professor {name} not found.")
    room = data[name]
    room["capacity"] = capacity
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data

def delete_room(name):
    #backup_courses()
    file_path = "rooms.json"
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No data file found. Cannot delete.")
    if name not in data:
        raise HTTPException(status_code=404, detail=f"Course {name} not found.")  
    del data[name]
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)    
    return data 

def load_professors():
    time_slots = []
    mwf_periods, tth_periods, mw_periods = load_periods()
    meeting_patterns = load_meeting_patterns(mwf_periods, tth_periods, mw_periods)
    for mp in meeting_patterns.values():
        for day in mp['days']:
            for period in mp['periods'].keys():
                time_slots.append((day, period))
    professors = {
    'Montek Singh': {
        'qualified_courses': ['COMP541', 'COMP572'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Tessa Joseph-Nicholas': {
        'qualified_courses': ['COMP126', "COMP380", "COMP380H"],
        'availability': time_slots,
        'max_classes': 3
    },
    'Ketan Mayer-Patel': {
        'qualified_courses': ['COMP301', 'COMP426'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Prairie Goodwin': {
        'qualified_courses': ['COMP301'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Sayeed Ghani': {
        'qualified_courses': ['COMP210'],
        'availability': time_slots,
        'max_classes': 2
    },
    'P.S. Thiagarajan': {
        'qualified_courses': ['COMP455'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Jasleen Kaur': {
        'qualified_courses': ['COMP431'],
        'availability': time_slots,
        'max_classes': 0
    },
    'Saba Eskandarian': {
        'qualified_courses': ['COMP537', 'COMP455', 'COMP435', 'COMP590', 'COMP790'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Ron Alterovitz': {
        'qualified_courses': ['COMP581', 'COMP781', 'COMP782'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Cynthia Sturton': {
        'qualified_courses': ['COMP435'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Marc Niethammer': {
        'qualified_courses': ['COMP775'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Izzi Hinks': {
        'qualified_courses': ['COMP110'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Samarjit Chakraborty': {
        'qualified_courses': ['COMP545', 'COMP790-148'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Donald Porter': {
        'qualified_courses': ['COMP530'],
        'availability': time_slots,
        'max_classes': 1
    },
    # Note: No longer at UNC
    'John Majikes': {
        'qualified_courses': ['COMP421', 'COMP550', 'COMP116'],
        'availability': time_slots,
        'max_classes': 2
    },
    # Note: Alyssa not on the given spreadsheet
    'Alyssa Byrnes': {
        'qualified_courses': ['COMP110', 'COMP116', 'COMP210', 'COMP283'],
        'availability': time_slots,
        'max_classes': 2
    },
    'Gedas Bertasius': {
        # Note, cross listed 590 and 790. Should get rid of 790 version
        'qualified_courses': ['COMP790-170'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Roni Sengupta': {
        'qualified_courses': ['COMP590-177'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Kevin Sun': {
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
        'max_classes': 1
    },
    'Jack Snoeyink': {
        'qualified_courses': ['COMP283', 'DATA140'],
        'availability': time_slots,
        'max_classes': 1
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
        # Note, he says he prefers visualization design, but is happy to teach something else
        # How do we specify what his qualified courses are?
        'qualified_courses': ['COMP790-172'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Daniel Szafir': {
        'qualified_courses': ['COMP581'],
        'availability': time_slots,
        'max_classes': 1
    },
    # Note: The course he specified was Safe Autonomy, but the course he teaches is Formal Methods
    'Parasara Sridhar Duggirala': {
        'qualified_courses': ['COMP089','COMP790-144'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Praneeth Chakravarthula': {
        'qualified_courses': [ 'COMP790-175'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Ben Berg': {
        'qualified_courses': ['COMP790-178'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Shashank Srivastava': {
        'qualified_courses': ['COMP664'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Snigdha Chaturvedi': {
        'qualified_courses': ['COMP790-158'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Huaxiu Yao': {
        'qualified_courses': ['COMP790-183'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Andrew Kwong': {
        'qualified_courses': ['COMP790-185'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Mike Reed': {
        'qualified_courses': ['COMP475'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Paul Stotts': {
        'qualified_courses': ['COMP590-59', 'COMP523'],
        'availability': time_slots,
        'max_classes': 3
    },
    'Prasun Dewan': {
        'qualified_courses': ['COMP524'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Jorge Silva': {
        'qualified_courses': ['COMP562'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Kris Jordan': {
        'qualified_courses': ['COMP590-140'],
        'availability': time_slots,
        'max_classes': 1
    },
    'Junier Oliva': {
        'qualified_courses': ['COMP755'],
        'availability': time_slots,
        'max_classes': 1
    },
    'TBD': {
        'qualified_courses': ['COMP421'],
        'availability': time_slots,
        'max_classes': 1
    },
    
}
    return professors

def load_courses():
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
    return courses
restore_courses()

def load_rooms():
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
        'university': {'capacity': 300}  
}
    return rooms

def load_manually_scheduled_classes():
    manually_scheduled_classes = [
        # Example of a fully specified manual schedule
        {
            'course': 'COMP110',
            'section': 3,
            'professor': 'Alyssa Byrnes',
            'meeting_pattern': 'MWF',
            'time_slot': ('Monday', 1),
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
    return manually_scheduled_classes

def is_prof_available_and_qualified(p, c, ts):
    professors = load_professors()
    return int(ts in professors[p]['availability'] and c in professors[p]['qualified_courses'])


import pulp

def run_scheduling_algorithm (
    days,
    meeting_patterns,
    professors,
    courses,
    rooms,
    manually_scheduled_classes = None,
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
        for day in meeting_patterns[mp]['days']:
            for period in meeting_patterns[mp]['periods'].keys():
                mp_time_slots.append((day, period))
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
                for ts in time_slots_mp[mp]:
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
                        idx = (c, s, mp, ts, r)
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
            # Ensure the professor is not assigned to other classes at the same time
            if 'time_slot' in entry:
                ts = tuple(entry['time_slot'])
                day, period = ts
                # Professors can't teach other classes at the same time
                for other_c in courses:
                    for section in courses[other_c]['sections']:
                        other_s = section['section_number']
                        if (other_c, other_s, p) in z and (other_c != c or other_s != s):
                            # Ensure uniqueness of constraint names
                            constraint_name = f"Manual_Prof_Time_Conflict_{p}_{day}_{period}_{other_c}_{other_s}"
                            prob += pulp.lpSum([
                                x[idx]
                                for idx in x_indices
                                if idx[0] == other_c and idx[1] == other_s and idx[3] == ts
                            ]) == 0, constraint_name

        # Fix meeting pattern, time slot, and room if specified
        if 'meeting_pattern' in entry and 'time_slot' in entry and 'room' in entry:
            mp = entry['meeting_pattern']
            ts = tuple(entry['time_slot'])
            r = entry['room']
            # Set x variable corresponding to these values to 1
            idx = (c, s, mp, ts, r)
            if idx in x:
                prob += x[idx] == 1, f"Manual_Schedule_{c}_{s}_{mp}_{ts}_{r}"
            else:
                pass  
        else:
            # Partial specifications
            if 'meeting_pattern' in entry:
                mp = entry['meeting_pattern']
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if idx[0] == c and idx[1] == s and idx[2] == mp
                ]) == 1, f"Manual_Meeting_Pattern_{c}_{s}_{mp}"

            if 'time_slot' in entry:
                ts = tuple(entry['time_slot'])
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if idx[0] == c and idx[1] == s and idx[3] == ts
                ]) == 1, f"Manual_Time_Slot_{c}_{s}_{ts}"

            if 'room' in entry:
                r = entry['room']
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if idx[0] == c and idx[1] == s and idx[4] == r
                ]) == 1, f"Manual_Room_{c}_{s}_{r}"

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
        for ts in set(professors[p]['availability']):
            day, period = ts
            ts_str = f"{day}_{period}"
            constraint_name = f"Prof_Time_Conflict_{p}_{ts_str}"
            prob += pulp.lpSum([
                x[idx]
                for idx in x_indices
                if idx[3] == ts and (idx[0], idx[1], p) in z
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
                        if idx[0] == c and idx[1] == s and idx[3] in professors[p]['availability']
                    ]) >= z[(c, s, p)], constraint_name

    # 5b. If x[idx] == 1, then z[(c, s, p)] == 1 for some p
    for idx in x_indices:
        c, s, mp, ts, r = idx
        constraint_name = f"Link_x_z_{c}_{s}_{mp}_{ts}_{r}"
        prob += x[idx] <= pulp.lpSum([
            z[(c, s, p)]
            for p in professors
            if (c, s, p) in z and ts in professors[p]['availability']
        ]), constraint_name

    # 6. Room capacity constraints (no double booking)
    # Collect all unique time slots across all meeting patterns
    all_time_slots = set()
    for mp in time_slots_mp:
        all_time_slots.update(time_slots_mp[mp])

    for r in rooms:
        if r != 'university':
            for ts in all_time_slots:
                day, period = ts
                ts_str = f"{day}_{period}"
                constraint_name = f"Room_Capacity_{r}_{ts_str}"
                # Ensure uniqueness of constraint names
                if constraint_name in prob.constraints:
                    index = 1
                    while f"{constraint_name}_{index}" in prob.constraints:
                        index += 1
                    constraint_name = f"{constraint_name}_{index}"
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if idx[4] == r and idx[3] == ts
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
                            c, s, mp, ts, r = idx
                            section = next(sec for sec in courses[c]['sections'] if sec['section_number'] == s)
                            seat_capacity = section['seat_capacity']
                            # Find the assigned professor
                            assigned_professor = None
                            for p in professors:
                                if (c, s, p) in z and pulp.value(z[(c, s, p)]) == 1:
                                    assigned_professor = p
                                    break
                            day, period = ts
                            start_time = meeting_patterns[mp]['periods'][period]['start_time']
                            end_time = meeting_patterns[mp]['periods'][period]['end_time']
                            schedule.append({
                                'Course': c,
                                'Section': s,
                                'Title': courses[c]['title'],
                                'Professor': assigned_professor,
                                'Meeting Pattern': mp,
                                'Day': day,
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
                        unscheduled_classes.append({
                            'Course': c,
                            'Section': s,
                            'Title': courses[c]['title']
                        })
                else:
                    # Class is not scheduled
                    unscheduled_classes.append({
                        'Course': c,
                        'Section': s,
                        'Title': courses[c]['title']
                    })

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
'''
manually_scheduled_classes = None
days = load_days()
mwf_periods, tth_periods, mw_periods = load_periods()
meeting_patterns =  load_meeting_patterns(mwf_periods, tth_periods, mw_periods)
professors =  load_professors()
courses =  load_courses()
rooms =  load_rooms()

results = run_scheduling_algorithm(
    days=days,
    meeting_patterns=meeting_patterns,
    professors=professors,
    courses=courses,
    rooms=rooms,
    manually_scheduled_classes=manually_scheduled_classes
)
print(results)
'''