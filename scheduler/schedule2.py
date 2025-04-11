import pandas as pd

class CourseScheduler:
    def __init__(self,
                 course_cap_file: str,
                 top_courses_file: str,
                 faculty_availability_file: str,
                 faculty_qualification_file: str,
                 classroom_file: str):

        self.course_cap_file = course_cap_file
        self.top_courses_file = top_courses_file
        self.faculty_availability_file = faculty_availability_file
        self.faculty_qualification_file = faculty_qualification_file
        self.classroom_file = classroom_file

        # UNC standard course time slots
        self.time_slots = [ 
            "MWF_1", "MWF_2", "MWF_3", "MWF_4", "MWF_5", "MWF_6", "MWF_7", "MWF_8", "MWF_9", "MWF_10",
            "MW_1", "MW_2", "MW_3", "MW_4", "MW_5", "MW_6", "MW_7",
            "TTH_1", "TTH_2", "TTH_3", "TTH_4", "TTH_5", "TTH_6", "TTH_7"
        ]
        self.time_slot_mapping = {
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
            "TTH_7": "5:00 – 6:15 p.m."
        }

        self.load_all_data()

    def load_all_data(self):
        self.course_caps = pd.read_excel(self.course_cap_file)
        self.top_courses = pd.read_csv(self.top_courses_file)
        self.faculty_availability = pd.read_excel(self.faculty_availability_file)
        self.faculty_qualification = pd.ExcelFile(self.faculty_qualification_file)
        self.classrooms = pd.read_excel(self.classroom_file)

        print("Data successfully loaded.")
