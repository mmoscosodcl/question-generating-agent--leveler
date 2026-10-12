import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from src.config import settings
from src.crew import build_assessment_crew
from src.models.schema import AssessmentOutput

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("main")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate academic assessment questions using CrewAI and Local LLMs."
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="Relational Database Normalization",
        help="Academic topic for question generation (default: 'Relational Database Normalization')"
    )
    parser.add_argument(
        "--program",
        type=str,
        default="Computer Science",
        help="Academic degree or program name (default: 'Computer Science')"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=3,
        help="Number of questions to generate (default: 3)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save the generated JSON (defaults to OUTPUT_DIR in config)"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    output_dir = Path(args.output_dir or settings.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Initializing Academic Assessment Crew...")
    logger.info(f"Program: {args.program}")
    logger.info(f"Target Topic: {args.topic}")
    logger.info(f"Question Count: {args.count}")
    logger.info(f"LLM Endpoint: {settings.LLM_BASE_URL} ({settings.LLM_MODEL_NAME})")

    crew = build_assessment_crew(
        topic=args.topic,
        program_name=args.program,
        question_count=args.count
    )

    logger.info("Starting multi-agent workflow...")
    result = crew.kickoff()

    # Extract output data
    output_data = None
    if hasattr(result, "pydantic") and result.pydantic:
        output_data = result.pydantic.model_dump()
    elif hasattr(result, "raw") and result.raw:
        try:
            output_data = json.loads(result.raw)
        except json.JSONDecodeError:
            logger.warning("Could not decode result.raw as JSON directly. Wrapping as raw output.")
            output_data = {"raw_output": result.raw}
    else:
        output_data = str(result)

    # Ensure reviewing state is explicitly False as mandated
    if isinstance(output_data, dict):
        output_data["reviewing"] = False

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_topic = "".join(c if c.isalnum() else "_" for c in args.topic.lower())
    output_filename = output_dir / f"assessment_{clean_topic}_{timestamp}.json"

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    logger.info(f"Assessment successfully generated and saved to: {output_filename}")
    print(f"\n[SUCCESS] Assessment written to: {output_filename}\n")

if __name__ == "__main__":
    main()
