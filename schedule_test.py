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
matching_files: Dict[str, tuple[Path, Path, Path]] = {
    name: (
        home / "test_data" / name,
        home / "target_data" / f"{name}.csv",
        home / "test_results" / f"{name}.csv",
    )
    for name in matching_names
}


# given outputted schedule and correct schedule, check if schedules are equivalent
def compare_output():
    for name in matching_names:
        case, target, result = matching_files[name]
        service = CourseScheduler(case / "data.csv", case / "room.csv")
        service.schedule_courses(case / "output.csv")
        diff = pd.read_csv(case / "output.csv").compare(pd.read_csv(target))
        with open(result, "w") as file:
            print(diff, file=file)
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
