from numpy import ndarray
import pytest
import pandas as pd
from pathlib import Path
from datacompy import Compare

# TODO: fix import
from scheduler.schedule import CourseScheduler


# home of test input and target output
test_data = Path("./tests/test_data")

# provides case names
simple_cases = (
    "base_case",
    "core_case",
    "peak_case",
)


# creates separate tests for each case by parametrizing expected data and schedulers instantiated from each case's input data
@pytest.mark.parametrize(
    ("service", "expected"),
    (
        pytest.param(
            CourseScheduler(
                test_data / name / "data.csv",
                test_data / name / "room.csv",
            ),
            pd.read_csv(test_data / name / "output.csv"),
            id=name,
        )
        for name in simple_cases
    ),
)  # compares algorithm output with expected output for simple cases
def test_schedule_courses_output(service, tmp_path: Path, expected: pd.DataFrame):
    # get actual output and compare with expected
    out_path = tmp_path / "output.csv"
    service.schedule_courses(out_path)
    # upon failure, makes differences between actual and expected output available
    actual = pd.read_csv(out_path)
    if not expected.equals(actual):
        diff = Compare(
            expected,
            actual,
            join_columns=["CourseID", "Sec"],
            df1_name="Expected",
            df2_name="Actual",
        )
        pytest.fail(
            reason=f"Actual output does not match expected, differences:\n{diff.report()}"
        )


# provides case names
full_scale_cases = ()


# parametrizes case data as above, but for the whole class
@pytest.mark.parametrize(
    ("data_file", "rooms_file"),
    (
        pytest.param(
            (
                test_data / name / "data.csv",
                test_data / name / "room.csv",
            ),
            id=name,
        )
        for name in full_scale_cases
    ),
)
class TestConstraints:
    out: pd.DataFrame

    # scheduling output as DataFrame fixture
    @pytest.fixture(autouse=True, scope="class")
    def output(self, data_file, rooms_file, tmp_path: Path):
        service = CourseScheduler(data_file, rooms_file)
        output_path = tmp_path / "output.csv"
        service.schedule_courses(output_path)
        self.out = pd.read_csv(output_path)

    # room and data fixtures
    @pytest.fixture(scope="class")
    def data(self, data_file):
        yield pd.read_csv(data_file)

    @pytest.fixture(scope="class")
    def rooms(self, rooms_file):
        yield pd.read_csv(rooms_file)

    @pytest.fixture(scope="class")
    def profs(self):
        yield self.out["ProfessorName"].unique()

    # the following tests check whether:
    # any professor has two classes scheduled concurrently
    def test_prof_conflict(self, profs: ndarray):
        for prof in profs:
            teaching_time = self.out["Time", self.out["ProfessorName"] == prof]
            duplicates = teaching_time[teaching_time.duplicated()]
            if not duplicates.empty:
                pytest.fail(reason=f"Professor {prof} is double booked: \n{duplicates}")
            # TODO: add MW and 2H checks

    # TODO: any professor is scheduled for a class or at a time they cannot teach
    def test_prof_can_teach(self, data: pd.DataFrame): ...

    # TODO: any room has two classes scheduled concurrently
    def test_room_conflict(self): ...

    # TODO: any duplicate class sections are scheduled
    def test_section_conflict(self): ...

    # TODO: all core classes have at least one section scheduled (how to get core reqs?)
    def test_core_requirements(self): ...
