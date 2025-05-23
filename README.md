# UNC COMP Course Scheduler

The **UNC COMP Course Scheduler** is an application developed to assist our client, Professor Montek Singh, with automating the course scheduling process for the UNC Computer Science Department.

It collects faculty teaching preferences, course assignments, section capacities, and availability constraints from multiple input spreadsheets. Using this data, it generates an optimized course schedule that assigns instructors to sections while balancing departmental needs and individual faculty requests.

The final output is a formatted `.csv` file that can be directly imported into Google Calendar, allowing faculty and staff to easily view and manage scheduled courses. 

This tool significantly reduces the manual workload involved in course scheduling and ensures a more organized, transparent, and data-driven process.

## Screenshots
<img width="1278" alt="image" src="https://github.com/user-attachments/assets/6142936d-807b-4cc6-973b-66c9297ae0eb" />

## Step by Step video: How to run the code?
[![Watch the video](https://img.youtube.com/vi/MjxVMGTAMIo/0.jpg)](https://youtu.be/MjxVMGTAMIo)

---

## Step 1: Getting Set Up

If you want to run this application locally, here are the following steps to do so:

0. **Environment Setup**: Be sure you have the following installed on your local machine
    - Visual Studio Code
    - Python 3
    - Git
1. **Install Necessary Libraries/Dependencies**: In a terminal, be sure to run these commands

```bash
pip install pulp

pip install pandas

```

2. **Git Clone**: Clone this repository into your local machine using this command

```bash
git clone https://github.com/hashunc/UNC-CS-Course-Scheduling-mk2.git
```

## Step 2: Preparation Before Running the Program

1. **Folders you need to know about**

After cloning the repository, navigate to the `UNC-CS-Course-Scheduling-mk2/` folder on your local machine.

Inside this folder, open the `data/` directory.  
You should see three subfolders:

- `Input/` — for storing input spreadsheets (e.g., faculty preferences, availability)
- `Output/` — where the generated output files will be saved
- `CSV/` — for storing intermediate CSV files
- <img width="647" alt="image" src="https://github.com/user-attachments/assets/b8bb127c-4bae-4113-8289-d9ddede45757" />

Make sure the required input files are correctly placed inside the `Input/` folder before running the program.

2. **Provide the Required .xlsx Files for Input**

This program depends on **four mandatory `.xlsx` files** as input.  
All four files must be present in the `data/Input/` folder **before running the program**, and each file must strictly follow the required file naming conventions.

> ⚠️ **Important Requirements:**  
> - **All four input files are required.** Missing any file will cause the program to fail.  
> - **All files must be in `.xlsx` format.** Other formats such as `.csv` or `.xls` are not accepted.  
> - **Each file must use the exact preset filename.** Renaming files may result in errors during execution.

### Required Input Files

- `ClassEnrollCap.xlsx`
- `ClassRoom.xlsx`
- `FacultyQualificationPreference.xlsx`
- `Responses.xlsx`

Make sure the filenames match exactly, including capitalization and spelling.

## Step 3: Input File Descriptions

Below is a detailed explanation of each required input file:

### 1. `ClassEnrollCap.xlsx`

- **Purpose**:  
  Defines enrollment capacities for each offered course section. This file specifies how many students can enroll in each course section, which is crucial for balancing course demand and instructor assignments.

- **Key Information**:  
  - Course code (e.g., COMP 110, COMP 210)
  - Section number
  - Maximum number of students per section

- **Format Requirements**:

  1. **Normal Courses**  
     For standard undergraduate or graduate courses, enter the course number, section number, and the maximum number of students.

     **Correct Example**:
     ```
     110, 1, 200
     110, 2, 200
     110, 3, 110
     ```

  2. **590/790 Special Topics Courses**  
     For 590 or 790 level special topics courses:
     - The section number must be entered as a **regular number without leading zeros**.
     - For example, a course listed as "590-089" must be entered as `590, 89, 30`, **not** as `590, 089, 30`.

     **Correct Example**:
     ```
     590, 80, 30
     790, 6, 15
     ```

  3. **Combined 590&790 Courses**  
     Some 590 and 790 courses are cross-listed and share the same time slot and classroom.
     - Use `590&790` as the course code.
     - The section number is the shared section number.
     - The enrollment capacity is the **total combined** number of students for both 590 and 790 levels.

     **Correct Example**:
     ```
     590&790, 158, 30
     590&790, 175, 15
     590&790, 187, 15
     ```

- **Additional Notes**:
  - All entries must be in numeric format except for the special combined course code `590&790`.
  - Ensure there are no leading zeros (except where specified).
  - Be careful with formatting when editing the `.xlsx` file—Excel sometimes automatically adds formatting that could cause parsing issues.


### 2. `ClassRoom.xlsx`

- **Purpose**:  
  Contains information about available classrooms for scheduling.
- **Key Information**:  
  - Room names or IDs
  - Building locations
  - Seating capacity
    
- #### 1. How to add a new Classroom?
    - You can add any class room with any string.
- #### 2. Format Requirements?
    - 1) Do not change any title of original file.
    -  ![image](https://github.com/user-attachments/assets/a9a25ec1-fc01-4e6a-ab89-87efb91e2b1e)
    - 2) There are only 3 types of rooms: CS, campus, and backup (uppercase and lowercase letters matter!). For example, if you name a room 'cs' instead of 'CS', the program will crash.
    - 3) AvailableTimeSlots, You can type any period of time by strict formmat as following:
         - All (any period for that room)
         - MWF_1,2,3,4,5,6,7,8,9,10
         - MW_1,2,3,4,5,6,7
         - TTH_1,2,3,4,5,6,7
         - If a single room has multiple days with different available times, use ';' to separate the times. For example:
         For example,
        - ![image](https://github.com/user-attachments/assets/51123cba-3115-43c7-bb03-de9f25785ca0)


### 3. `FacultyQualificationPreference.xlsx`

- **Purpose**:  
  Records each faculty member's readiness and preference scores for courses they are qualified to teach.  
  This file helps determine which instructors are best suited for specific courses based on both qualification and teaching interest.

- **Key Information**:  
  - Faculty names
  - Course names
  - Readiness/qualification scores
  - Frequency or preference indicators

- **Description of Forms**:
  - This file is based on the original **Faculty Staff Qualifications + Preferences** form provided by Professor Montek Singh.
  - The structure and logic of the original table have been **fully retained**; no changes have been made.
  - Users are free to **add** or **remove** faculty members as needed.
  - All added or modified sheets must still comply with the required format for the system to function correctly.

- **Format Requirements**:
- 1. How to add a new faculty member?
  - Each faculty member must have their own sheet (worksheet) within the Excel file.
  - The **name of each sheet must be the faculty member’s last name**.
    - This follows the naming style used in the original document to maintain consistency and reduce the information collection burden.
    - Our program explicitly requires the sheet names to match faculty last names when parsing the file.
  - **Special Case — Duplicate Last Names**:
    - If two or more faculty members share the same last name, use their **full name** in the format `LastNameFirstName` to create the sheet name.
    - Example:
      - Faculty 1: Tianlong Chen → Sheet name: `TianlongChen` (!!! NO SPACE !!!)
      - Faculty 2: Jackie Chen → Sheet name: `JackieChen`
    - In addition, when filling out the `Responses.xlsx` file, their `LastName` field must also be entered as `TianlongChen` and `JackieChen` respectively to ensure consistency.
    - After that, copy the temple of sheet, and paste it in new place.
- 2. Can I add a new course?
     - Yes, you can. However, please be sure to name them according to this format.
     ![CleanShot 2025-04-28 at 11 26 29@2x](https://github.com/user-attachments/assets/8e956cdc-01dc-4e63-a581-3c3784175260)

- 3. Can I add a new 590 or 790 course?
     - Yes, you can! However, please be sure to name them according to this format.
  ![CleanShot 2025-04-28 at 11 30 18@2x](https://github.com/user-attachments/assets/a5433f46-545e-46d7-bd98-d3bf8581baa6)

     As an example, Chen's sheet looks like this:
<img width="1333" alt="image" src="https://github.com/user-attachments/assets/21fa76f2-6a9f-42f7-9a86-d89b7c2f11b4" />

- 4. Can I add a new course with two sections combine with 590 and 790?
     - Yes, you can! However, please be sure to name them according to this format.
        - For example, In 2025 Fall, the professor Chaturvedi will teaching COMP 590&790-158 Special Topics: Special topics in Natural Language Processing.
          
    ![CleanShot 2025-04-28 at 11 38 20@2x](https://github.com/user-attachments/assets/21c78cca-7c4b-4c3c-abdf-f8610d921ee8)


- **Additional Notes**:
  - Sheet names and faculty identifiers must be consistent with **responses sheet** across all input files to avoid parsing errors.

> 📌 **Important:**  
> Failure to correctly name the sheets using either last names or full names (for duplicates) will cause the program to fail when loading preferences.


### 4. `Responses.xlsx`

- **Purpose**:  
  Captures faculty responses regarding their teaching availability, number of courses will teaching, and scheduling constraints for the semester.

- **Key Information**:  
  - Faculty names
  - Number of classes each faculty member plans to teach
  - Weekly time block availability (e.g., MWF_1, TTH_2)

- **How to Obtain**:
  - This file is generated from **Google Forms**.
  - Users should create and distribute a Google Form to all faculty members who are expected to teach in the upcoming semester.
  - Faculty members fill out the form, providing their teaching availability, desired course load, and any additional information.
  - After all responses have been collected:
    1. Download the Google Form responses as an `.xlsx` file (Excel Workbook format).
    2. Save the file as `Responses.xlsx`.
    3. Place it into the `data/Input/` directory.

- **Important Notes**:
  - Ensure that the faculty names listed in the `Responses.xlsx` match exactly with the sheet names or last names used in `FacultyQualificationPreference.xlsx`.
  - In cases where faculty members share the same last name (e.g., Tianlong Chen and Jackie Chen), use the full name format `LastNameFirstName` (e.g., `TianlongChen`, `JackieChen`) consistently across both files. Make sure the Lastname column is TianlongChen, and Lastname column is JackieChen.

- **Demo Video**:
[![Watch the Demo](https://img.youtube.com/vi/aI8CfDE8jHo/0.jpg)](https://youtu.be/aI8CfDE8jHo)

---
   
## Step 4: **Run the program**

After setting up the environment and preparing all required input files, you can run the program to generate the course schedule.

Follow these steps:

1. Navigate to the project root directory
   cd UNC-CS-Course-Scheduling-mk2
2. Run the program
    python scheduler/all_generate.py

Wait for the terminal to finish running, and the final result will be displayed in data/Output/.

## Step 5: **Check the Outputs**

After running the program, the following output files will be generated and saved in the `data/Output/` folder:

### Main Output Files

- `schedule_output.csv`  
  - The finalized, comprehensive course-to-instructor assignment schedule.
  - This file contains **the complete set of all course sections** offered in the semester, with each section assigned to an instructor based on their teaching preferences, qualifications, availability, and the department's scheduling needs.
  - Every course that was successfully matched to a faculty member will be listed, along with key details such as:
    - Course name and section number
    - Assigned instructor
    - Scheduled time block (if applicable)
    - Additional metadata (e.g., undergraduate/graduate level classification, enrollment capacity)
  - This file serves as the **authoritative source** for viewing the full scheduling results and can be used for administrative review, further processing, or archival purposes.

- `google_calendar_undergraduate.csv`  
  - A CSV file formatted specifically for importing **undergraduate course schedules** into Google Calendar.  
  - Includes course titles, meeting times, and assigned instructors.

- `google_calendar_graduated.csv`  
  - A CSV file formatted specifically for importing **graduate-level course schedules** into Google Calendar.  
  - Structured similarly to the undergraduate file but filtered for graduate courses.


### Diagnostic and Validation Files

- `missing_in_facultyqualification.csv`  
  - Lists courses that were showing in `Responses.xlsx` but missing from the `FacultyQualificationPreference.xlsx`.  

- `skipped_faculty.csv`  
  - Lists faculty members who could not be assigned any courses because they said teaching 0 course in `Responses.xlsx`

- `unassigned_courses.csv`  
  - Lists courses that could not be assigned to any faculty member.  
  - Useful for identifying gaps that may require manual adjustments or secondary assignment rounds.

> 📌 **Note:**  
> The Google Calendar CSV files can be directly imported into Google Calendar using the "Import" function for easy visualization and management of the final schedule.

## Step 6: Import .csv Files into Google Calendar

After generating the calendar-compatible `.csv` files (`google_calendar_undergraduate.csv` and `google_calendar_graduated.csv`), follow these steps to import them into Google Calendar:

1. Open [Google Calendar](https://calendar.google.com/) in your web browser.

2. On the left sidebar, find **"Other calendars"** and click the `+` button next to it.

3. Select **"Import"** from the dropdown menu.

4. In the Import window:
   - Click **"Select file from your computer"** and choose either `google_calendar_undergraduate.csv` or `google_calendar_graduated.csv`.
   - Choose which calendar you want to import the events into (you can create a new calendar for this if desired).

5. Click **"Import"**.

6. After the import finishes, all scheduled classes will appear in the selected calendar with their correct times, names, and instructors.

> 📌 **Note:**  
> - You may want to create separate calendars (e.g., "Undergraduate Courses", "Graduate Courses") to better organize the imported events.
> - Double-check that your local timezone settings in Google Calendar are correct before importing to avoid time shifts.

If you would like to see a complete walkthrough of setting up, running the program, and importing the `.csv` files into Google Calendar, please watch the demonstration video below:

[![Watch the Full Demo](https://img.youtube.com/vi/TNFIEQCRf88/0.jpg)](https://youtu.be/TNFIEQCRf88)
___
### Additional Step: About `config.py`

The `config.py` file is used to centralize and manage all important data file paths. While you can modify this file as needed, we **recommend only changing two specific things**:
- [![Watch the video](https://img.youtube.com/vi/X-YaTYNBN_w/0.jpg)](https://youtu.be/X-YaTYNBN_w)  

#### 1. Custom Input File Names

All input filenames in the `data/Input` folder can be renamed to suit your needs. This means you're **not restricted** to using the default file names.

For example, if you want to use a new file called `Responses_UNC.xlsx` for testing, you can update the line in `config.py` from:

```python
INPUT_AVAILABILITY = "data/Input/Responses.xlsx"
```

to:

```python
INPUT_AVAILABILITY = "data/Input/Responses_UNC.xlsx"
```

The same approach applies to the other input files (e.g., preferences, capacity, room files).

#### 2. Modifying the 2H Course Configuration

You can also update the configuration for a special 2-hour course by editing the course section ID and professor name in `config.py`.

If you choose to do this, **make sure you also update the following files accordingly** to ensure consistency:

- **`ClassEnrollCap.xlsx`**  
  → Make sure the section number matches your changes.

- **`FacultyQualificationPreference.xlsx`**  
  → The professor's last name must match exactly, and the course should comply with the predefined rules. Be sure the section number is consistent as well.

- **`Responses.xlsx`**  
  → Again, ensure that the professor’s last name exactly matches your updates.

Incorrect or inconsistent modifications in these files may result in errors or unexpected behavior during scheduling.


You are all set!
Thank you for using the UNC COMP Course Scheduler. 
This project aims to streamline and simplify the course assignment process for the department. 
Please refer to the full demonstration video above for a step-by-step guide on setting up and running the application.
