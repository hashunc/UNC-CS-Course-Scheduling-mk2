import pandas as pd
from pulp import LpProblem, LpVariable, LpMinimize, lpSum


class CourseScheduler:
    def __init__(self, data_file, rooms_file):
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
            "TTH_7": "5:00 – 6:15 p.m.",
        }
        self.data = self.read_data(data_file)
        self.rooms_data = self.read_rooms(rooms_file)
        self.prof_course_scores = None
        self.course_ids = None
        self.secs = None
        self.room_ids = None
        self.X = None
        self.prob = None
        self.preference_penalties = {}
        self.core_courses = []


    def expand_time_slots(self, time_slots):
        """Expand time slots with comma-separated values."""
        expanded_slots = []
        for slot in str(time_slots).split(";"):
            parts = slot.split("_")
            if len(parts) == 2 and "," in parts[1]:
                base = parts[0] + "_"
                expanded_slots.extend([base + num for num in parts[1].split(",")])
            else:
                expanded_slots.append(slot)
        return ";".join(expanded_slots)


    def read_data(self, data_file):
        """Read course data from CSV file."""
        
        print(f"Reading file: {data_file}")
        data = pd.read_csv(data_file)
        data.columns = data.columns.str.strip().str.replace(" ", "")
        data["Professor_PreferredTimeSlots"] = data["Professor_PreferredTimeSlots"].apply(
            self.expand_time_slots
        )
        return data


    def read_rooms(self, rooms_file):
        """Read room data from CSV file."""

        print(f"Reading file: {rooms_file}")
        data = pd.read_csv(rooms_file)
        data.columns = data.columns.str.strip().str.replace(" ", "")
        return data
    

    def initialize_problem(self):
        """Initialize the LP problem and decision variables."""

        self.X = {
            (c, s, t, r): LpVariable(f"X_{c}_{s}_{t}_{r}", cat="Binary")
            for c, s in zip(self.course_ids, self.secs)
            for t in self.time_slots
            for r in self.room_ids
        }

        self.prob = LpProblem("Course_Scheduling", LpMinimize)
        self.prob += lpSum(
            self.X[c, s, t, r] 
            for c, s in zip(self.course_ids, self.secs) 
            for t in self.time_slots 
            for r in self.room_ids
        )

        # Initialize preference penalty variables
        for idx, row in self.data.iterrows():
            self.preference_penalties[row["CourseID"], row["Sec"]] = LpVariable(
                f"Penalty_{row['CourseID']}_{row['Sec']}", 
                lowBound=0
            )

        # Use big weight 100 for preferences
        self.prob += 100 * lpSum(self.preference_penalties.values())


    def add_course_assignment_constraints(self):
        """Add constraints to ensure each course is assigned exactly once."""

        for idx, row in self.data.iterrows():
            # Make sure every course would be arranged to 1 time slot and 1 room
            self.prob += lpSum(
                self.X[row["CourseID"], row["Sec"], t, r] 
                for t in self.time_slots 
                for r in self.room_ids
            ) == 1


    def add_professor_preference_constraints(self):
        """Add soft constraints for professor time slot preferences."""

        for idx, row in self.data.iterrows():
            # Get preference and non-preference time slots
            preferred_times = row["Professor_PreferredTimeSlots"].split(";")
            non_preferred_times = [t for t in self.time_slots if t not in preferred_times]

            # If the professor has non-preference time slots
            if len(non_preferred_times) > 0:
                self.prob += lpSum(
                    self.X[row["CourseID"], row["Sec"], t, r] 
                    for t in non_preferred_times 
                    for r in self.room_ids
                ) <= self.preference_penalties[row["CourseID"], row["Sec"]]
                
            # If the professor has preference time slots
            if len(preferred_times) > 0:
                # Encourage to use preference time slots
                self.prob += lpSum(
                    self.X[row["CourseID"], row["Sec"], t, r] 
                    for t in preferred_times 
                    for r in self.room_ids
                ) + self.preference_penalties[row["CourseID"], row["Sec"]] >= 1


    def add_section_time_constraints(self):
        """Add constraints to prevent different sections of the same course 
        from being scheduled at the same time."""

        for c in set(self.course_ids):
            for t in self.time_slots:
                self.prob += lpSum(
                    self.X[c, s, t, r] 
                    for s in self.data[self.data["CourseID"] == c]["Sec"] 
                    for r in self.room_ids
                ) <= 1


    def add_professor_time_constraints(self):
        """Add constraints to prevent a professor from teaching multiple courses at the same time."""

        for professor in set(self.data["ProfessorName"]):
            for t in self.time_slots:
                self.prob += (
                    lpSum(
                        self.X[c, s, t, r]
                        for c, s in zip(self.course_ids, self.secs)
                        for r in self.room_ids
                        if self.data.loc[
                            (self.data["CourseID"] == c) & (self.data["Sec"] == s), "ProfessorName"
                        ].values[0] == professor
                    ) <= 1
                )


    def add_specific_course_constraints(self):
        """Add constraints that Courses 301 and 211 cannot be scheduled at the same time."""

        for t in self.time_slots:
            self.prob += (
                lpSum(
                    self.X[c, s, t, r]
                    for c, s in zip(self.course_ids, self.secs)
                    for r in self.room_ids
                    if c in [301, 211]
                ) <= 1
            )


    def add_mwf_course_constraints(self):
        """Add constraints for MWF courses. MoWeFr 3x50-min courses can only be scheduled in MoWe periods 
        (excluding Period 1 and Period 10)"""

        for c, s in zip(self.course_ids, self.secs):
            for t in self.time_slots:
                if "MWF" in t and (t.endswith("_1") or t.endswith("_10")):
                    for r in self.room_ids:
                        self.prob += self.X[c, s, t, r] == 0

    def add_mw_course_constraints(self):
        """Add constraints for MW courses. MW 2x75-min courses must start in Periods 3, 5, 7, 9."""

        for c, s in zip(self.course_ids, self.secs):
            for t in self.time_slots:
                if "MW" in t and not any(t.endswith(f"_{p}") for p in [3, 5, 7, 9]):
                    for r in self.room_ids:
                        self.prob += self.X[c, s, t, r] == 0

    def add_high_demand_period_constraints(self):
        """Add constraints to limit courses in high-demand periods. The number of courses scheduled 
        in MWF_4,5,6,7 / MW_3,4,5 / TTH_3,4,5 should be at most 65% of total courses."""

        high_demand_periods = [
            "MWF_4", "MWF_5", "MWF_6", "MWF_7",
            "MW_3", "MW_4", "MW_5",
            "TTH_3", "TTH_4", "TTH_5",
        ]
        total_courses = len(self.data)
        max_allowed = int(0.65 * total_courses)

        high_demand_courses = lpSum(
            self.X[c, s, t, r]
            for c, s in zip(self.course_ids, self.secs)
            for t in self.time_slots
            for r in self.room_ids
            if any(period in t for period in high_demand_periods)
        )

        # Add as a soft constraint that can be skipped if no solution is found
        self.prob += high_demand_courses <= max_allowed


    def add_core_course_constraints(self):
        """Add constraints to ensure core courses must be taught in a semester."""

        for c in self.core_courses:
            related_secs = [s for c_id, s in zip(self.course_ids, self.secs) if c_id == c]
            if related_secs:  # Only add constraint if there are sections for this course
                self.prob += lpSum(
                    self.X[c, s, t, r] 
                    for s in related_secs 
                    for t in self.time_slots 
                    for r in self.room_ids
                ) >= 1


    def add_room_time_constraints(self):
        """Add constraints to prevent multiple courses in the same room at the same time."""

        for t in self.time_slots:
            for r in self.room_ids:
                self.prob += lpSum(
                    self.X[(c, s, t, r)] 
                    for c, s in zip(self.data["CourseID"], self.data["Sec"])
                ) <= 1


    def add_room_capacity_constraints(self):
        """Add constraints to ensure room capacity is sufficient for course enrollment."""

        for c, s in zip(self.data["CourseID"], self.data["Sec"]):
            course_capacity = self.data.loc[
                (self.data["CourseID"] == c) & (self.data["Sec"] == s), 
                "EnrollCapacity"
            ].values[0]
            
            for t in self.time_slots:
                for r in self.room_ids:
                    # Check if the room capacity is smaller than enroll capacity of the course
                    if self.rooms_data.loc[self.rooms_data["RoomID"] == r, "Capacity"].values[0] < course_capacity:
                        self.prob += self.X[c, s, t, r] == 0


    def add_room_preference_constraints(self):
        # TODO
        return
    

    def add_professor_scores_constraints(self):
        # TODO
        return


    def solve_problem(self):
        """Attempt to solve the LP problem."""

        try:
            self.prob.solve()
            return True
        except Exception as e:
            print(f"Solver encountered an error: {e}")
            print("At most 65% in 11am-3pm failed, the program skipped constraint 7.")
            return False


    def check_unscheduled_courses(self):
        """Check and report any unscheduled courses."""

        assigned_courses = set(
            (c, s) for c, s, t, r in self.X if self.X[c, s, t, r].varValue == 1
        )
        all_courses = set(zip(self.course_ids, self.secs))
        unassigned_courses = all_courses - assigned_courses

        if unassigned_courses:
            print("The following courses are not scheduled:")
            for c, s in unassigned_courses:
                print(f"CourseID: {c}, Sec: {s}")
                
        return unassigned_courses


    def generate_schedule(self, output_file):
        """Generate and save the final schedule."""

        schedule = []
        for c, s in zip(self.course_ids, self.secs):
            for t in self.time_slots:
                for r in self.room_ids:
                    if self.X[c, s, t, r].varValue == 1:
                        professor_name = self.data.loc[
                            (self.data["CourseID"] == c) & (self.data["Sec"] == s), 
                            "ProfessorName"
                        ].values[0]
                        section = s
                        formatted_time = f"{t}: {self.time_slot_mapping.get(t, t)}"
                        room = r
                        schedule.append([c, section, professor_name, formatted_time, room])

        schedule_df = pd.DataFrame(
            schedule, columns=["CourseID", "Sec", "ProfessorName", "Time", "Room"]
        )
        schedule_df.drop_duplicates(inplace=True)

        # Save the schedule to a CSV file
        schedule_df.to_csv(output_file, index=False)
        print(f"Schedule saved to {output_file}")
        
        return schedule_df

    def schedule_courses(self, output_file):
        """Main method to schedule courses."""

        # Extract required data
        self.course_ids = self.data["CourseID"].tolist()
        self.secs = self.data["Sec"].tolist()
        self.room_ids = self.rooms_data["RoomID"].tolist()

        # Initialize the LP problem
        self.initialize_problem()

        # Add constraints
        self.add_course_assignment_constraints()
        self.add_professor_preference_constraints()
        self.add_section_time_constraints()
        self.add_professor_time_constraints()
        self.add_specific_course_constraints()
        self.add_mwf_course_constraints()
        self.add_mw_course_constraints()
        self.add_high_demand_period_constraints()
        self.add_core_course_constraints()
        self.add_room_time_constraints()
        self.add_room_capacity_constraints()

        # Solve the problem
        success = self.solve_problem()
        
        # Check for unscheduled courses
        self.check_unscheduled_courses()
        
        # Generate and save the schedule
        return self.generate_schedule(output_file)


# Example usage
if __name__ == "__main__":
    data_file = "CSV/data.csv"
    rooms_file = "CSV/room.csv"
    output_file = "CSV/schedule_output.csv"
    
    scheduler = CourseScheduler(data_file, rooms_file)
    schedule = scheduler.schedule_courses(output_file)