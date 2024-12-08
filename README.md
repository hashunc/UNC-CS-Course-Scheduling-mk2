# UNC COMP Course Scheduler

The UNC COMP Course Scheduler is an application that provides our client, Professor Montek Singh, an interface that generates a course schedule for the UNC Computer Science department based on the constraints that Professor Singh inputs. This application was possible by using JavaScript, HTML, CSS, the PuLP Linear Optimization library, and a SQLite3 based database.

## Pages

This application consists of the following pages:

1. **Login Page**: A simple way for Professor Singh to input the password to access the website.
2. **Home Page**: A page for Professor Singh to choose whether he wants to view the schedule that the algorithm has generated, edit the constraints such as professor's individual availabilities, course occupancy, room occupancies, etc. for the algorithm to run on, or manually edit the timigs and locations of certain classes.
3. **View Page**: A page where Professor Singh can choose whether he wants to view the schedule in a list view or calendar view.
4. **List View Page**: A page where Professor Singh can view the list of scheduled courses that the algorithm generated / Professor Singh manually adjusted in a tabular format.
5. **Edit Fields Page**: A page where Professor Singh can select whether he wants to update the properties for certain professors, courses, or rooms.
6. **Professors Edit Page**: A page where Professor Singh can edit the properties of each individual Computer Science department professor such as their qualified courses to teach, their availability, and the maximum number of classes they want to teach.
7. **Professors Edit Page**: A page where Professor Singh can edit the properties of each individual Computer Science course such as their sections and each section's maximum capacity.
8. **Rooms Edit Page**: A page where Professor Singh can edit the properties of each individual room in Sitterson/Fred Brooks or any university room such as their name and the room's occupancy.
9. **Update Schedule Page**: A page where Professor Singh can choose whether he wants to edit the course schedule in a list format or a calendar format.
10. **Update List View**: A page where Professor Singh can adjust the scheduling of courses manually in a list view.

## Getting Set Up

If you want to run this application locally, here are the following steps to do so:

0. **Environment Setup**: Be sure you have the following installed on your local machine
    - Visual Studio Code
    - Python 3
    - Git
1. **Install Necessary Libraries/Dependencies**: In a terminal, be sure to run these commands

```bash
pip install pulp
pip install fastapi
```

2. **Git Clone**: Clone this repository into your local machine using this command

```bash
git clone https://github.com/JustinIndla/COMP523.git
```

3. **Terminal Setup**: Start a new terminal in Visual Studio Code and run the command:

```bash
uvicorn main:app --reload
```

4. **Browser**: In your browser of choice, navigate to <ins>http://127.0.0.1:5500/public/index.html</ins>

5. You should be all set!