from app.agents.extractor_atss import *
from crewai import Task,Crew

extractor = extractor_agent_ats()

def extractor_ats(resume,jd):
    task1 = Task(
        description=f"""Extract key structured information from both resume and job description:
Resume:
{resume}

JD:
{jd}""",
        expected_output=(
    "Return structured JSON with:\n"
    "- 'projects': List of {title, tools, outcome, duration}\n"
    "- 'experience': List of {role, company, outcome}\n"
    "- 'skills': List\n"
    "- 'jd': {requirements: List, responsibilities: List, bonus: List}"
    ),
        agent=extractor,
    )

    crew = Crew(
        agents=[extractor],
        tasks=[task1],
        verbose=False,
    )

    result = crew.kickoff()
    return result

