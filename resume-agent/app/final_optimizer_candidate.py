from crewai import Crew, Task
from app.agents.analyzer import analyzer_agent
from app.agents.optimizer import optimizer_agent
from app.agents.writer import writer_agent
from app.agents.extractor import extractor_agent
from app.agents.refiner import refiner_agent  

def run_optimizer(resume: str, jd: str):
    extractor = extractor_agent()
    analyzer = analyzer_agent()
    optimizer = optimizer_agent()
    writer = writer_agent()
    refiner = refiner_agent()

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

    task2 = Task(
        description="Analyze the structured resume and JD to identify clear matches and gaps.",
        expected_output="JSON showing matching skills and responsibilities, and gaps that need to be addressed.",
        agent=analyzer,
    )

    task3 = Task(
    description="Based on the resume-JD matches and gaps, suggest strategies to better align the resume content with the job requirements.",
    expected_output="List of alignment strategies, such as keywords to emphasize or skills to highlight.",
    agent=optimizer,
    )


    task4 = Task(
    description="""Using the structured resume and JD analysis, generate up to 3 high-quality, non-redundant bullet points for each experience and project.

Each bullet point must:
- Mention specific tools, technologies, or techniques used
- Clearly describe the candidate’s unique contribution
- Include measurable outcomes where available
- Avoid vague phrasing like "collaborated", "communicated" unless critically necessary
- Avoid repeating similar points across different sections

Format your response in this JSON structure:
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
}""",
    expected_output="Crisp, specific, and technically-rich bullet points in the given JSON format.",
    agent=writer,
    )


    task5 = Task(
    description="""
Refine the given resume bullet points for clarity, strength, and alignment with job requirements.

Your goal is to:
- Make each bullet point more concise and impactful.
- Ensure each point is clearly aligned with industry hiring standards.
- Improve readability without changing meaning.

Maintain the same JSON structure:
{
  "optimized_resume": {
    "title": "Optimized Resume Bullet Points",
    "sections": [
      {
        "heading": "Project or Experience Name",
        "points": [
          "Refined bullet 1",
          "Refined bullet 2",
          "Refined bullet 3"
        ]
      },
      ...
    ]
  }
}
""",
    expected_output="Improved bullet points with enhanced clarity and alignment, in the same JSON structure.",
    agent=refiner,
    )

    crew = Crew(
        agents=[extractor, analyzer, optimizer, writer, refiner],
        tasks=[task1, task2, task3, task4,task5],
        verbose=True,
    )

    result = crew.kickoff()
    return result
