# University Course Finder – Intelligent Course Discovery System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6.svg)](https://www.typescriptlang.org/)
[![FAISS](https://img.shields.io/badge/Vector_Search-FAISS_CPU-orange.svg)](https://github.com/facebookresearch/faiss)
[![Pytest 23/23 Passing](https://img.shields.io/badge/Pytest-23%2F23%20Passing-brightgreen.svg)](backend/tests/)
[![Offline Capable](https://img.shields.io/badge/Environment-100%25%20Offline%20%7C%20No%20Docker-success.svg)](#)

---

## 1. Overview & Problem Statement

Students commonly struggle to identify appropriate online courses tailored to their personal goals, existing competencies, desired difficulty levels, and target career trajectories. Traditional keyword search systems frequently return overwhelming lists of undifferentiated courses without understanding student intent, educational prerequisites, or specific skill gaps.

Students ask queries like:
- *"I want to learn data science from the basics. Which courses should I start with?"*
- *"I know Python and SQL. What courses should I take next to move into machine learning?"*
- *"I want to learn cloud computing but I don't know which prerequisite courses I need."*
- *"Can you suggest a learning path from beginner to advanced data analytics?"*

The **University Course Finder** solves this problem as an end-to-end intelligent recommendation engine. It parses natural-language learning goals, executes semantic vector search over 884 real Coursera courses, performs deterministic skill-gap analysis, resolves prerequisite dependencies via directed acyclic graphs (DAGs), generates topologically ordered learning paths, and applies multi-factor hybrid reranking with fully transparent, grounded explanations.

---

## 2. Key Architectural Highlights

```
+--------------------------------------------------------------------------------------------------+
|                                    UNIVERSITY COURSE FINDER                                      |
+--------------------------------------------------------------------------------------------------+
                                                 |
                       +-------------------------+-------------------------+
                       |                                                   |
                       v                                                   v
          +-------------------------+                         +-------------------------+
          |   React 18 + TS Web UI  |                         |   FastAPI REST Backend  |
          |  Tailwind CSS Explorer  |                         |      Swagger OpenAPI    |
          |   (Port 5173 / Vite)    |                         |    (Port 8000 / Uvicorn)|
          +-------------------------+                         +-------------------------+
                       |                                                   |
                       +-------------------------+-------------------------+
                                                 |
                   +-----------------------------+-----------------------------+
                   |                             |                             |
                   v                             v                             v
        +--------------------+         +--------------------+        +--------------------+
        |  Semantic Engine   |         |  Knowledge Base    |        |   Database Layer   |
        | - MiniLM-L6-v2     |         | - 60+ Tech Skills  |        | - SQLite Engine    |
        | - FAISS IndexFlatIP|         | - 6 Career Models  |        | - 884 Real Courses |
        | - TF-IDF Fallback  |         | - Prerequisite DAG |        | - Student Feedback |
        +--------------------+         +--------------------+        +--------------------+
```

1. **Natural-Language Query Understanding**:
   Segments student prompts into existing competencies, desired target careers, specific skills, and preferred difficulty using rule-based parsing with negative lookbehinds.
2. **Dense Semantic Retrieval**:
   Embeds queries with `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors) and queries a normalized FAISS `IndexFlatIP` for cosine similarity matching, with TF-IDF fallback for rare acronyms.
3. **Skill-Gap Analysis & Coverage Scoring**:
   Maps 6 career profiles (Data Scientist, ML Engineer, Cloud Engineer, Software Developer, Data Analyst, Data Engineer) against 60+ canonical skills and 100+ aliases to identify missing proficiencies.
4. **Curated Prerequisite Directed Acyclic Graph (DAG)**:
   Formalizes educational dependencies (e.g., Python & Mathematics $\to$ Machine Learning $\to$ Deep Learning $\to$ TensorFlow). Employs Kahn's algorithm for topological sorting and cycle detection.
5. **Multi-Factor Hybrid Reranking**:
   Combines semantic similarity, skill-gap closure, career alignment, difficulty compatibility, and institutional rating using min-max score normalization.
6. **Topological Learning Path Generation**:
   Produces a step-by-step sequential curriculum mapping each milestone to real, accredited Coursera courses from IBM, Google, Stanford, Johns Hopkins, and University of Michigan.
7. **SQLite Persistence & Feedback Loop**:
   Persists course metadata and real-time student usefulness ratings and comments.
8. **Native Windows Execution**:
   Runs 100% natively on Windows PowerShell without Docker or paid external LLM APIs.

---

## 3. Project Directory Structure

```
c:\Users\Administrator\Python\capstone\
|-- backend\
|   |-- app\
|   |   |-- api\                    # FastAPI REST endpoints
|   |   |   |-- courses.py          # /api/v1/courses (list, detail, search)
|   |   |   |-- recommendations.py  # /api/v1/recommendations
|   |   |   |-- skills.py           # /api/v1/skills/analyze, taxonomy, careers
|   |   |   |-- learning_path.py    # /api/v1/learning-path
|   |   |   `-- feedback.py         # /api/v1/feedback & stats
|   |   |-- knowledge_base\         # Centralized educational graph & profiles
|   |   |   |-- skill_taxonomy.py   # 60+ canonical skills, 100+ aliases
|   |   |   |-- career_mapping.py   # 6 career roles & core competencies
|   |   |   `-- prerequisite_graph.py # DAG, cycle check, Kahn's topological sort
|   |   |-- models\                 # SQLAlchemy ORM models (courses, feedback)
|   |   |-- schemas\                # Pydantic v2 validation models
|   |   |-- services\               # Domain business logic
|   |   |   |-- embedding_service.py # MiniLM-L6-v2 singleton
|   |   |   |-- search_service.py    # FAISS + TF-IDF dense/sparse retrieval
|   |   |   |-- ranking_service.py   # Min-max normalized hybrid scoring
|   |   |   |-- query_parser.py      # Natural language intent segmentation
|   |   |   |-- skill_service.py     # Skill-gap & coverage evaluation
|   |   |   |-- prerequisite_service.py # Educational dependency graphs
|   |   |   |-- learning_path_service.py # Sequential course curriculum builder
|   |   |   `-- recommendation_service.py # End-to-end orchestration & explanations
|   |   |-- utils\                  # Request logging & timing middleware
|   |   |-- config.py               # Central project constants & weights
|   |   |-- database.py             # SQLite connection & sessionmaker
|   |   `-- main.py                 # FastAPI application factory
|   |-- scripts\
|   |   |-- preprocess_data.py      # Cleans courses.csv & populates SQLite DB
|   |   |-- build_embeddings.py     # Generates 884 course vector embeddings
|   |   `-- build_index.py          # Compiles FAISS IndexFlatIP vector index
|   `-- tests\                      # 23 Pytest unit & integration test cases
|-- data\
|   |-- raw\courses.csv             # Coursera course catalog (884 rows)
|   `-- processed\courses_cleaned.csv # Cleaned & normalized course dataset
|-- vector_store\
|   |-- course_embeddings.npy       # Precomputed MiniLM float32 numpy vectors
|   |-- course_ids.json             # Vector-index-to-course-ID mapping
|   `-- course_index.faiss          # Serialized FAISS CPU index
|-- frontend\
|   |-- src\
|   |   |-- components\             # Navbar, SearchForm, CourseCard, Filters,
|   |   |                           # SkillGapPanel, LearningPathTimeline, etc.
|   |   |-- pages\                  # HomePage, ResultsPage, CourseDetailPage,
|   |   |                           # SkillGapPage, LearningPathPage, Explorer
|   |   |-- services\api.ts         # Axios API client
|   |   |-- types\index.ts          # TypeScript interfaces
|   |   `-- App.tsx / main.tsx      # React router & root component
|   |-- package.json & vite.config.ts
|-- docs\
|   |-- architecture.md             # System architecture & data flow diagrams
|   |-- architecture_diagram.png    # 300 DPI high-resolution architecture visual
|   |-- design.md                   # Algorithm design & trade-offs
|   |-- api.md                      # Comprehensive REST API reference & curls
|   `-- presentation.md             # 10-minute presentation script & Q&A defense
|-- evaluation\
|   |-- test_queries.json           # 10 benchmark student queries
|   |-- evaluate_system.py          # Benchmark runner (P@K, NDCG@K, MRR, DAG)
|   `-- evaluation_report.md        # Comprehensive quantitative results report
|-- requirements.txt                # Python backend dependencies
`-- README.md                       # Master capstone documentation
```

---

## 4. Quick Start Guide (Windows Native Execution)

> [!NOTE]
> **Zero Docker Guarantee**: All services run natively on Windows via Python 3.10+ and Node.js.

### Step 1: Environment Setup
Open PowerShell in the project root:
```powershell
cd c:\Users\Administrator\Python\capstone

# Create and activate Python virtual environment (or use system Python 3.10+)
python -m venv .venv
.venv\Scripts\activate

# Install backend dependencies
python -m pip install -r requirements.txt
```

### Step 2: Data Preprocessing & Database Initialization
Clean the raw Coursera dataset (`data/raw/courses.csv`), normalize difficulty and ratings, clean skill tokens, and populate the SQLite database:
```powershell
python backend/scripts/preprocess_data.py
```
*Output: Processed 884 courses into `data/processed/courses_cleaned.csv` and initialized `backend/course_finder.db`.*

### Step 3: Vector Embeddings & FAISS Index Generation
Generate 384-dimensional dense semantic vectors using `all-MiniLM-L6-v2` and build the FAISS `IndexFlatIP` index:
```powershell
python backend/scripts/build_embeddings.py
python backend/scripts/build_index.py
```
*Output: Saved `course_embeddings.npy` (884 x 384) and `course_index.faiss` in `vector_store/`.*

### Step 4: Run the Backend REST API
Launch the FastAPI development server with automatic reload:
```powershell
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **Live API Endpoint**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **Redoc Documentation**: `http://127.0.0.1:8000/redoc`

### Step 5: Run the React 18 Frontend
In a second PowerShell terminal:
```powershell
cd c:\Users\Administrator\Python\capstone\frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
- **Web Application**: `http://localhost:5173`

---

## 5. REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Service health status and application metadata |
| `GET` | `/api/v1/courses` | Paginated catalog browsing with search and filters |
| `GET` | `/api/v1/courses/{course_id}` | Detailed course view by unique ID |
| `POST` | `/api/v1/courses/search` | Semantic and keyword course search with filters |
| `POST` | `/api/v1/recommendations` | **Core Engine**: Natural language recommendation pipeline |
| `POST` | `/api/v1/skills/analyze` | Standalone student skill-gap analysis |
| `GET` | `/api/v1/skills/taxonomy` | Complete list of 60+ canonical technical skills |
| `GET` | `/api/v1/skills/careers` | Available target career profiles and core competencies |
| `POST` | `/api/v1/learning-path` | Topologically ordered milestone curriculum builder |
| `POST` | `/api/v1/feedback` | Record student usefulness rating and comments in SQLite |
| `GET` | `/api/v1/feedback/stats` | Aggregated feedback metrics and recent reviews |

### Core Recommendation Request Example
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/recommendations" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "I know Python and SQL and want to become a machine learning engineer.",
       "top_k": 5
     }'
```

### Recommendation Response Payload (Truncated)
```json
{
  "query": {
    "query": "I know Python and SQL and want to become a machine learning engineer.",
    "existing_skills": ["Python", "SQL"],
    "target_career": "Machine Learning Engineer",
    "desired_skills": ["Machine Learning"],
    "difficulty": "Any"
  },
  "skill_gap": {
    "target_career": "Machine Learning Engineer",
    "current_skills": ["Python", "SQL"],
    "required_skills": ["Python", "Mathematics", "Statistics", "Machine Learning", "Scikit-learn", "Deep Learning", "TensorFlow", "Model Deployment"],
    "missing_skills": ["Deep Learning", "Machine Learning", "Mathematics", "Model Deployment", "Scikit-learn", "TensorFlow"],
    "coverage_percentage": 14.3
  },
  "recommendations": [
    {
      "course_id": "course_0570",
      "course_name": "Machine Learning with Python",
      "organization": "IBM",
      "difficulty": "Intermediate",
      "rating": 4.7,
      "final_score": 0.8258,
      "matched_skills": ["Machine Learning", "Python"],
      "explanation": "Recommended because it directly targets skills you need (Machine Learning, Python) for Machine Learning Engineer and helps close your identified skill gap in Machine Learning and offers Intermediate-level instruction provided by IBM (with a 4.7 rating)."
    }
  ],
  "learning_path": [
    {
      "order": 1,
      "course": "Mathematics for Machine Learning",
      "difficulty": "Beginner",
      "prerequisites": [],
      "reason": "[Foundations] Foundational course in Mathematics to anchor your progression toward becoming a Machine Learning Engineer."
    },
    {
      "order": 2,
      "course": "Machine Learning with Python",
      "difficulty": "Intermediate",
      "prerequisites": ["Python", "Statistics", "Mathematics", "NumPy", "Pandas"],
      "reason": "[Core Competency] Build upon your competency in Python, Mathematics by mastering Machine Learning to bridge your Machine Learning Engineer skill gap."
    }
  ]
}
```

---

## 6. Multi-Factor Hybrid Ranking Formula

Candidate courses retrieved from semantic search are reranked using a normalized weighted combination of multi-dimensional educational signals:

$$\text{FinalScore}(c) = w_{\text{sem}} \cdot S_{\text{norm}}(c) + w_{\text{skill}} \cdot K_{\text{norm}}(c) + w_{\text{career}} \cdot C_{\text{norm}}(c) + w_{\text{diff}} \cdot D_{\text{norm}}(c) + w_{\text{rating}} \cdot R_{\text{norm}}(c)$$

Where weights are calibrated to prioritize educational goal alignment:
- $w_{\text{sem}} = 0.40$ (Semantic Vector Similarity via FAISS)
- $w_{\text{skill}} = 0.25$ (Skill-Gap Closure: overlap with student's missing skills)
- $w_{\text{career}} = 0.15$ (Career Profile Alignment)
- $w_{\text{diff}} = 0.10$ (Difficulty Level Fit)
- $w_{\text{rating}} = 0.10$ (Normalized Course Rating / Provider Quality)

**Min-Max Score Normalization**:
Raw sub-scores are normalized across the candidate retrieval set using min-max scaling to prevent dominant features from biasing results:

$$\text{Score}_{\text{norm}}(x) = \frac{x - x_{\min}}{x_{\max} - x_{\min} + \epsilon}$$

---

## 7. Sample Queries & Verified Outputs

### Query 1: Machine Learning Engineer Transition
- **Input**: *"I know Python and SQL and want to become a machine learning engineer."*
- **Intent**: Existing: `Python`, `SQL` | Target: `Machine Learning Engineer`
- **Missing Skills**: `Machine Learning`, `Deep Learning`, `Mathematics`, `Scikit-learn`, `TensorFlow`, `Model Deployment`
- **Top Course**: *Machine Learning with Python* (IBM, Rating 4.7, Score 0.8258)
- **Learning Path**:
  1. *Mathematics for Machine Learning* (Foundations)
  2. *Machine Learning with Python* (Core Competency)
  3. *Scikit-learn Fundamentals & Practical Applications* (Applied Practice)
  4. *Deep Learning* (Intermediate)
  5. *TensorFlow in Practice* (Specialization)

### Query 2: Beginner Data Science
- **Input**: *"I want to learn data science from the basics. Which courses should I start with?"*
- **Intent**: Existing: None | Difficulty: `Beginner` | Target: `Data Scientist`
- **Top Course**: *Python for Data Science and AI* (IBM, Rating 4.6, Score 0.8429)

### Query 3: Cloud Computing Prerequisite Exploration
- **Input**: *"I want to learn cloud computing but I don't know which prerequisite courses I need."*
- **Intent**: Target: `Cloud Engineer` | Domain: `Cloud Computing`
- **Identified Prerequisites**: Computer Networks $\to$ Operating Systems $\to$ Linux $\to$ Cloud Computing Basics
- **Top Course**: *Cloud Computing Basics (Cloud 101)* (Learn Quest, Rating 4.5, Score 0.8030)

---

## 8. Evaluation & Benchmarking Results

The system was evaluated against 10 comprehensive, realistic student queries using standard Information Retrieval metrics (`evaluation/evaluate_system.py`):

| Metric | Score (K=3) | Score (K=5) | Interpretation |
| :--- | :--- | :--- | :--- |
| **Precision@K** | **0.900** | **0.880** | 88-90% of recommended courses directly align with target competencies |
| **Recall@K** | **0.555** | **0.900** | Comprehensive coverage of relevant target courses in top 5 recommendations |
| **NDCG@K** | **0.937** | **0.966** | Highly relevant courses are strongly ranked at top positions |
| **Mean Reciprocal Rank (MRR)** | **1.000** | **1.000** | The first relevant course appears in Rank 1 for 100% of queries |

### Subsystem Verification

| Subsystem Check | Success Rate | Details |
| :--- | :--- | :--- |
| **Skill-Gap Analysis Accuracy** | **100.0%** | Successfully isolated existing vs missing skills across all test profiles |
| **Prerequisite Cycle Safety** | **100.0%** | Zero cycles detected in prerequisite graph (DAG verified via Kahn's algorithm) |
| **Learning Path Validity** | **100.0%** | 100% of generated paths strictly adhered to topological dependencies |
| **Database Feedback Persistence** | **100.0%** | Average student rating 5.0/5 with 100% usefulness across captured reviews |

---

## 9. Testing & Quality Assurance

The codebase includes an extensive Pytest test suite covering preprocessing, data normalization, vector search, DAG cycle detection, topological sorting, hybrid reranking, query parsing, and API endpoints:

```powershell
# Run the entire test suite
python -m pytest -v

# Run the end-to-end live verification script
python backend/tests/test_live_e2e.py
```

**Results**:
- **23 / 23 unit and integration tests passing** in 15 seconds.
- 0 linting or runtime errors.

---

## 10. Design Decisions & Trade-offs

1. **Sentence Transformers + FAISS vs. Pure BM25 / TF-IDF**:
   - *Decision*: Adopted `all-MiniLM-L6-v2` dense embeddings with normalized inner product (cosine similarity) index.
   - *Rationale*: Students phrase goals colloquially (e.g., "build smart algorithms" rather than "machine learning"). Dense embeddings capture conceptual affinity where keyword search fails.
2. **Explicit Rule-Based DAG vs. Unconstrained LLM Hallucinations**:
   - *Decision*: Embedded a curated directed acyclic graph for core educational prerequisites.
   - *Rationale*: Academic dependencies are strictly sequential (e.g., calculus before machine learning). Rule-based graphs guarantee zero cycle deadlocks and 100% curriculum validity.
3. **Deterministic Explanations vs. Generative Text**:
   - *Decision*: Template-based grounded explanation generation using real course metadata (partner university, rating, difficulty, and matched skills).
   - *Rationale*: Eliminates hallucinated degrees, fabricated credentials, and ensures transparency.
4. **Zero-Docker Native Windows Architecture**:
   - *Decision*: Deployed directly via Python 3.10+ and Vite/Node.js.
   - *Rationale*: Fast developer onboarding, minimal memory overhead, zero Hyper-V/WSL2 dependency issues.

---

## 11. Capstone Defense & Presentation

Comprehensive defense materials are available in the `docs/` directory:
- [System Architecture Specification](docs/architecture.md)
- [Architecture Flow Diagram](docs/architecture_diagram.png)
- [Technical Design & Algorithm Rationale](docs/design.md)
- [REST API Reference & Curl Examples](docs/api.md)
- [Capstone Presentation Script & 17 Defense Q&A Answers](docs/presentation.md)
- [System Evaluation Report](evaluation/evaluation_report.md)

---

## 12. License & Academic Integrity Notice

This project was built for academic demonstration and capstone evaluation using the publicly available Coursera course catalog. All course titles, descriptions, and partner names belong to their respective institutions.
