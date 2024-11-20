from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from algorithm import load_days, load_courses, load_meeting_patterns, load_professors, load_rooms, load_periods, run_scheduling_algorithm, load_manually_scheduled_classes


app = FastAPI()


@app.get("/")
def schedule_classes():
    manually_scheduled_classes: Optional[List[dict]] = None
    days = load_days()
    mwf_periods, tth_periods, mw_periods = load_periods()
    meeting_patterns =  load_meeting_patterns(mwf_periods, tth_periods, mw_periods)
    professors =  load_professors()
    courses =  load_courses()
    rooms =  load_rooms()

    try:
        # Run the scheduling algorithm
        results = run_scheduling_algorithm(
            days=days,
            meeting_patterns=meeting_patterns,
            professors=professors,
            courses=courses,
            rooms=rooms,
            manually_scheduled_classes=manually_scheduled_classes
        )
        print(results)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


