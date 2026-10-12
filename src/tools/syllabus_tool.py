import json
import logging
from typing import Type, Optional, Dict, Any
import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from src.config import settings

logger = logging.getLogger(__name__)

# Sample multi-course syllabus database for offline testing & mock mode
MOCK_CURRICULUM_DATABASE: Dict[str, Dict[str, Any]] = {
    "computer science": {
        "program_name": "Computer Science",
        "courses": [
            {
                "course_code": "CS-301",
                "course_name": "Database Systems",
                "area": "Information Management",
                "description": "Relational data modeling, SQL optimization, ACID transactions, and normalization theory.",
                "topics": [
                    {
                        "topic_id": "CS301-T1",
                        "title": "Relational Database Normalization",
                        "competencies": [
                            "Distinguish between 1NF, 2NF, 3NF, and BCNF",
                            "Identify partial functional dependencies and transitive dependencies",
                            "Decompose unnormalized relations into lossless-join, dependency-preserving schemas"
                        ],
                        "bloom_level": "Analyze",
                        "prerequisites": ["Relational Algebra", "Primary and Foreign Key Definitions"],
                        "related_topics": ["CS301-T2: Transaction Management", "CS301-T3: Query Optimization"]
                    },
                    {
                        "topic_id": "CS301-T2",
                        "title": "Transaction Management and ACID Properties",
                        "competencies": [
                            "Explain Atomicity, Consistency, Isolation, and Durability",
                            "Analyze concurrency anomalies: dirty reads, non-repeatable reads, phantom reads",
                            "Implement two-phase locking (2PL) protocols"
                        ],
                        "bloom_level": "Evaluate",
                        "prerequisites": ["CS301-T1: Relational Database Normalization"],
                        "related_topics": ["CS301-T3: Query Optimization"]
                    }
                ]
            },
            {
                "course_code": "CS-302",
                "course_name": "Software Engineering Architecture",
                "area": "Systems Engineering",
                "description": "Design patterns, microservice architectures, API contracts, and distributed data systems.",
                "topics": [
                    {
                        "topic_id": "CS302-T1",
                        "title": "Microservices and Distributed Persistence",
                        "competencies": [
                            "Apply CQRS and Event Sourcing patterns",
                            "Evaluate trade-offs between monolithic databases and database-per-service"
                        ],
                        "bloom_level": "Evaluate",
                        "prerequisites": ["CS-301: Database Systems"],
                        "related_topics": ["CS301-T2: Transaction Management"]
                    }
                ]
            }
        ]
    },
    "data science": {
        "program_name": "Data Science",
        "courses": [
            {
                "course_code": "DS-201",
                "course_name": "Linear Algebra & Optimization",
                "area": "Mathematical Foundations",
                "description": "Matrix decompositions, vector spaces, eigenvalues, and convex optimization for machine learning.",
                "topics": [
                    {
                        "topic_id": "DS201-T1",
                        "title": "Matrix Decompositions (SVD & PCA)",
                        "competencies": [
                            "Compute singular value decomposition (SVD) for dimensionality reduction",
                            "Interpret geometric projection of eigenvectors and variance capture in PCA"
                        ],
                        "bloom_level": "Apply",
                        "prerequisites": ["Vector Spaces", "Orthogonality"],
                        "related_topics": ["DS-202: Supervised Learning"]
                    }
                ]
            }
        ]
    }
}

class SyllabusToolInput(BaseModel):
    """Input parameters for querying academic syllabi."""
    program_name: str = Field(description="Name of the academic program, e.g., 'Computer Science' or 'Data Science'")
    topic: Optional[str] = Field(default=None, description="Optional specific topic title or keyword to filter")

class SyllabusTool(BaseTool):
    name: str = "Syllabus Fetcher Tool"
    description: str = (
        "Queries and retrieves academic syllabi, course structures, learning competencies, "
        "prerequisites, and inter-course relationships from the academic registry or REST API."
    )
    args_schema: Type[BaseModel] = SyllabusToolInput

    def _run(self, program_name: str, topic: Optional[str] = None) -> str:
        """Fetch syllabus data via REST API or fallback to mock curriculum registry."""
        norm_program = program_name.strip().lower()

        # If live API is configured and mock is disabled, attempt HTTP request
        if not settings.MOCK_SYLLABUS and settings.SYLLABUS_API_BASE_URL:
            try:
                headers = {"Authorization": f"Bearer {settings.SYLLABUS_API_TOKEN}"}
                params = {"program": program_name}
                if topic:
                    params["topic"] = topic
                
                response = requests.get(
                    f"{settings.SYLLABUS_API_BASE_URL.rstrip('/')}/syllabi",
                    headers=headers,
                    params=params,
                    timeout=10
                )
                if response.status_code == 200:
                    return json.dumps(response.json(), indent=2)
                else:
                    logger.warning(
                        f"API returned status {response.status_code}. Falling back to internal syllabus registry."
                    )
            except Exception as e:
                logger.warning(f"Error querying live syllabus API: {e}. Falling back to internal registry.")

        # Fallback / Mock Mode: Query internal curriculum repository
        program_data = MOCK_CURRICULUM_DATABASE.get(norm_program)
        if not program_data:
            # Fuzzy match or fallback to first available
            for key in MOCK_CURRICULUM_DATABASE:
                if key in norm_program or norm_program in key:
                    program_data = MOCK_CURRICULUM_DATABASE[key]
                    break
        
        if not program_data:
            available = list(MOCK_CURRICULUM_DATABASE.keys())
            return json.dumps({
                "error": f"Program '{program_name}' not found.",
                "available_programs": available
            })

        # If a specific topic is requested, provide both the topic details and cross-course links
        if topic:
            topic_lower = topic.lower()
            matched_topics = []
            for course in program_data["courses"]:
                for t in course["topics"]:
                    if topic_lower in t["title"].lower() or topic_lower in t["topic_id"].lower():
                        matched_topics.append({
                            "course_code": course["course_code"],
                            "course_name": course["course_name"],
                            "area": course.get("area", ""),
                            "topic_details": t
                        })
            
            return json.dumps({
                "program_name": program_data["program_name"],
                "target_topic": topic,
                "matches": matched_topics if matched_topics else "No exact topic match, inspect full program courses.",
                "program_course_index": [
                    {"code": c["course_code"], "title": c["course_name"]} for c in program_data["courses"]
                ]
            }, indent=2)

        # Return the entire program syllabus overview
        return json.dumps(program_data, indent=2)
