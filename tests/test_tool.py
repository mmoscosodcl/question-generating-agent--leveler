import json
import pytest
from src.tools.syllabus_tool import SyllabusTool

def test_syllabus_tool_mock_program():
    tool = SyllabusTool()
    raw = tool._run(program_name="Computer Science")
    data = json.loads(raw)

    assert "program_name" in data
    assert data["program_name"] == "Computer Science"
    assert "courses" in data
    assert len(data["courses"]) >= 2

def test_syllabus_tool_mock_topic():
    tool = SyllabusTool()
    raw = tool._run(program_name="Computer Science", topic="Normalization")
    data = json.loads(raw)

    assert "program_name" in data
    assert "target_topic" in data
    assert data["target_topic"] == "Normalization"
    assert "matches" in data
    matches = data["matches"]
    assert isinstance(matches, list)
    assert len(matches) > 0
    first_match = matches[0]
    assert "CS-301" in first_match["course_code"]
    assert "competencies" in first_match["topic_details"]

def test_syllabus_tool_unknown_program():
    tool = SyllabusTool()
    raw = tool._run(program_name="Astrophysics 999")
    data = json.loads(raw)

    assert "error" in data
    assert "available_programs" in data
