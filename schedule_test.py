from typing import Dict, List
from schedule import *
import pandas as pd
from pathlib import Path

home = Path.cwd()
testing_files: List[Path] = [
    home / "CSV" / "schedule_output.csv",
]
matching_names: List[str] = [
    "base_case.csv",
]
matching_files: Dict[Path, Path] = {
    home / "test_data" / name: home / "target_data" / name for name in matching_names
}


# read outputs into a data frame
def read_output() -> List[pd.DataFrame]:
    try:
        return [pd.read_csv(path) for path in testing_files]
    except:
        raise FileNotFoundError


# given outputted schedule and constraints, check if all constraints are satisfied
def test_constraints() -> None:

    for schedule in read_output():
        for item in schedule:
            pass


# given outputted schedule and correct schedule, check if schedules are equivalent
def test_compare_output():
    return


def test_schedule_courses():
    return
