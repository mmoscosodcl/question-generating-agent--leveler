from typing import List, Optional
from pydantic import BaseModel, Field

class QuestionItem(BaseModel):
    """Schema for an individual multiple choice assessment question."""
    id: str = Field(description="Unique question identifier, e.g., 'Q1'")
    question_text: str = Field(description="The academic question stem")
    options: List[str] = Field(
        description="List of 4 distinct choices, formatted as ['A) ...', 'B) ...', 'C) ...', 'D) ...']"
    )
    correct_answer: str = Field(
        description="The correct option letter and text, e.g., 'A) First Normal Form'"
    )
    feedback: str = Field(
        description="Pedagogical explanation of why this answer is correct and why common misconceptions fail"
    )
    feedforward: str = Field(
        description="Forward-looking study guidance, prerequisite reinforcement, or explicit links to subsequent topics or related questions"
    )

class AssessmentOutput(BaseModel):
    """Schema for the complete academic assessment output."""
    topic: str = Field(description="The primary academic topic covered")
    program_context: str = Field(description="The academic program and course area where this syllabus resides")
    reviewing: bool = Field(default=False, description="State of review. Must default to False")
    questions: List[QuestionItem] = Field(description="List of generated assessment questions")

class SyllabusTopic(BaseModel):
    """Schema for a syllabus topic unit."""
    topic_id: str
    title: str
    competencies: List[str]
    bloom_level: str
    prerequisites: List[str]
    suggested_reading: Optional[str] = None

class SyllabusData(BaseModel):
    """Schema for a full academic course syllabus."""
    program_name: str
    course_code: str
    course_name: str
    description: str
    topics: List[SyllabusTopic]
