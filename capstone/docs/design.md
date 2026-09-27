# University Course Finder — System Design & Trade-offs Document

## 1. Executive Summary & Design Philosophy
The **University Course Finder** is built around one fundamental principle: **students search with goals, intents, and career aspirations, while traditional course databases index keywords.**

To bridge this semantic divide, the system is designed as a modular, local-first intelligent discovery engine that combines:
1. **Dense Vector Semantic Retrieval** using Sentence Transformers and FAISS.
2. **Deterministic Intent & Entity Parsing** that robustly separates current capabilities from desired learning targets.
3. **Graph-Theoretic Curriculum Sequencing** using Directed Acyclic Graphs (DAGs) and Kahn's topological sort.
4. **Multi-Signal Hybrid Reranking** balancing semantic similarity, skill-gap closure, difficulty alignment, and peer course ratings.
5. **Local Persistence and Microservice Delivery** utilizing FastAPI, SQLite, and a modern React frontend without containerization or cloud dependency.

---

## 2. Key Architecture Decisions & Technical Trade-offs

### Trade-off 1: Semantic Vector Search (FAISS) vs Keyword Matching (BM25/Elasticsearch)
- **Decision**: Implemented dense vector retrieval using `sentence-transformers/all-MiniLM-L6-v2` with FAISS (`IndexFlatIP`).
- **Rationale**: Students frequently query with concepts like *"predictive models"*, *"cloud infrastructure"*, or *"deep learning from scratch"*. Keyword systems fail if the course description uses *"regression algorithms"*, *"AWS architecture"*, or *"neural networks"*. Vector embeddings map these related phrases into contiguous regions in 384-dimensional Euclidean space.
- **Trade-off Considered**: Heavy indexing cost vs recall quality. Pre-computing embeddings once offline and storing them in `.npy` and `.faiss` files ensures $O(N)$ dot-product retrieval runs in $<15\text{ms}$ per query during runtime.
- **Fallback Strategy**: If FAISS or the neural model is unavailable, the system automatically degrades to a TF-IDF cosine similarity search with domain n-gram boosting.

### Trade-off 2: Rule-Based Prerequisite DAG vs Generative LLM Hallucination
- **Decision**: Implemented an explicit, curated educational prerequisite DAG (`prerequisite_graph.py`) with topological cycle detection.
- **Rationale**: LLMs are prone to hallucinations, suggesting out-of-order curricula or recommending non-existent prerequisite courses. An explicit graph ensures that mathematical foundations (e.g. Linear Algebra, Statistics) strictly precede Machine Learning, and operating system / networking fundamentals strictly precede Cloud and DevOps tools.
- **Trade-off Considered**: Graph maintenance overhead vs pedagogical validity. Hand-curating 30+ core technical skill relationships provides $100\%$ cyclic safety and explainable reasoning while avoiding uncontrollable LLM latency or cost.

### Trade-off 3: Hybrid Score Normalization vs Raw Score Addition
- **Decision**: All five scoring signals (Semantic, Skill Gap, Difficulty, Rating, Career Match) are independently min-max normalized to $[0.0, 1.0]$ before applying weighted fusion:
  $$\text{Final Score} = 0.50 \cdot S_{\text{sem}} + 0.20 \cdot S_{\text{skill}} + 0.10 \cdot S_{\text{diff}} + 0.10 \cdot S_{\text{rating}} + 0.10 \cdot S_{\text{career}}$$
- **Rationale**: Raw cosine similarities typically range between $0.3$ and $0.85$, course ratings between $4.0$ and $5.0$, and discrete skill counts between $0$ and $4$. Without normalization, the signal with the highest baseline scale dominates the ranking. Normalization guarantees that each factor contributes strictly according to its configured weight.

### Trade-off 4: Local Native Execution (No Docker) vs Containerized Deployment
- **Decision**: Built strictly for native Windows execution using standard Python virtual environment and Node.js/npm.
- **Rationale**: Containerization introduces hypervisor overhead, GPU pass-through complexities for PyTorch on Windows, and Docker Desktop licensing hurdles in educational and enterprise environments. Native execution guarantees sub-second startup and direct file system access.

### Trade-off 5: SQLite vs External Database (PostgreSQL / MongoDB)
- **Decision**: Used SQLite via SQLAlchemy with `check_same_thread=False` and connection pooling.
- **Rationale**: The course catalogue is read-heavy ($884$ courses) and feedback is low-frequency asynchronous writes. SQLite eliminates external server process dependencies while providing ACID guarantees.

---

## 3. Algorithmic Specifications

### 3.1 Intent Parsing Algorithm
The natural language query parser differentiates clauses:
- Matches phrases like `I know [X]`, `familiar with [X]` -> classified into `existing_skills`.
- Matches phrases like `weak in [X]`, `struggling with [X]` -> classified into `weak_skills` and `desired_skills`.
- Matches phrases like `want to learn [X]`, `become a [X]` -> classified into `target_career` and `desired_skills`.
- Extracts difficulty keywords: *"basics"*, *"from scratch"* -> `Beginner`; *"advanced"* -> `Advanced`.

### 3.2 Topological Sort Algorithm (Kahn's Algorithm)
For a set of required skills $V$ and directed prerequisite dependencies $E = \{(u, v) \mid u \text{ is prerequisite for } v\}$:
1. Compute in-degree $\text{deg}^-(v)$ for each skill.
2. Initialize queue $Q$ with all skills having $\text{deg}^-(v) = 0$ (foundations).
3. Pop $u$ from $Q$, append to ordered sequence.
4. For each dependent $v \in \text{adj}[u]$, decrement $\text{deg}^-(v)$. If $\text{deg}^-(v) == 0$, push $v$ into $Q$.
5. If sequence length $< |V|$, detect cycle and raise `ValueError`.

### 3.3 Skill Gap Calculation
$$\text{Missing Skills} = \text{Required Skills}_{\text{career}} \setminus \text{Current Skills}_{\text{student}}$$
$$\text{Coverage \%} = \frac{|\text{Required Skills}_{\text{career}} \cap \text{Current Skills}_{\text{student}}|}{|\text{Required Skills}_{\text{career}}|} \times 100$$

---

## 4. Error Handling & Resilience
- **Empty Query**: Validated at Pydantic schema level; returns HTTP 400 with actionable feedback.
- **Out-of-Vocabulary Skills**: Passed to dense vector search, which relies on subword token embeddings to match conceptually related courses.
- **Missing Dataset or Index**: Caught during startup/request; returns HTTP 500 detailing the specific missing script output.
- **Character Encoding Guard**: All course strings are normalized via `unicodedata.normalize('NFKD')` to prevent Windows cp1252 charmap encoding errors.

---

## 5. Security & Privacy
- **Zero API Key Leakage**: No hardcoded API keys. All credentials reside in `.env`.
- **SQL Injection Prevention**: All database interactions use SQLAlchemy parameterized queries.
- **Cross-Origin Resource Sharing (CORS)**: Configured for flexible local pairing with Vite frontend.
- **Safe Logging**: `RequestLoggingMiddleware` strips sensitive authorization headers and query tokens from log traces.

---

## 6. Future Scope
1. **Interactive Feedback Reranking**: Automatically adjust recommendation weights based on aggregated student feedback ratings.
2. **Curriculum Syllabi Parsing**: Scrape weekly module breakdowns from Coursera to enable lesson-level prerequisite graph construction.
3. **Multi-Platform Course Aggregation**: Ingest courses from edX, MIT OpenCourseWare, and Udacity into the unified FAISS index.
