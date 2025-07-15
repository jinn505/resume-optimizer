from fastapi import FastAPI, UploadFile, File
from app.utils.file_parser import extract_text_from_pdf_file, load_jd
from app.final_optimizer import run_optimizer
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()


# Step 1: Define expected output structure
class ResumeSection(BaseModel):
    heading: str
    points: List[str] = Field(..., min_items=3, max_items=3)

class ResumeOutput(BaseModel):
    title: str
    sections: List[ResumeSection]

class OptimizedResumeWrapper(BaseModel):
    optimized_resume: ResumeOutput


# Step 2: Output parser
parser = PydanticOutputParser(pydantic_object=OptimizedResumeWrapper)


@app.post("/upload")
async def upload_details(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    # Extract resume and job description text
    resume_text = extract_text_from_pdf_file(resume)
    jd_text = await load_jd(jd)

    # Run CrewAI agents
    result = run_optimizer(resume_text, jd_text)

    # Get raw output from final agent
    raw_output = result.tasks_output[-1].raw

    # Parse and clean output
    try:
        structured_output = parser.parse(raw_output)
    except Exception as e:
        return {"error": "Parsing failed", "details": str(e), "raw_output": raw_output}

    return structured_output



