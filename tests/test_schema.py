import json
import pytest
from src.models.schema import QuestionItem, AssessmentOutput

def test_question_item_valid():
    q = QuestionItem(
        id="Q1",
        question_text="What is the primary objective of 2NF?",
        options=[
            "A) Remove transitive dependencies",
            "B) Remove partial dependencies",
            "C) Remove multi-valued dependencies",
            "D) Ensure atomic values only"
        ],
        correct_answer="B) Remove partial dependencies",
        feedback="2NF eliminates partial dependencies by ensuring all non-key attributes are fully dependent on the primary key.",
        feedforward="Make sure to review composite keys before studying transitive dependencies in 3NF."
    )
    assert q.id == "Q1"
    assert len(q.options) == 4
    assert "partial dependencies" in q.correct_answer

def test_assessment_output_defaults():
    q = QuestionItem(
        id="Q1",
        question_text="Sample question",
        options=["A) 1", "B) 2", "C) 3", "D) 4"],
        correct_answer="A) 1",
        feedback="Sample feedback",
        feedforward="Sample feedforward"
    )
    assessment = AssessmentOutput(
        topic="Database Systems",
        program_context="Computer Science",
        questions=[q]
    )
    # Mandated business rule: reviewing must be False by default
    assert assessment.reviewing is False
    assert len(assessment.questions) == 1

def test_assessment_json_serialization():
    q = QuestionItem(
        id="Q1",
        question_text="Sample question",
        options=["A) Option A", "B) Option B", "C) Option C", "D) Option D"],
        correct_answer="A) Option A",
        feedback="Detailed feedback rationale.",
        feedforward="Study prerequisite chapter 3."
    )
    assessment = AssessmentOutput(
        topic="Relational Normalization",
        program_context="Computer Science - Databases",
        reviewing=False,
        questions=[q]
    )
    json_str = assessment.model_dump_json()
    data = json.loads(json_str)

    assert data["reviewing"] is False
    assert data["topic"] == "Relational Normalization"
    assert data["questions"][0]["id"] == "Q1"
    assert len(data["questions"][0]["options"]) == 4
