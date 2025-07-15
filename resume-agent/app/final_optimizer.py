from crewai import Crew, Task
from app.agents.analyzer import analyzer_agent
from app.agents.optimizer import optimizer_agent
from app.agents.writer import writer_agent

def run_optimizer(resume:str,jd:str):
    analyzer = analyzer_agent()
    optimizer = optimizer_agent()
    writer = writer_agent()

    task1 = Task(
        description=f"Analyze the resume:\n{resume}",
        expected_output="Structured summary of resume in JSON.",
        agent=analyzer,
    )

    task2 = Task(
    description=(
        f"Match and highlight how each project, internship, or experience in the resume relates to the following job description:\n{jd}"
    ),
    expected_output="Alignment analysis between resume experiences and JD, categorized by each item.",
    agent=optimizer,
    )


    task3 = Task(
    description="""
Your job is to extract **exactly 3 valuable and concise bullet points for each project, internship, or work experience** found in the resume and align them with the job description.

⚠️ Follow this output format strictly (in JSON):
{
  "optimized_resume": {
    "title": "Optimized Resume Bullet Points",
    "sections": [
      {
        "heading": "Project or Experience Name",
        "points": [
          "Bullet point 1",
          "Bullet point 2",
          "Bullet point 3"
        ]
      },
      ...
    ]
  }
}

🔁 For each project or experience, detect its title and return exactly 3 crisp bullet points only.

❌ Do NOT return raw resume JSON
❌ Do NOT return general paragraphs
❌ Do NOT return anything outside the JSON format above
""",
    expected_output="JSON with 'title' and 'sections'; each section has a 'heading' and list of 3 bullet 'points'.",
    agent=writer,
    )




    crew = Crew(
        agents=[analyzer,optimizer,writer],
        tasks = [task1,task2,task3],
        verbose=True
    )
    
    result = crew.kickoff()
    return result