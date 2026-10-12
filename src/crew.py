import logging
from typing import Dict, Any
from crewai import LLM, Crew, Process, Task

from src.config import settings
from src.models.schema import AssessmentOutput
from src.tools.syllabus_tool import SyllabusTool
from src.agents import (
    create_orchestrator_agent,
    create_analyst_agent,
    create_specialist_agent,
)

logger = logging.getLogger(__name__)

def get_llm() -> LLM:
    """Instantiate the CrewAI LLM configured for local or self-hosted endpoint."""
    model_name = settings.LLM_MODEL_NAME
    # If using an OpenAI-compatible server (vLLM, LM Studio) that doesn't prefix with provider:
    if not model_name.startswith("ollama/") and not model_name.startswith("openai/"):
        model_string = f"openai/{model_name}"
    else:
        model_string = model_name

    return LLM(
        model=model_string,
        base_url=settings.LLM_BASE_URL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0.3
    )

def build_assessment_crew(topic: str, program_name: str, question_count: int = 3) -> Crew:
    """Build and configure the 3-agent CrewAI assessment generation workflow."""
    llm = get_llm()
    syllabus_tool = SyllabusTool()

    # Create Agents
    orchestrator = create_orchestrator_agent(llm=llm, tools=[syllabus_tool])
    analyst = create_analyst_agent(llm=llm, tools=[syllabus_tool])
    specialist = create_specialist_agent(llm=llm)

    # Task 1: Curriculum Scope & Cross-Syllabus Analysis (Orchestrator)
    orchestration_task = Task(
        description=(
            f"Review the academic program '{program_name}' and locate the syllabus containing the topic '{topic}'. "
            f"Use the Syllabus Fetcher Tool to inspect the program's courses. Determine which course this topic belongs to, "
            f"what prerequisites exist across other syllabi in the degree, and what subsequent courses build upon it. "
            f"Produce a curriculum overview that establishes the academic context and relationships between courses."
        ),
        expected_output=(
            "A curriculum context briefing containing the host course code/name, area of study, "
            "prior prerequisites from other syllabi, and downstream course connections."
        ),
        agent=orchestrator
    )

    # Task 2: Topic Competency Extraction (Curriculum Analyst)
    analyst_task = Task(
        description=(
            f"Analyze the specific syllabus unit for topic '{topic}' in '{program_name}'. "
            f"Using the Syllabus Fetcher Tool and the orchestrator's briefing, extract the explicit learning competencies, "
            f"Bloom's taxonomy cognitive levels (e.g. Apply, Analyze, Evaluate), and key conceptual boundaries. "
            f"Identify common student misconceptions that distractors in multiple-choice questions should target."
        ),
        expected_output=(
            "A pedagogical breakdown listing: target competencies, key concepts, Bloom cognitive depth, "
            "and common student misconceptions."
        ),
        agent=analyst
    )

    # Task 3: Assessment, Feedback & Feedforward Generation (Assessment Specialist)
    generation_task = Task(
        description=(
            f"Using the pedagogical breakdown and curriculum context, write exactly {question_count} high-quality "
            f"Multiple Choice Questions (MCQs) for the topic '{topic}'.\n\n"
            f"Each question must satisfy the following strict requirements:\n"
            f"1. 'id': A unique identifier (e.g., 'Q1', 'Q2', etc.).\n"
            f"2. 'question_text': A realistic, academically rigorous question stem testing analytical understanding.\n"
            f"3. 'options': A list of exactly 4 choices formatted as ['A) ...', 'B) ...', 'C) ...', 'D) ...'].\n"
            f"4. 'correct_answer': The exact string of the correct choice (e.g., 'B) ...').\n"
            f"5. 'feedback': Clear pedagogical justification explaining why the correct choice is valid and why the distractors are wrong.\n"
            f"6. 'feedforward': Constructive forward-looking advice referencing related concepts, questions, or future modules in the curriculum.\n\n"
            f"The final output must conform strictly to the AssessmentOutput schema with 'reviewing' explicitly set to False."
        ),
        expected_output=(
            f"A valid AssessmentOutput JSON containing {question_count} MCQs with correct answers, "
            f"feedback, feedforward, and reviewing set to False."
        ),
        agent=specialist,
        output_pydantic=AssessmentOutput
    )

    return Crew(
        agents=[orchestrator, analyst, specialist],
        tasks=[orchestration_task, analyst_task, generation_task],
        process=Process.sequential,
        verbose=True
    )
