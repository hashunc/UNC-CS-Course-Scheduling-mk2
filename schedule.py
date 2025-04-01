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
        self.core_courses = []

        self.data = self.read_data(data_file)
        self.professors = self.data["ProfessorName"].unique().tolist()
        self.course_ids = self.data["CourseID"].tolist()
        self.secs = self.data["Sec"].tolist()
        self.all_courses = set(zip(self.course_ids, self.secs))

        self.rooms_data = self.read_rooms(rooms_file)
        self.room_ids = self.rooms_data["RoomID"].tolist()

        self.X = None
        self.prob = None
        self.valid_course_professor_pairs = None

        self.preference_time_penalties = {}
        self.preference_room_penalties = {}
        self.score_rank_penalties = {}
        self.score_penalty_coefficients = {}


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

        # create a set to record valid professor-course with scores higher than threshold
        self.valid_course_professor_pairs = set()
        for idx, row in self.data.iterrows():
            self.valid_course_professor_pairs.add((row["CourseID"], row["Sec"], row["ProfessorName"]))
        
        self.X = {
            (c, s, t, r, p): LpVariable(f"X_{c}_{s}_{t}_{r}_{p}", cat="Binary")
            for c, s in self.all_courses
            for t in self.time_slots
            for r in self.room_ids
            for p in self.professors
        }

        self.prob = LpProblem("Course_Scheduling", LpMinimize)
        self.prob += lpSum(
            self.X[c, s, t, r, p]
            for c, s in self.all_courses
            for t in self.time_slots
            for r in self.room_ids
            for p in self.professors
        )

        # Initialize penalty variables
        for idx, row in self.data.iterrows():
            key = (row["CourseID"], row["Sec"], row["ProfessorName"])
            self.preference_time_penalties[key] = LpVariable(
                f"TimePenalty_{row['CourseID']}_{row['Sec']}_{row['ProfessorName']}", 
                lowBound=0
            )
            self.score_rank_penalties[key] = LpVariable(
                f"ScorePenalty_{row['CourseID']}_{row['Sec']}_{row['ProfessorName']}", 
                lowBound=0
            )
            score = row['Ability'] + row['Willingness']
            penalty_coefficient = (10 - score) / 10
            self.score_penalty_coefficients[key] = penalty_coefficient

        # Use big weight 100 for preferences
        # self.prob += 100 * lpSum(self.preference_time_penalties.values())
        # self.prob += 100 * lpSum([self.score_penalty_coefficients[key] * self.score_rank_penalties[key] for key in self.score_rank_penalties])


    def add_course_assignment_constraints(self):
        """Add constraints to ensure every (course + sec) would be arranged to 1 time slot and 1 room and 1 professor at most."""
        """However, every (course) would be arranged at least once."""

        for (course_id, section) in self.all_courses:
            self.prob += lpSum(
                self.X[course_id, section, t, r, p] 
                for t in self.time_slots 
                for r in self.room_ids
                for p in self.professors
            ) <= 1
        

        unique_course_ids = set(c for c, s in self.all_courses)
        for course_id in unique_course_ids:
            sections = [s for c, s in self.all_courses if c == course_id]
            self.prob += lpSum(
                self.X[course_id, section, t, r, p]
                for section in sections
                for t in self.time_slots
                for r in self.room_ids
                for p in self.professors
            ) >= 1


    def add_professor_preference_constraints(self):
        """Add soft constraints for professor time slot preferences."""

        for idx, row in self.data.iterrows():
            c = row["CourseID"]
            s = row["Sec"]
            p = row["ProfessorName"]
            key = (c, s, p)
            
            # 获取教授偏好的时间段
            preferred_times = row["Professor_PreferredTimeSlots"].split(",") if "," in row["Professor_PreferredTimeSlots"] else [row["Professor_PreferredTimeSlots"]]
            
            # 检查课程是否被安排给这位教授
            assigned_to_this_professor = lpSum(
                self.X[(c, s, t, r, p)]
                for t in self.time_slots
                for r in self.room_ids
                if (c, s, t, r, p) in self.X
            )
            
            non_preferred_time_assignment = lpSum(
                self.X[(c, s, t, r, p)]
                for t in self.time_slots
                for r in self.room_ids
                if t not in preferred_times and (c, s, t, r, p) in self.X
            )
            
            self.prob += self.preference_time_penalties[key] >= non_preferred_time_assignment
            
            self.prob += self.preference_time_penalties[key] <= assigned_to_this_professor
        
        self.prob += 100 * lpSum(self.preference_time_penalties.values())


    def add_professor_zero_score_constraints(self):

        for c, s in self.all_courses:
            for p in self.professors:
                if (c, s, p) not in self.valid_course_professor_pairs:
                    for t in self.time_slots:
                        for r in self.room_ids:
                            self.prob += self.X[(c, s, t, r, p)] == 0
    

    def add_professor_scores_constraints(self):
        """
        添加基于教授能力和意愿分数的软约束
        课程未安排时，根据教授评分添加惩罚（评分越高惩罚越重）
        """
        
        # 按课程分组处理
        course_sections = {}
        for _, row in self.data.iterrows():
            c = row["CourseID"]
            s = row["Sec"]
            p = row["ProfessorName"]
            score = row['Ability'] + row['Willingness']
            
            key = (c, s)
            if key not in course_sections:
                course_sections[key] = []
            course_sections[key].append((p, score))
        
        # 对每门课程处理
        for (c, s), professors in course_sections.items():
            # 检查此课程是否被安排（到任何教授）
            course_assigned = lpSum(
                self.X[(c, s, t, r, prof)]
                for t in self.time_slots
                for r in self.room_ids
                for prof in self.professors
                if (c, s, prof) in self.valid_course_professor_pairs and (c, s, t, r, prof) in self.X
            )
            
            # 为每个教授添加惩罚项
            for p, score in professors:
                if (c, s, p) not in self.valid_course_professor_pairs:
                    continue
                    
                # 计算归一化权重（高分高惩罚）
                max_score = 10  # 假设最大分数为10
                penalty_weight = score / max_score
                
                # 当课程未被安排时，添加基于教授评分的惩罚
                # 即 1 - course_assigned = 1 时（课程未安排）
                self.prob += self.score_rank_penalties[(c, s, p)] >= penalty_weight * (1 - course_assigned)
                
                # 确保惩罚上限
                self.prob += self.score_rank_penalties[(c, s, p)] <= 1 - course_assigned
            
        # 将惩罚项加入目标函数
        self.prob += 100 * lpSum(self.score_rank_penalties.values())


    def add_section_time_constraints(self):
        """Add constraints to prevent different sections of the same course 
        from being scheduled at the same time."""

        for c in set(self.course_ids):
            for t in self.time_slots:
                self.prob += lpSum(
                    self.X[c, s, t, r, p] 
                    for s in self.data[self.data["CourseID"] == c]["Sec"] 
                    for r in self.room_ids
                    for p in self.professors
                ) <= 1

    
    def add_room_time_constraints(self):
        """Add constraints to prevent multiple courses from being scheduled in the same room at the same time."""
        
        # 对于每个房间和每个时间段
        for r in self.room_ids:
            for t in self.time_slots:
                # 确保在任何给定的时间段，一个房间最多只能安排一门课
                self.prob += lpSum(
                    self.X[(c, s, t, r, p)]
                    for c in self.course_ids
                    for s in self.secs
                    for p in self.professors
                    if (c, s, t, r, p) in self.X
                ) <= 1


    def add_professor_time_constraints(self):
        """Add constraints to prevent a professor from teaching multiple courses at the same time."""

        for p in self.professors:
            for t in self.time_slots:
                # 确保在任何给定的时间段，一位教授最多只能教一门课
                self.prob += lpSum(
                    self.X[(c, s, t, r, p)]
                    for c in self.course_ids
                    for s in self.secs
                    for r in self.room_ids
                    if (c, s, t, r, p) in self.X
                ) <= 1


    def add_specific_course_constraints(self):
        """Add constraints that Courses 301 and 211 cannot be scheduled at the same time."""

        for t in self.time_slots:
            self.prob += (
                lpSum(
                    self.X[c, s, t, r, p]
                    for c, s in self.all_courses
                    for r in self.room_ids
                    for p in self.professors
                    if c in [301, 211]
                ) <= 1
            )


    def add_mwf_course_constraints(self):
        """Add constraints for MWF courses. MoWeFr 3x50-min courses can only be scheduled in MoWe periods 
        (excluding Period 1 and Period 10)"""

        for c, s in self.all_courses:
            for t in self.time_slots:
                if "MWF" in t and (t.endswith("_1") or t.endswith("_10")):
                    for r in self.room_ids:
                        for p in self.professors:
                            self.prob += self.X[c, s, t, r, p] == 0


    def add_mw_course_constraints(self):
        """Add constraints for MW courses. MW 2x75-min courses must start in Periods 3, 5, 7, 9."""

        for c, s in self.all_courses:
            for t in self.time_slots:
                if "MW" in t and not any(t.endswith(f"_{period}") for period in [3, 5, 7, 9]):
                    for r in self.room_ids:
                        for p in self.professors:
                            self.prob += self.X[c, s, t, r, p] == 0

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
            self.X[c, s, t, r, p]
            for c, s in self.all_courses
            for t in self.time_slots
            for r in self.room_ids
            for p in self.professors
            if any(period in t for period in high_demand_periods)
        )

        # Add as a soft constraint that can be skipped if no solution is found
        self.prob += high_demand_courses <= max_allowed


    def add_core_course_constraints(self):
        """Add constraints to ensure core courses must be taught in a semester."""

        for c in self.core_courses:
            related_secs = [s for c_id, s in self.all_courses if c_id == c]
            if related_secs:  # Only add constraint if there are sections for this course
                self.prob += lpSum(
                    self.X[c, s, t, r, p] 
                    for s in related_secs 
                    for t in self.time_slots 
                    for r in self.room_ids
                    for p in self.professors
                ) >= 1


    def add_room_capacity_constraints(self):
        """Add constraints to ensure room capacity is sufficient for course enrollment."""

        for c, s in self.all_courses:
            course_capacity = self.data.loc[
                (self.data["CourseID"] == c) & (self.data["Sec"] == s), 
                "EnrollCapacity"
            ].values[0]
            
            for t in self.time_slots:
                for r in self.room_ids:
                    for p in self.professors:
                        # Check if the room capacity is smaller than enroll capacity of the course
                        if self.rooms_data.loc[self.rooms_data["RoomID"] == r, "Capacity"].values[0] < course_capacity:
                            self.prob += self.X[c, s, t, r, p] == 0


    def add_room_preference_constraints(self):
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
            (c, s) for c, s, t, r, p in self.X if self.X[c, s, t, r, p].varValue == 1
        )
        unassigned_courses = self.all_courses - assigned_courses

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
                    for p in self.professors:
                        if (c, s, t, r, p) in self.X and self.X[c, s, t, r, p].varValue == 1:
                            course = c
                            section = s
                            professor_name = p
                            formatted_time = f"{t}: {self.time_slot_mapping.get(t, t)}"
                            room = r
                            schedule.append([course, section, professor_name, formatted_time, room])

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

        # Initialize the LP problem
        self.initialize_problem()

        # Add constraints
        self.add_course_assignment_constraints()
        self.add_professor_zero_score_constraints()
        self.add_professor_scores_constraints()
        self.add_professor_preference_constraints()
        self.add_section_time_constraints()
        self.add_professor_time_constraints()
        self.add_room_time_constraints()
        self.add_specific_course_constraints()
        self.add_mwf_course_constraints()
        self.add_mw_course_constraints()
        self.add_high_demand_period_constraints()
        self.add_core_course_constraints()
        self.add_room_capacity_constraints()

        # Solve the problem
        success = self.solve_problem()
        
        # Check for unscheduled courses
        self.check_unscheduled_courses()
        
        # Generate and save the schedule
        return self.generate_schedule(output_file)


# Example usage
if __name__ == "__main__":
    data_file = "CSV/new_data.csv"
    rooms_file = "CSV/room.csv"
    output_file = "CSV/schedule_output.csv"
    
    scheduler = CourseScheduler(data_file, rooms_file)
    schedule = scheduler.schedule_courses(output_file)