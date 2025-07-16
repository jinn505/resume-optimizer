from fastapi import FastAPI, UploadFile, File,HTTPException
from app.utils.file_parser import extract_text_from_pdf_file, load_jd
from app.final_optimizer_candidate import run_optimizer
from langchain.output_parsers import PydanticOutputParser
from app.ats_agent.ats_scorer import *
from app.ats_agent.extractor_ats import *
from app.agents.extractor_atss import *
from app.schemas import *
import json,re

app = FastAPI()

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

@app.post("/ats-score",response_model = ATSoutput)
async def ats_calculator(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    try:
       resume_text = extract_text_from_pdf_file(resume)
       jd_text = await load_jd(jd)

       result = extractor_ats(resume_text,jd_text)
       raw_output = result.tasks_output[-1].raw if hasattr(result, "tasks_output") else str(result)
       json_match = re.search(r'\{[\s\S]*\}', raw_output)
       if not json_match:
            raise HTTPException(status_code=500, detail="Extractor JSON parsing failed.")

       extracted = json.loads(json_match.group(0))
    
       resume_skills = extracted.get("skills",[])
       resume_experience = extracted.get("experience", [])
       resume_projects = extracted.get("projects", [])
       resume_edu = extracted.get("education", "B.Tech") 

       jd_data = extracted.get("jd", {})
       jd_reqs = jd_data.get("requirements", [])
       jd_responsibilities = jd_data.get("responsibilities", [])
       jd_bonus = jd_data.get("bonus", [])

       print(resume_skills)
       print(jd_reqs + jd_bonus)


       skill_score , matched_skills, missing_skills = score_skills(resume_skills,jd_reqs + jd_bonus)
       experience_score = score_experience(resume_experience , jd_responsibilities + jd_bonus)
       education_score,ed_or_not = score_education(resume_edu,jd_reqs)
       projects_score = score_projects(resume_projects,jd_responsibilities + jd_reqs + jd_bonus)

       scores = {
        "skills" : round(skill_score*100,2),
        "experience" : round(experience_score*100,2),
        "projects" : round(projects_score*100,2),
        "education" : round(education_score*100,2)
      }
       

       final_score = final_ats_score(scores,ed_or_not)


       return {
        "score":{
        **scores,
        "final_ats_score" : final_score
        },

        "insights" : {
            "matched_skills" : matched_skills,
            "missing_skills" : missing_skills,
            "verdict" : "good" if final_score >=75 else "bad"
        }
       }
    
    except Exception as e:
        raise HTTPException(status_code=500 , detail = str(e))





    
    
    
    



