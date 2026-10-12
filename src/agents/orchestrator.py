from crewai import Agent, LLM
from typing import List, Any

def create_orchestrator_agent(llm: LLM, tools: List[Any]) -> Agent:
    """Create the Orchestrator agent responsible for broad program scope and cross-syllabus relations."""
    return Agent(
        role="Academic Program Director & Curriculum Orchestrator",
        goal=(
            "Coordinate curriculum evaluation, analyze relationships and prerequisites between all courses "
            "in the academic program, and provide cross-syllabus contextual scoping for question generation."
        ),
        backstory=(
            "You are an esteemed university dean and curriculum architect. You have comprehensive authority "
            "and access across all syllabi within academic programs. When evaluating a topic, you identify "
            "the academic area it belongs to, how it connects to prior and subsequent courses, and frame "
            "the pedagogical scope for specialist curriculum analysts."
        ),
        tools=tools,
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
