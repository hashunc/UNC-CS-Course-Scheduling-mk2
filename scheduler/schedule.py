from typing import Dict, List, MutableSet
import pandas as pd
import pulp
from pulp import LpProblem, LpVariable, LpMinimize, lpSum
from pathlib import Path


class CourseScheduler:
    def __init__(self, data_file, rooms_file):
        self.time_slots = [
            "MWF_1", "MWF_2", "MWF_3", "MWF_4", "MWF_5", "MWF_6", "MWF_7", "MWF_8", "MWF_9", "MWF_10",
            "MW_12", "MW_34", "MW_56", "MW_78", "MW_90",
            "TTH_1", "TTH_2", "TTH_3", "TTH_4", "TTH_5", "TTH_6", "TTH_7",
            "2H_M", "2H_T", "2H_W", "2H_TH", "2H_F"
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
            "MW_12": "8:00 – 9:15 a.m.",
            "MW_34": "10:10 – 11:25 p.m.",
            "MW_56": "12:20 – 1:35 p.m.",
            "MW_78": "2:30 – 3:45 p.m.",
            "MW_90": "4:40 – 5:55 p.m.",
            "TTH_1": "8:00 – 9:15 a.m.",
            "TTH_2": "9:30 – 10:45 a.m.",
            "TTH_3": "11:00 – 12:15 p.m.",
            "TTH_4": "12:30 – 1:45 p.m.",
            "TTH_5": "2:00 – 3:15 p.m.",
            "TTH_6": "3:30 – 4:45 p.m.",
            "TTH_7": "5:00 – 6:15 p.m.",
            "2H_M": "9:00 – 11:00 a.m.",
            "2H_T": "9:00 – 11:00 a.m.",
            "2H_W": "9:00 – 11:00 a.m.",
            "2H_TH": "9:00 – 11:00 a.m.",
            "2H_F": "9:00 – 11:00 a.m."
        }

        self.data: pd.DataFrame = self.read_data(data_file)
        self.professors: str = self.data["ProfessorName"].unique().tolist()
        self.course_ids: List[str] = self.data["CourseID"].tolist()
        self.secs: List[str] = self.data["Sec"].tolist()
        self.all_courses: MutableSet[tuple[str, str]] = set(
            zip(self.course_ids, self.secs)
        )

        self.rooms_data: pd.DataFrame = self.read_rooms(rooms_file)
        self.room_ids: List[str] = self.rooms_data["RoomID"].tolist()

        self.X: Dict[tuple, LpVariable]
        self.prob: LpProblem
        self.valid_course_professor_pairs: List[tuple[str, str, str]] = []
        self.professors_courses: Dict[str, List[tuple[str, str]]] = {}

        self.course_miss_penalties: Dict[str, LpVariable] = {}
        self.preference_time_penalties: Dict[tuple[str, str, str], LpVariable] = {}
        self.peak_penalties: Dict[str, LpVariable] = {}

        self.course_miss_weight = 900
        self.preference_time_weight = 100
        self.peak_weight = 1000

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
        data["Professor_PreferredTimeSlots"] = data[
            "Professor_PreferredTimeSlots"
        ].apply(self.expand_time_slots)
        return data

    def read_rooms(self, rooms_file):
        """Read room data from CSV file."""

        print(f"Reading file: {rooms_file}")
        data = pd.read_csv(rooms_file)
        data.columns = data.columns.str.strip().str.replace(" ", "")
        return data

    def initialize_problem(self):
        """Initialize the LP problem and decision variables."""

        print("Initialize Problem...")

        # create a list to record valid professor-course with scores higher than threshold
        for idx, row in self.data.iterrows():
            self.valid_course_professor_pairs.append(
                (row["CourseID"], row["Sec"], row["ProfessorName"])
            )
            if row["ProfessorName"] in self.professors_courses:
                self.professors_courses[row["ProfessorName"]].append(
                    (row["CourseID"], row["Sec"])
                )
            else:
                self.professors_courses[row["ProfessorName"]] = [
                    (row["CourseID"], row["Sec"])
                ]

        self.X = {
            (c, s, t, r, p): LpVariable(f"X_{c}_{s}_{t}_{r}_{p}", cat="Binary")
            for c, s, p in self.valid_course_professor_pairs
            for t in self.time_slots
            for r in self.room_ids
        }

        self.prob = LpProblem("Course_Scheduling", LpMinimize)

        # Initialize course missing penalty variables
        self.course_miss_penalties["miss"] = LpVariable(
            "course_missing", lowBound=0, cat="Integer"
        )
        # Initialize time preference penalty variables
        for c, s, p in self.valid_course_professor_pairs:
            self.preference_time_penalties[c, s, p] = LpVariable(
                f"TimePenalty_{c}_{s}_{p}", lowBound=0, cat="Binary"
            )
        # Initialize peak arrangements penalty variables
        self.peak_penalties["over"] = LpVariable(
            "peak_time_arrangements_over", lowBound=0, cat="Integer"
        )

    def add_course_assignment_constraints(self):
        """Add constraints to prevent course being arranged multiple times and rooms."""
        """Every course must be arranged."""

        for c, s, p in self.valid_course_professor_pairs:
            self.prob += (
                lpSum(
                    self.X[c, s, t, r, p]
                    for t in self.time_slots
                    for r in self.room_ids
                )
                == 1
            )

        # hard: every [course] would be arranged at least once.
        # unique_course_ids = set(c for c, s in self.all_courses)
        # for course_id in unique_course_ids:
        #     sections = [s for c, s, p in self.valid_course_professor_pairs if c == course_id]
        #     professors = [p for c, s, p in self.valid_course_professor_pairs if c == course_id]
        #     self.prob += lpSum(
        #         self.X[course_id, section, t, r, p]
        #         for section in sections
        #         for t in self.time_slots
        #         for r in self.room_ids
        #         for p in professors
        #     ) >= 1

    def add_section_time_constraints(self):
        """Add constraints to prevent different sections of the same course
        from being scheduled at the same time."""

        for c in set(self.course_ids):
            if c not in ["COMP 590", "COMP 790"]:
                for t in self.time_slots:
                    self.prob += (
                        lpSum(
                            self.X[c, s, t, r, p]
                            for s in self.data[self.data["CourseID"] == c]["Sec"]
                            for r in self.room_ids
                            for p in self.professors
                            if (c, s, p) in self.valid_course_professor_pairs
                        )
                        <= 1
                    )

    def add_professor_time_constraints(self):
        """Add constraints to prevent a professor from teaching multiple courses at the same time."""

        for p in self.professors:
            for t in self.time_slots:
                self.prob += (
                    lpSum(
                        self.X[(c, s, t, r, p)]
                        for c, s in self.professors_courses[p]
                        for r in self.room_ids
                    )
                    <= 1
                )

    def add_room_time_constraints(self):
        """Add constraints to prevent multiple courses from being scheduled in the same room at the same time."""

        for r in self.room_ids:
            for t in self.time_slots:
                self.prob += (
                    lpSum(
                        self.X[(c, s, t, r, p)]
                        for c, s, p in self.valid_course_professor_pairs
                    )
                    <= 1
                )

    def add_specific_course_constraints(self):
        """Add constraints that Courses 301 and 211 cannot be scheduled at the same time."""

        for t in self.time_slots:
            self.prob += (
                lpSum(
                    self.X[c, s, t, r, p]
                    for c, s, p in self.valid_course_professor_pairs
                    for r in self.room_ids
                    if c in ["COMP 301", "COMP 211"]
                )
                <= 1
            )

    def add_mwf_course_constraints(self):
        """Add constraints for MWF courses. MoWeFr 3x50-min courses can only be scheduled in MoWe periods
        (excluding Period 1 and Period 10)"""

        for c, s, p in self.valid_course_professor_pairs:
            for t in self.time_slots:
                if "MWF" in t and (t.endswith("_1") or t.endswith("_10")):
                    for r in self.room_ids:
                        self.prob += self.X[c, s, t, r, p] == 0

    def add_core_course_constraints(self):
        """Add constraints to ensure core courses must be taught in a semester."""

        core_courses = [
            "COMP 210",
            "COMP 211",
            "COMP 283",
            "COMP 301",
            "COMP 311",
            "COMP 455",
            "COMP 550",
        ]

        for c, s, p in self.valid_course_professor_pairs:
            self.prob += (
                lpSum(
                    self.X[c, s, t, r, p]
                    for t in self.time_slots
                    for r in self.room_ids
                    if c in core_courses
                )
                >= 1
            )

    def add_room_capacity_constraints(self):
        """Add constraints to ensure room capacity is sufficient for course enrollment, but the room can't be too empty."""

        other_rooms = ["ClassRoom1_200", "ClassRoom2_200", "ClassRoom3_200", "ClassRoom4_200", "ClassRoom5_200", "ClassRoom6_200", 
                       "ClassRoom1_250", "ClassRoom2_250", "ClassRoom3_250", "ClassRoom4_250", "ClassRoom5_250", "ClassRoom6_250", 
                       "ClassRoom1_300", "ClassRoom2_300", "ClassRoom3_300", "ClassRoom4_300", "ClassRoom5_300", "ClassRoom6_300"]

        for c, s, p in self.valid_course_professor_pairs:
            course_capacity = self.data.loc[
                (self.data["CourseID"] == c) & (self.data["Sec"] == s), "EnrollCapacity"
            ].values[0]
            for t in self.time_slots:
                for r in self.room_ids:
                    # check if the room capacity is smaller than enroll capacity of the course
                    if (
                        self.rooms_data.loc[
                            self.rooms_data["RoomID"] == r, "Capacity"
                        ].values[0]
                        < course_capacity
                    ):
                        self.prob += self.X[c, s, t, r, p] == 0
            # try our best to avoid arranging courses to non-CS buildings
            if course_capacity <= 128:
                self.prob += lpSum(
                    self.X[c, s, t, r, p]
                    for t in self.time_slots
                    for r in other_rooms
                ) == 0

    def add_same_pre_courses_constraints(self):
        """Add constraints to avoid courses with the same prerequisite being arranged at the same time."""

        for t in self.time_slots:
            self.prob += (
                lpSum(
                    self.X[c, s, t, r, p]
                    for c, s, p in self.valid_course_professor_pairs
                    for r in self.room_ids
                    if c in ["COMP 283", "COMP 210"]
                    or c in ["COMP 211", "COMP 301", "COMP 455", "COMP 550"]
                )
                <= 1
            )

        conflict_periods = [
            (["MWF_1", "MWF_2"], ["MW_12"]),
            (["MWF_3", "MWF_4"], ["MW_34"]),
            (["MWF_5", "MWF_6"], ["MW_56"]),
            (["MWF_7", "MWF_8"], ["MW_78"]),
            (["MWF_9", "MWF_10"], ["MW_90"]),
        ]

        for mwf_periods, mw_periods in conflict_periods:
            for r in self.room_ids:
                for mwf_period in mwf_periods:
                    self.prob += (
                        lpSum(
                            self.X[c, s, mwf_period, r, p]
                            for c, s, p in self.valid_course_professor_pairs
                            if c in ["COMP 283", "COMP 210"]
                            or c in ["COMP 211", "COMP 301", "COMP 455", "COMP 550"]
                        )
                        + lpSum(
                            self.X[c, s, mw_periods[0], r, p]
                            for c, s, p in self.valid_course_professor_pairs
                            if c in ["COMP 283", "COMP 210"]
                            or c in ["COMP 211", "COMP 301", "COMP 455", "COMP 550"]
                        )
                        <= 1
                    )

    def add_mw_mwf_time_constraints(self):
        """Add constraints to avoid courses with the same prerequisite being arranged at the same time."""
        conflict_periods = [
            (["MWF_1", "MWF_2"], ["MW_12"]),
            (["MWF_3", "MWF_4"], ["MW_34"]),
            (["MWF_5", "MWF_6"], ["MW_56"]),
            (["MWF_7", "MWF_8"], ["MW_78"]),
            (["MWF_9", "MWF_10"], ["MW_90"]),
        ]

        for mwf_periods, mw_periods in conflict_periods:
            for r in self.room_ids:
                for mwf_period in mwf_periods:
                    # constraint for the same room
                    self.prob += (
                        lpSum(
                            self.X[c, s, mwf_period, r, p]
                            for c, s, p in self.valid_course_professor_pairs
                        )
                        + lpSum(
                            self.X[c, s, mw_periods[0], r, p]
                            for c, s, p in self.valid_course_professor_pairs
                        )
                        <= 1
                    )

                    # constraint for the same professor
                    for p in self.professors:
                        self.prob += (
                            lpSum(
                                self.X[c, s, mwf_period, r, p]
                                for c, s in self.professors_courses[p]
                                for r in self.room_ids
                            )
                            + lpSum(
                                self.X[c, s, mw_periods[0], r, p]
                                for c, s in self.professors_courses[p]
                                for r in self.room_ids
                            )
                            <= 1
                        )

    def add_professor_preference_constraints(self):
        """Add soft constraints for professor time slot preferences."""

        preferred_times = {}

        for idx, row in self.data.iterrows():
            c = row["CourseID"]
            s = row["Sec"]
            p = row["ProfessorName"]
            key = (c, s, p)

            # get preferred time periods of every professor
            professor_preferred_times = (
                row["Professor_PreferredTimeSlots"].split(",")
                if "," in row["Professor_PreferredTimeSlots"]
                else [row["Professor_PreferredTimeSlots"]]
            )
            preferred_times[key] = professor_preferred_times

        # set preference time penalties with 0 or 1
        for c, s, p in self.valid_course_professor_pairs:
            disliked_times = [
                t for t in self.time_slots if t not in preferred_times[c, s, p]
            ]
            for t in disliked_times:
                self.prob += self.preference_time_penalties[(c, s, p)] >= lpSum(
                    self.X[c, s, t, r, p] for r in self.room_ids
                )
            self.prob += self.preference_time_penalties[(c, s, p)] <= lpSum(
                self.X[c, s, t, r, p] for t in disliked_times for r in self.room_ids
            )

        # soft constraint by penalty
        self.prob += self.preference_time_weight * lpSum(
            self.preference_time_penalties.values()
        )

    def add_course_miss_constraint(self):
        """Add soft constraints to encourage (not force) every [course+sec] to be arranged."""

        course_nums = len(self.valid_course_professor_pairs)

        # soft: encourage every course to be arranged by adding penalty to missing course.
        self.prob += (
            lpSum(
                self.X[c, s, t, r, p]
                for c, s, p in self.valid_course_professor_pairs
                for t in self.time_slots
                for r in self.room_ids
            )
            + self.course_miss_penalties["miss"]
            == course_nums
        )

        self.prob += self.course_miss_weight * self.course_miss_penalties["miss"]

    def add_peak_time_constraints(self):
        """Add constraints to limit courses in high-demand periods. The number of courses scheduled
        in MWF_4,5,6,7 / MW I don't know / TTH_3,4,5 should be at most 65% of total courses.
        """

        high_demand_periods = [
            "MWF_4",
            "MWF_5",
            "MWF_6",
            "MWF_7",
            "MW_34",
            "MW_56",
            "MW_78",
            "TTH_3",
            "TTH_4",
            "TTH_5",
        ]
        total_courses = len(self.valid_course_professor_pairs)
        max_allowed = int(0.65 * total_courses)

        high_demand_courses = lpSum(
            self.X[c, s, t, r, p]
            for c, s, p in self.valid_course_professor_pairs
            for t in self.time_slots
            for r in self.room_ids
            if any(period in t for period in high_demand_periods)
        )

        self.prob += high_demand_courses <= max_allowed

        # Add as a constraint that can be skipped if no solution is found
        # self.prob += self.peak_weight * self.peak_penalties["over"]

    def add_2Hclass_constraints(self):
        """Add constraints to a 2H-class to Professor Chaturvedi for 790-150."""

        class_2H_list = ["2H_M", "2H_T", "2H_W", "2H_TH", "2H_F"]
        conflict_periods = [
            (["2H_M"], ["MWF_2", "MWF_3", "MW_12", "MW_34"]),
            (["2H_T"], ["TTH_1", "TTH_2", "TTH_3"]),
            (["2H_W"], ["MWF_2", "MWF_3", "MW_12", "MW_34"]),
            (["2H_TH"], ["TTH_1", "TTH_2", "TTH_3"]),
            (["2H_F"], ["MWF_2", "MWF_3"])
        ]
        c_2H = "COMP 790"
        s_2H = 158

        p_2H = "Chaturvedi"
        class_2H_list = ["2H_M", "2H_T", "2H_W", "2H_TH", "2H_F"]

        conflict_periods = [
            (["2H_M"], ["MWF_2", "MWF_3", "MW_12", "MW_34"]),
            (["2H_T"], ["TTH_1", "TTH_2", "TTH_3"]),
            (["2H_W"], ["MWF_2", "MWF_3", "MW_12", "MW_34"]),
            (["2H_TH"], ["TTH_1", "TTH_2", "TTH_3"]),
            (["2H_F"], ["MWF_2", "MWF_3"]),
        ]

        self.prob += (
            lpSum(
                self.X[c_2H, s_2H, t, r, p_2H]
                for t in class_2H_list
                for r in self.room_ids
            )
            == 1
        )
        # constraint for the same room of conflicted time of 2H class
        for class_2H_periods, normal_periods in conflict_periods:
            for normal_t in normal_periods:
                for r in self.room_ids:
                    self.prob += (
                        lpSum(self.X[c_2H, s_2H, class_2H_periods[0], r, p_2H])
                        + lpSum(
                            self.X[c, s, normal_t, r, p]
                            for c, s, p in self.valid_course_professor_pairs
                        )
                        <= 1
                    )

        # constraint for other professors, they can't be arrange to 2H class
        for c, s, p in self.valid_course_professor_pairs:
            self.prob += (
                lpSum(
                    self.X[c, s, t, r, p]
                    for t in class_2H_list
                    for r in self.room_ids
                    if (c, s, p) != (c_2H, s_2H, p_2H)
                )
                == 0
            )

    def solve_problem(self):
        """Attempt to solve the LP problem."""

        try:
            self.prob.solve()
            print("======penalty sum======")
            print(pulp.value(self.prob.objective))
            print("======preference time penalty======")
            time_penalties: List[LpVariable] = [
                pulp.value(var) for var in self.preference_time_penalties.values()
            ]  # type:ignore
            time_penalty_sum = sum(time_penalties)
            print(time_penalty_sum)
            # print every course penalty
            for key, var in self.preference_time_penalties.items():
                if var.value() > 0:
                    print(f"{key}: {var.value()}")
            
            # print("======course miss penalty======")
            # for key, var in self.course_miss_penalties.items():
            #     print(f"{key}: {var.value() * self.course_miss_weight}")
            # print("======peak time penalty======")
            # for key, var in self.peak_penalties.items():
            #     print(f"{key}: {var.value() * self.peak_weight}")
            return True
        except Exception as e:
            print(f"Solver encountered an error: {e}")
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
                        if (c, s, t, r, p) in self.X and self.X[
                            c, s, t, r, p
                        ].varValue == 1:
                            course = c
                            section = s
                            professor_name = p
                            formatted_time = f"{t}: {self.time_slot_mapping.get(t, t)}"
                            room = r
                            enroll_capacity  = self.data.loc[
                                (self.data["CourseID"] == c) & (self.data["Sec"] == s), 
                                "EnrollCapacity"
                            ].values[0]
                            schedule.append([course, section, professor_name, formatted_time, room, enroll_capacity])

        schedule_df = pd.DataFrame(
            schedule, columns=["CourseID", "Sec", "ProfessorName", "Time", "Room", "Enroll Capacity"]
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
        self.add_professor_preference_constraints()
        self.add_section_time_constraints()
        self.add_professor_time_constraints()
        self.add_room_time_constraints()
        self.add_specific_course_constraints()
        self.add_mwf_course_constraints()
        self.add_room_capacity_constraints()
        self.add_same_pre_courses_constraints()
        self.add_mw_mwf_time_constraints()
        self.add_peak_time_constraints()
        self.add_2Hclass_constraints()
        # self.add_course_miss_constraint()
        # self.add_core_course_constraints()

        # Solve the problem
        success = self.solve_problem()

        # Check for unscheduled courses
        self.check_unscheduled_courses()

        # Generate and save the schedule
        return self.generate_schedule(output_file)


# Example usage
if __name__ == "__main__":
    data_file = Path(".") / "data" / "CSV" / "new_data.csv"
    rooms_file = Path(".") / "data" / "CSV" / "room.csv"
    output_file = Path(".") / "data" / "CSV" / "schedule_output.csv"

    scheduler = CourseScheduler(data_file, rooms_file)
    schedule = scheduler.schedule_courses(output_file)
