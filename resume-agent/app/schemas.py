from pydantic import BaseModel,Field
from typing import List


class ResumeSection(BaseModel):
    heading: str
    points: List[str] = Field(..., min_items=1, max_items = 3)

class ResumeOutput(BaseModel):
    title: str
    sections: List[ResumeSection]

class OptimizedResumeWrapper(BaseModel):
    optimized_resume: ResumeOutput

class ATSinput(BaseModel):
    resume : str
    jd : str

class ATSoutput(BaseModel):
    score : dict
    insights : dict        