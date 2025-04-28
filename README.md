# UNC COMP Course Scheduler

The **UNC COMP Course Scheduler** is an application developed to assist our client, Professor Montek Singh, with automating the course scheduling process for the UNC Computer Science Department.

It collects faculty teaching preferences, course assignments, section capacities, and availability constraints from multiple input spreadsheets. Using this data, it generates an optimized course schedule that assigns instructors to sections while balancing departmental needs and individual faculty requests.

The final output is a formatted `.csv` file that can be directly imported into Google Calendar, allowing faculty and staff to easily view and manage scheduled courses. 

This tool significantly reduces the manual workload involved in course scheduling and ensures a more organized, transparent, and data-driven process.

## Screenshots
<img width="1278" alt="image" src="https://github.com/user-attachments/assets/6142936d-807b-4cc6-973b-66c9297ae0eb" />

---

## Getting Set Up

If you want to run this application locally, here are the following steps to do so:

0. **Environment Setup**: Be sure you have the following installed on your local machine
    - Visual Studio Code
    - Python 3
    - Git
1. **Install Necessary Libraries/Dependencies**: In a terminal, be sure to run these commands

```bash
pip install pulp
```

2. **Git Clone**: Clone this repository into your local machine using this command

```bash
git clone https://github.com/hashunc/UNC-CS-Course-Scheduling-mk2.git
```

## Preparation Before Running the Program

After cloning the repository, navigate to the `UNC-CS-Course-Scheduling-mk2/` folder on your local machine.

Inside this folder, open the `data/` directory.  
You should see three subfolders:

- `Input/` — for storing input spreadsheets (e.g., faculty preferences, availability)
- `Output/` — where the generated output files will be saved
- `CSV/` — for storing intermediate CSV files
- <img width="647" alt="image" src="https://github.com/user-attachments/assets/b8bb127c-4bae-4113-8289-d9ddede45757" />


Make sure the required input files are correctly placed inside the `Input/` folder before running the program.

---
   
   


5. **Browser**: In your browser of choice, navigate to <ins>http://127.0.0.1:5500/public/index.html</ins>

6. You should be all set!
