from pydantic import BaseModel

class Professor (BaseModel):
    name: str
    qualified_courses: list[str]
    availability: list
    max_classes: int