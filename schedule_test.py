from typing import Dict, List
from schedule import *
import pandas as pd
from pathlib import Path

home = Path(".")
testing_files: List[Path] = [
    home / "CSV" / "schedule_output.csv",
]
matching_names: List[str] = [
    "base_case",
]
matching_files: Dict[Path, Path] = {
    home / "test_data" / name: home / "target_data" / (name + ".csv")
    for name in matching_names
}


# given outputted schedule and correct schedule, check if schedules are equivalent
def compare_output():
    for case in matching_files:
        print([pd.read_csv(case / file) for file in ["data.csv", "room.csv"]])
        service = CourseScheduler(case / "data.csv", case / "room.csv")
        service.schedule_courses(case / "output.csv")
        diff = pd.read_csv(case / "output.csv").compare(
            pd.read_csv(matching_files[case])
        )
        print(diff)
        assert diff.empty


# read outputs into a data frame
def read_output() -> List[pd.DataFrame]:
    try:
        return [pd.read_csv(path) for path in testing_files]
    except:
        raise FileNotFoundError


# TODO: given outputted schedule and constraints, check if all constraints are satisfied
def constraints() -> None:
    for schedule in read_output():
        for item in schedule:
            pass


def test_schedule_courses():
    compare_output()
