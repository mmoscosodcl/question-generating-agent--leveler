from crewai import Agent, LLM
from typing import List, Any

def create_analyst_agent(llm: LLM, tools: List[Any]) -> Agent:
    """Create the Curriculum Analyst agent responsible for detailed syllabus and competency extraction."""
    return Agent(
        role="Curriculum Pedagogy Analyst",
        goal=(
            "Extract and structure the targeted syllabus unit, isolating key learning competencies, "
            "Bloom's taxonomy cognitive levels, prerequisite concepts, and conceptual boundaries for the topic."
        ),
        backstory=(
            "You are a rigorous educational measurement specialist and pedagogical analyst. Your expertise "
            "lies in parsing syllabus documentation, identifying specific cognitive skills students must master, "
            "and outlining common pitfalls and misconceptions related to each competency."
        ),
        tools=tools,
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
