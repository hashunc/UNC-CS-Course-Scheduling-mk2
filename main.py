import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from algorithm import load_days, load_meeting_patterns, load_periods, create_professors_data, create_courses_data, create_rooms_data, run_scheduling_algorithm
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = "sqlite:///./database.db"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000/", "http://127.0.0.1:5500"],  # React app origin during development
    allow_credentials=True,
    allow_methods=[""],  # Allow all HTTP methods
    allow_headers=[""],  # Allow all HTTP headers
)

def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row  
    return connection

#General data dictionary and algorithm endpoints
@app.get("/")
def schedule_classes():
    manually_scheduled_classes = None
    days = load_days()
    mwf_periods, tth_periods, mw_periods = load_periods()
    meeting_patterns =  load_meeting_patterns(mwf_periods, tth_periods, mw_periods)
    professors =  create_professors_data()
    courses =  create_courses_data()
    rooms =  create_rooms_data()

    try:
        results = run_scheduling_algorithm(
            days=days,
            meeting_patterns=meeting_patterns,
            professors=professors,
            courses=courses,
            rooms=rooms,
            manually_scheduled_classes=manually_scheduled_classes
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
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
