# scheduler/config.py

# Input files
INPUT_COURSE_CAP = "data/Input/ClassEnrollCap.xlsx"
INPUT_AVAILABILITY = "data/Input/Responses.xlsx"
INPUT_CLASSROOM = "data/Input/ClassRoom.xlsx"
INPUT_CURRICULUM_COVERAGE = "data/Input/FacultyQualificationPreference.xlsx"


# Output files
OUTPUT_NEW_DATA_590_790 = "data/CSV/new_data_590_790.csv"
OUTPUT_NEW_DATA_590_AND_790 = "data/CSV/new_data_590&790_only.csv"

OUTPUT_MERGED_NO_590_790 = "data/CSV/merged_assignments_no_590_790.csv"
OUTPUT_MERGED_590_790 = "data/CSV/merged_assignments_590_790.csv"
OUTPUT_MERGED_590_AND_790 = "data/CSV/merged_assignments_590&790_only.csv"
OUTPUT_NEW_DATA_CSV = "data/CSV/new_data.csv"
OUTPUT_SCHEDULE_OUTPUT = "data/CSV/schedule_output.csv"
OUTPUT_COPIED_SCHEDULE = "data/Output/schedule_output.csv"
OUTPUT_GOOGLE_CALENDAR_UNDERGRAD = "data/Output/google_calendar_undergraduate.csv"
OUTPUT_GOOGLE_CALENDAR_GRADUATED = "data/Output/google_calendar_graduated.csv"
OUTPUT_UNASSIGNED_COURSES = "data/Output/unassigned_courses.csv"
OUTPUT_SKIPPED_FACULTY = "data/Output/skipped_faculty.csv"
OUTPUT_ROOM_CSV = "data/CSV/room.csv"
OUTPUT_TOP_COURSES = "data/CSV/top_courses_per_instructor_clean.csv"
OUTPUT_FACULTY_PREF = "data/CSV/faculty_time_preferences.csv"

# Scripts
CONVERT_CLASSROOM_SCRIPT = "scheduler/convert_classroom_to_room_csv.py"
EXTRACT_TOP_COURSES_SCRIPT = "scheduler/extract_and_clean_top_courses.py"
EXTRACT_TIME_SLOTS_SCRIPT = "scheduler/extract_faculty_time_slots.py"
GENERATE_NO_590_790_SCRIPT = "scheduler/generate_assignments_no_590_790.py"
GENERATE_590_790_SCRIPT = "scheduler/generate_assignments_590_790.py"
GENERATE_590_AND_790_SCRIPT = "scheduler/generate_assignments_590&790.py"
CHECK_UNASSIGNED_SCRIPT = "scheduler/check_unassigned_courses.py"
SCHEDULE_SCRIPT = "scheduler/schedule.py"
SPLIT_590_790_SCRIPT = "scheduler/split_590_790.py"
COPY_SCHEDULE_OUTPUT_SCRIPT = "scheduler/copy_schedule_output.py"
CONVERT_TO_CALENDAR_SCRIPT = "scheduler/convert_to_google_calendar.py"
