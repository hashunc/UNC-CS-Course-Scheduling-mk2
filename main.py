import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from algorithm import load_days, load_meeting_patterns, load_periods, create_professors_data, create_courses_data, create_rooms_data, run_scheduling_algorithm, create_manually_scheduled_data
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = "sqlite:///./database.db"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000/", "http://127.0.0.1:5500"],  # React app origin during development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row  
    return connection

@app.get("/run_alg")
def schedule_classes():
    manually_scheduled_classes = create_manually_scheduled_data()  
    days = load_days()
    mwf_periods, tth_periods, mw_periods = load_periods()
    meeting_patterns = load_meeting_patterns(mwf_periods, tth_periods, mw_periods)
    professors = create_professors_data()
    courses = create_courses_data()
    rooms = create_rooms_data()

    try:
        results = run_scheduling_algorithm(
            days=days,
            meeting_patterns=meeting_patterns,
            professors=professors,
            courses=courses,
            rooms=rooms,
            manually_scheduled_classes=manually_scheduled_classes,
        )

        print(results)

        if "schedule" not in results or not isinstance(results["schedule"], list):
            raise HTTPException(status_code=500, detail="Invalid schedule data returned")

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM CourseSchedule
        """)
        for course in results["schedule"]:
            if not isinstance(course, dict):
                raise ValueError(f"Unexpected course data structure: {course}")

            cursor.execute("""
                INSERT INTO CourseSchedule (Course, Section, Title, Prof, Start, MeetingPattern, SeatCapacity, Room, Type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, "AUTOMATED")
            """, (
                course.get("Course"),
                course.get("Section"),
                course.get("Title"),
                course.get("Professor"),
                course.get("Start Time"),
                course.get("Meeting Pattern"),
                course.get("Seat Capacity"),
                course.get("Room")
    
            ))

        # Commit changes
        connection.commit()

        # Return the results
        return {"message": "Schedule successfully updated", "results": results}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Ensure connection is always closed
        if connection:
            connection.close()
@app.get("/professors")
def get_professors():
    try: 
        results = create_professors_data()
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
@app.get("/courses")
def get_courses():
    try: 
        results = create_courses_data()
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
@app.get("/rooms")
def get_rooms():
    try: 
        results = create_rooms_data()
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
#Database CRUD Endpoints
@app.get("/schedule")
async def get_qcourse():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM CourseSchedule 
        """)
        courses = cursor.fetchall()
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    return courses

@app.get("/schedule/{course}-{section}")
async def get_course(course: str, section: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT * FROM CourseSchedule 
            WHERE Course = ? AND Section = ?
        """, (course, section))
        existing_row = cursor.fetchone()
        
        if not existing_row:
            raise HTTPException(status_code=404, detail="Course and section not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    return existing_row

@app.post("/schedule")
async def add_course(course:str, section:int, title:str = None, professor:str = None, start:str = None, meeting_pattern:str = None, capacity: str = None, room:str = None):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO CourseSchedule (Course, Section, Title, Prof, Start, MeetingPattern, SeatCapacity, Room, Type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            course,
            section,
            title,
            professor,
            start,
            meeting_pattern,
            capacity,
            room,
            'AUTOMATED'
        ))
        connection.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        connection.close()
    return f"Manual course added successfully course: {course}"

@app.put("/schedule/{course}-{section}")
async def update_course(
    course: str,
    section: int,
    title: str = None,
    professor: str = None,
    start: str = None,
    meeting_pattern: str = None,
    capacity: str = None,
    room: str = None,
):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Check if the course and section exist
        cursor.execute("""
            SELECT * FROM CourseSchedule
            WHERE Course = ? AND Section = ?
        """, (course, section))
        existing_row = cursor.fetchone()

        if not existing_row:
            print(existing_row)
            raise HTTPException(status_code=404, detail="Course and section not found")
        
        # Build the update query dynamically based on non-null parameters
        update_fields = []
        update_values = []

        if title is not None:
            update_fields.append("Title = ?")
            update_values.append(title)
        if professor is not None:
            update_fields.append("Prof = ?")
            update_values.append(professor)
        if start is not None:
            update_fields.append("Start = ?")
            update_values.append(start)
        if meeting_pattern is not None:
            update_fields.append("MeetingPattern = ?")
            update_values.append(meeting_pattern)
        if capacity is not None:
            update_fields.append("SeatCapacity = ?")
            update_values.append(capacity)
        if room is not None:
            update_fields.append("Room = ?")
            update_values.append(room)

        # Add the WHERE condition to the query
        update_query = f"""
            UPDATE CourseSchedule
            SET {", ".join(update_fields)}
            WHERE Course = ? AND Section = ?
        """
        update_values.extend([course, section])

        # Execute the update query
        cursor.execute(update_query, update_values)
        connection.commit()
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    return {"message": f"Course {course}, section {section} updated successfully."}

@app.delete("/schedule/{course}-{section}")
async def delete_course(course: str, section: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Check if the course and section exist
        cursor.execute("""
            SELECT * FROM CourseSchedule
            WHERE Course = ? AND Section = ?
        """, (course, section))
        existing_row = cursor.fetchone()

        if not existing_row:
            raise HTTPException(status_code=404, detail="Course and section not found")
        
        # Delete the course and section
        cursor.execute("""
            DELETE FROM CourseSchedule
            WHERE Course = ? AND Section = ?
        """, (course, section))
        connection.commit()
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    
    return f"Course {course}, section {section} has been deleted successfully."


class Course(BaseModel):
    Course: str
    Title: str
    Section: int
    SeatCapacity: int


@app.get("/courses/{course}-{section}")
async def get_course(course: str, section: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT * FROM CoursesAndSections 
            WHERE Course = ? AND Section = ?
        """, (course, section))
        existing_row = cursor.fetchone()
        
        if not existing_row:
            raise HTTPException(status_code=404, detail="Course and section not found")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    return existing_row

@app.post("/courses")
async def create_course(course: Course):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO CoursesAndSections (Course, Title, Section, SeatCapacity) 
            VALUES (?, ?, ?, ?)
        """, (course.Course, course.Title, course.Section, course.SeatCapacity))
        connection.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        connection.close()
    return {"Course": course.Course, "Title": course.Title, "Section": course.Section, "SeatCapacity": course.SeatCapacity}

@app.put("/courses/{course}-{section}")
async def update_course(course: str, section: str, course_data: Course):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM CoursesAndSections 
            WHERE Course = ? AND Section = ?
        """, (course, section))
        existing_row = cursor.fetchone()
        
        if not existing_row:
            raise HTTPException(status_code=404, detail="Course and section not found")
        cursor.execute("""
            UPDATE CoursesAndSections
            SET Title = ?, SeatCapacity = ?
            WHERE Course = ? AND Section = ?
        """, (course_data.Title, course_data.SeatCapacity, course, section))
        connection.commit()
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    
    return {
        "Course": course,
        "Section": section,
        "Updated Title": course_data.Title,
        "Updated SeatCapacity": course_data.SeatCapacity
    }


@app.put("/courses/{course}-{section}")
async def update_course(course: str, section: str, course_data: Course):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM CoursesAndSections 
            WHERE Course = ? AND Section = ?
        """, (course, section))
        existing_row = cursor.fetchone()
        
        if not existing_row:
            raise HTTPException(status_code=404, detail="Course and section not found")
        cursor.execute("""
            UPDATE CoursesAndSections
            SET Title = ?, SeatCapacity = ?
            WHERE Course = ? AND Section = ?
        """, (course_data.Title, course_data.SeatCapacity, course, section))
        connection.commit()
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    
    return {
        "Course": course,
        "Section": section,
        "Updated Title": course_data.Title,
        "Updated SeatCapacity": course_data.SeatCapacity
    }

@app.delete("/courses/{course}-{section}")
async def delete_course(course: str, section: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM CoursesAndSections
            WHERE Course = ? AND Section = ?
        """, (course, section))
        existing_row = cursor.fetchone()
        
        if not existing_row:
            raise HTTPException(status_code=404, detail="Course and section not found")
        
        # Delete the course
        cursor.execute("""
            DELETE FROM CoursesAndSections
            WHERE Course = ? AND Section = ?
        """, (course, section))
        connection.commit()
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    
    return {
        "Course": course,
        "Section": section,
        "Message": "Course and section deleted successfully"
    }

class QualifiedCourse(BaseModel):
    Professor: str
    Course: str

@app.get("/qualified/{professor}")
async def get_qcourse(professor: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT Course FROM QualifiedCourses 
            WHERE Prof = ?
        """, (professor,))
        courses = cursor.fetchall()
        
        if not courses:
            raise HTTPException(status_code=404, detail="No qualified courses found for the professor")
        
        # Extract course names from the result
        course_list = [course["Course"] for course in courses]
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    
    return course_list

@app.post("/qualified")
async def create_qcourse(qcourse: QualifiedCourse):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT Prof, Course 
            FROM QualifiedCourses 
            WHERE Prof = ? AND Course = ?
        """, (qcourse.Professor, qcourse.Course))
        existing_room = cursor.fetchone()
        if existing_room:
            raise HTTPException(status_code=400, detail=f"Course '{qcourse.Course}' already exists")
        cursor.execute("""
            INSERT INTO QualifiedCourses (Prof, Course) 
            VALUES (?, ?)
        """, (qcourse.Professor, qcourse.Course))
        connection.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        connection.close()
    return {"Professor": qcourse.Professor, "Course": qcourse.Course}


@app.delete("/qualified/{professor}")
async def delete_qcourse(qcourse:QualifiedCourse):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM QualifiedCourses
            WHERE Prof = ? AND Course = ?
        """, (qcourse.Professor, qcourse.Course))
        existing_row = cursor.fetchone()
        
        if not existing_row:
            raise HTTPException(status_code=404, detail="Course and section not found")
        
        # Delete the course
        cursor.execute("""
            DELETE FROM QualifiedCourses
            WHERE Prof = ? AND Course = ?
        """, (qcourse.Professor, qcourse.Course))
        connection.commit()
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    
    return {
        "Prfoessor": qcourse.Professor,
        "Course": qcourse.Course,
        "Message": "Qualified Course deleted successfully"
    }


@app.get("/max/{professor}")
async def get_max_course(professor: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT MaxCourses FROM MaxCourses 
            WHERE Prof = ?
        """, (professor,))
        max_courses = cursor.fetchone()
        
        if not max_courses:
            raise HTTPException(status_code=404, detail="No qualified courses found for the professor")
        max_courses = max_courses['MaxCourses']
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    
    return max_courses


@app.put("/max/{professor}")
async def update_max_course(professor: str, new_max:int):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT 1 FROM MaxCourses 
            WHERE Prof = ?
        """, (professor,))
        existing_professor = cursor.fetchone()
        if existing_professor is None:
            raise HTTPException(status_code=404, detail=f"Professor {professor} not found in Max Courses")

        cursor.execute("""
            UPDATE MaxCourses
            SET MaxCourses = ?
            Where Prof = ?
        """, (new_max,professor,))
        connection.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    return f" {professor}'s max has been updated to {new_max} classes."

@app.get("/rooms/{room}")
async def get_room_capacity(room:str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT SeatCapacity
            FROM Rooms
            WHERE Room = ?
        """, (room,))
        capacity = cursor.fetchone()
        capacity = capacity['SeatCapacity']
        if capacity is None:
            raise HTTPException(status_code=404, detail=f"Room '{room}' not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    return capacity

@app.post("/rooms/{room}")
async def create_room(room: str, capacity:int):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT Room 
            FROM Rooms 
            WHERE Room = ?
        """, (room,))
        existing_room = cursor.fetchone()
        if existing_room:
            raise HTTPException(status_code=400, detail=f"Room '{room}' already exists")
        cursor.execute("""
            INSERT INTO Rooms (Room, SeatCapacity) 
            VALUES (?, ?)
        """, (room, capacity))
        connection.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        connection.close()
    return {"Room": room, "Capacity": capacity}

@app.put("/room/{room}")
async def update_capacity(room, new_capacity):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT SeatCapacity FROM Rooms 
            WHERE Room = ?
        """, (room,))
        existing_professor = cursor.fetchone()
        if existing_professor is None:
            raise HTTPException(status_code=404, detail=f"Room {room} not found in Room List")

        cursor.execute("""
            UPDATE Rooms
            SET SeatCapacity = ?
            Where Room = ?
        """, (new_capacity,room,))
        connection.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    return f" {room}'s capacity has been updated to {new_capacity} seats."

@app.delete("/room/{room}")
async def delete_room(room: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM Rooms
            WHERE Room = ?
        """, (room,))
        existing_row = cursor.fetchone()
        
        if not existing_row:
            raise HTTPException(status_code=404, detail="Course and section not found")
        
        # Delete the course
        cursor.execute("""
            DELETE FROM Rooms
            WHERE Room = ? 
        """, (room,))
        connection.commit()
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    
    return {
        f"Room {room} deleted successfully"
    }

@app.get("/availability/{professor}")
async def get_professor_availability(professor: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT AvailableMp, AvailablePeriod FROM Availability 
            WHERE Prof = ?
        """, (professor,))
        availability = cursor.fetchall()
        
        if not availability:
            raise HTTPException(status_code=404, detail="No availability found for the professor")
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    
    return availability

@app.post("/availability/{professor}")
async def create_professor_availability(professor: str, AvailableMp:str, AvailablePeriod: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO Availability (Prof, AvailableMp, AvailablePeriod) 
            VALUES (?, ?, ?)
        """, (professor, AvailableMp, AvailablePeriod))
        connection.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        connection.close()
    return {"Professor": professor, "AvailableMP": AvailableMp, "AvailablePeriod": AvailablePeriod}

@app.delete("/availability/{professor}")
async def delete_professor_availability(professor: str, AvailableMp: str, AvailablePeriod: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT * 
            FROM Availability
            WHERE Prof = ? AND AvailableMp = ? AND AvailablePeriod = ?
        """, (professor, AvailableMp, AvailablePeriod))
        availability = cursor.fetchone()

        if not availability:
            raise HTTPException(status_code=404, detail="Availability not found for the given professor and time period")
        cursor.execute("""
            DELETE FROM Availability 
            WHERE Prof = ? AND AvailableMp = ? AND AvailablePeriod = ?
        """, (professor, AvailableMp, AvailablePeriod))
        connection.commit()

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        connection.close()

    return {f"Availability for Professor '{professor}' during MP '{AvailableMp}' and Period '{AvailablePeriod}' has been deleted"}

@app.get("/manual")
async def get_manual_courses():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM CourseSchedule 
            WHERE Type = 'MANUAL'
        """)
        courses = cursor.fetchall()
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    return courses


@app.get("/manual")
async def get_manual_courses():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM CourseSchedule 
            WHERE Type = 'MANUAL'
        """)
        courses = cursor.fetchall()
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        connection.close()
    return courses

@app.post("/manual")
async def add_manual_course(course:str, section:int, title:str = None, professor:str = None, start:str = None, meeting_pattern:str = None, capacity: str = None, room:str = None):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO CourseSchedule (Course, Section, Title, Prof, Start, MeetingPattern, SeatCapacity, Room, Type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            course,
            section,
            title,
            professor,
            start,
            meeting_pattern,
            capacity,
            room,
            'MANUAL'
        ))
        connection.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        connection.close()
    return f"Manual course added successfully", "course: {course}"

@app.delete("/manual/{course}/{section}")
async def delete_manual_course(course: str, section: int):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Check if the course and section exist in the database
        cursor.execute("""
            SELECT * FROM CourseSchedule 
            WHERE Course = ? AND Section = ? AND Type = 'MANUAL'
        """, (course, section))
        existing_course = cursor.fetchone()

        if not existing_course:
            raise HTTPException(
                status_code=404,
                detail=f"Manual course with Course '{course}' and Section '{section}' not found."
            )

        # Delete the manual course
        cursor.execute("""
            DELETE FROM CourseSchedule 
            WHERE Course = ? AND Section = ? AND Type = 'MANUAL'
        """, (course, section))
        connection.commit()

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        connection.close()

    return f"Manual course '{course}' with Section '{section}' has been deleted."



