# Academic Assessment Generator

> [!IMPORTANT]
> **Disclaimer: Testing Pending on Target Environment**  
> Unit tests and live container execution have not yet been run in this local development environment. Verification will be executed on the target testing host equipped with Docker and network access to the team's shared Ollama instance.

A containerized multi-agent system powered by **CrewAI** and **Local LLMs** (Ollama / OpenAI-compatible servers) that generates academic Multiple-Choice Assessments (MCQs) aligned with curriculum syllabi retrieved via REST APIs.

---

## Key Features
- **3-Tier Agent Architecture**:
  - **Orchestrator Agent**: Manages program-level scope, questions regarding course relationships, and curriculum routing across all syllabi.
  - **Curriculum Analyst Agent**: Extracts learning competencies, Bloom taxonomy levels, and prerequisites for specific topics.
  - **Assessment Specialist Agent**: Crafts rigorous MCQs with options `[A, B, C, D]`, unambiguous answers, pedagogical feedback, and forward-looking feedforward links.
- **Strict Data Contract**: Validated with Pydantic (`reviewing: false` explicitly enforced by default).
- **Flexible Syllabus Ingestion**: Custom CrewAI `BaseTool` that queries external REST APIs or runs in offline mock mode (`MOCK_SYLLABUS=true`).
- **Fully Containerized**: Ready to build and run via Docker & Docker Compose with mounted `./output` directory.

---

## Repository Setup & Linking to Remote

To push this repository to GitHub, GitLab, or your remote git server:

```bash
# 1. Initialize git repository (if not already initialized)
git init

# 2. Add files and make initial commit
git add .
git commit -m "feat: initial release of CrewAI academic assessment generator"

# 3. Link (connect) to your remote repository
git remote add origin https://github.com/your-org/academic-assessment-crew.git
git branch -M main

# 4. Push to remote
git push -u origin main
```

---

## Configuration

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Set the environment variables in `.env`:
```env
# ==========================================
# Local LLM Service (Team Ollama Instance)
# ==========================================
# If running inside Docker and reaching host: http://host.docker.internal:11434/v1
# If targeting remote team instance: http://<REMOTE_IP>:11434/v1
LLM_BASE_URL=http://host.docker.internal:11434/v1
LLM_MODEL_NAME=ollama/llama3
OPENAI_API_KEY=NA

# ==========================================
# Syllabus API Configuration
# ==========================================
SYLLABUS_API_BASE_URL=https://api.youruniversity.edu/v1
SYLLABUS_API_TOKEN=your_api_token
MOCK_SYLLABUS=true

# ==========================================
# Output Volume Directory
# ==========================================
OUTPUT_DIR=/app/output
```

---

## Running with Docker Compose (On Target Machine)

Once cloned to the target testing machine with Docker:

```bash
# Build and run assessment generation
docker compose run --rm assessment-crew --topic "Relational Database Normalization" --program "Computer Science" --count 3
```

The resulting assessment will be saved as a JSON file in `./output/`.

---

## Running Automated Tests (On Target Machine)

```bash
# Install dependencies
pip install -r requirements.txt

# Run pytest suite
pytest tests/ -v
```

---

## Example Output (`output/assessment_*.json`)

```json
{
  "topic": "Relational Database Normalization",
  "program_context": "Computer Science - Database Systems",
  "reviewing": false,
  "questions": [
    {
      "id": "Q1",
      "question_text": "Which normal form requires that all non-key attributes be fully functionally dependent on the primary key, eliminating partial dependency?",
      "options": [
        "A) First Normal Form (1NF)",
        "B) Second Normal Form (2NF)",
        "C) Third Normal Form (3NF)",
        "D) Boyce-Codd Normal Form (BCNF)"
      ],
      "correct_answer": "B) Second Normal Form (2NF)",
      "feedback": "2NF specifically eliminates partial dependencies, requiring tables to satisfy 1NF and ensure non-prime attributes depend on the complete primary key.",
      "feedforward": "Review candidate key identification before moving to 3NF and transitive dependencies in Topic 4.2."
    }
  ]
}
```

For detailed architectural specifications, consult [PLAN.md](file:///c:/Users/manue/Documents/antigravity/dazzling-meitner/PLAN.md).
