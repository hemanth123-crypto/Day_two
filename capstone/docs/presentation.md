# 10-Minute Capstone Presentation & Defense Guide

**Title**: University Course Finder – Intelligent Course Discovery System  
**Format**: 8-Minute Working Solution Demonstration + 2-Minute Panel Q&A  
**Audience**: Capstone Evaluation Panel / Examination Committee  

---

## Part 1: Minute-by-Minute Presentation Script (8 Minutes)

### 00:00 – 01:00 | Problem Statement & Motivation
- **Speaker Script**:  
  *"Good morning, esteemed panel. Today, online education platforms host hundreds of thousands of courses. Yet, students encounter significant friction when trying to discover the right courses. Why? Because students search with intent, existing background, and career goals — such as 'I know Python and SQL and want to move into machine learning' — while traditional platforms rely on rigid keyword search. Keywords miss synonyms, fail to analyze skill gaps, ignore prerequisites, and return hundreds of disconnected results without pedagogical structure. Our objective was to engineer an intelligent course discovery system that understands natural-language learning goals, audits skill deficits, resolves prerequisites, and generates a personalized curriculum."*

### 01:00 – 02:00 | Proposed Solution & Key Value Proposition
- **Speaker Script**:  
  *"Our solution is a local-first microservice application powered by dense vector retrieval and graph algorithms. When a student enters a natural language goal, the system performs four core tasks:*
  1. *Deconstructs the query into existing skills, career targets, and difficulty preferences.*
  2. *Audits the student's competencies against standardized industry career profiles.*
  3. *Retrieves and reranks genuine Coursera courses using FAISS and multi-factor hybrid scoring.*
  4. *Synthesizes an ordered, prerequisite-safe learning path using topological graph sequencing.*
  *Crucially, the entire system runs locally on Windows without requiring cloud LLM dependencies or Docker."*

### 02:00 – 03:00 | System Architecture & Technical Stack
- **Speaker Script**:  
  *(Display Architecture Diagram)*  
  *"Our architecture comprises three decoupled layers:*
  - **Data & Embedding Pipeline**: *884 Coursera courses cleaned and indexed offline into a 384-dimensional FAISS Inner Product index using sentence-transformers/all-MiniLM-L6-v2.*
  - **Backend Microservice**: *FastAPI providing asynchronous REST endpoints, request timing middleware, SQLAlchemy ORM, and SQLite persistence for student feedback.*
  - **Frontend UI**: *A modern, responsive React 18 application built with TypeScript, Tailwind CSS, and Lucide icons featuring interactive skill gap meters, course cards, and timeline roadmaps."*

### 03:00 – 05:00 | Live Demonstration
- **Speaker Script**:  
  *(Open browser at `http://localhost:5173`)*  
  1. *"Let us test a complex query: **'I know Python and SQL and want to become a machine learning engineer.'**"*
  2. *(Submit search)*  
     *"Observe how the Query Understanding Engine instantly extracts 'Python' and 'SQL' as existing competencies and detects 'Machine Learning Engineer' as the target career."*
  3. *(Click on Skill Gap tab)*  
     *"The Skill Gap Engine compares the student's profile against the required competencies for a Machine Learning Engineer. It reveals a 28.6% readiness score, identifies gaps in Deep Learning, Mathematics, Scikit-learn, and TensorFlow, and suggests specific courses to close each gap."*
  4. *(Click on Recommendations tab)*  
     *"Notice the top recommendation: **'Machine Learning with Python'** by IBM with a 4.7 rating. Each course card includes an evidence-based explanation grounded in real metadata without hallucination. We can filter dynamically by difficulty or rating."*
  5. *(Click on Learning Path tab)*  
     *"Finally, look at the personalized curriculum: Step 1 starts with foundational Mathematics for Machine Learning; Step 2 establishes Machine Learning fundamentals; Step 3 advances to Scikit-learn; Step 4 covers Deep Learning; Step 5 finishes with TensorFlow in Practice. Every step satisfies topological prerequisite constraints."*
  6. *(Submit 5-star feedback)*  
     *"We submit a feedback rating, which is immediately recorded in our local SQLite database."*

### 05:00 – 06:00 | Deep Dive: Semantic Retrieval vs Keyword Search
- **Speaker Script**:  
  *"To prove our vector retrieval capability, let us enter a query without exact keyword matches: **'I want to learn predictive models.'** Traditional search fails because the course titles say 'Machine Learning' or 'Regression Analysis'. Our FAISS vector engine calculates cosine similarity in embedding space and immediately surfaces courses in Machine Learning, Business Analytics, and Quantitative Modeling."*

### 06:00 – 07:00 | Deep Dive: Skill Gap Diagnostics & Multi-Factor Reranking
- **Speaker Script**:  
  *"After vector search retrieves 30 candidate courses, our hybrid ranking engine computes:*
  $$\text{Final Score} = 0.50 \cdot S_{\text{sem}} + 0.20 \cdot S_{\text{skill}} + 0.10 \cdot S_{\text{diff}} + 0.10 \cdot S_{\text{rating}} + 0.10 \cdot S_{\text{career}}$$
  *Each score is min-max normalized to prevent rating or length scale distortion. Courses that close critical missing skills are promoted to the top of the recommendation list."*

### 07:00 – 08:00 | Deep Dive: Prerequisite DAG & Topological Sequencing
- **Speaker Script**:  
  *"Prerequisites are modeled as a Directed Acyclic Graph. We apply Kahn's algorithm with cycle detection to compute in-degrees. This guarantees students are guided through Foundations first, Core second, and Specialization third. If a student already knows Python, the system intelligently skips Python 101 and begins directly at the missing prerequisite level."*

---

## Part 2: Panel Q&A Defense — Anticipated Questions & Concise Answers (2 Minutes)

### 1. Why semantic search instead of keyword search?
> **Answer**: Keyword search requires exact vocabulary matching and is fragile against synonyms, paraphrasing, and skill aliasing. Semantic search projects query and course concepts into a shared embedding space, capturing conceptual similarity (e.g. matching "predictive models" to "machine learning").

### 2. Why embeddings?
> **Answer**: Embeddings encode semantic meaning, syntactic nuance, and technical domain context into dense numerical vectors, enabling continuous mathematical similarity calculations via dot product.

### 3. Why FAISS?
> **Answer**: Meta's FAISS library provides ultra-fast, memory-efficient nearest-neighbor search. For our 884 courses, FAISS computes exact inner-product cosine similarity in under 2 milliseconds on standard CPU hardware without external database overhead.

### 4. Why not traditional keyword search (like BM25)?
> **Answer**: BM25 relies on term frequency and inverse document frequency. It fails when users express goals in colloquial terms that differ from official university course titles. However, we maintain a TF-IDF fallback to ensure the system never crashes if vector indices are absent.

### 5. How do you identify skills from user queries?
> **Answer**: We use a centralized skill taxonomy (`skill_taxonomy.py`) with 60+ canonical skills and over 100 aliases, combined with regex-based syntactic boundary detection that distinguishes "I know X" from "I want to learn X".

### 6. How does skill-gap analysis work?
> **Answer**: We map target careers to standardized competency sets (`career_mapping.py`). The engine calculates the set difference:
> $$\text{Missing Skills} = \text{Required Skills} \setminus \text{Current Skills}$$
> and coverage percentage as the proportion of mastered competencies.

### 7. How are prerequisites determined?
> **Answer**: Prerequisites are governed by an educational knowledge graph (`prerequisite_graph.py`) curated from standard computer science and data science university curricula. They are explicitly marked in responses as rule-based educational guidance to distinguish them from raw dataset metadata.

### 8. How is the learning path generated?
> **Answer**: We extract the prerequisite subgraph for the student's missing skills, check for circular dependencies, and run Kahn's topological sort. We then query the dataset to match each milestone with the highest-rated real course matching that difficulty tier.

### 9. How do you personalize recommendations?
> **Answer**: Personalization is achieved through multi-signal weighting: prioritizing courses that cover the user's *missing* skills, match their preferred difficulty tier, reflect their target career track, and maintain verified peer ratings.

### 10. How do you prevent hallucinations?
> **Answer**: All recommended courses, descriptions, ratings, and URLs are retrieved directly from the real Coursera dataset. Explanations are deterministically assembled from factual course metadata and matched skills, rather than unconstrained generative text.

### 11. How do you evaluate recommendation quality?
> **Answer**: We built an automated benchmark suite (`evaluate_system.py`) testing 10 representative queries. It calculates Precision@K (0.900 @ K=3), Recall@K (0.555 @ K=3, 0.900 @ K=5), NDCG@K (0.937 @ K=3), 100% skill-gap accuracy, and 100% learning-path validity.

### 12. What happens if the external LLM API is unavailable?
> **Answer**: The application is 100% locally self-contained. It relies on local SentenceTransformers embeddings, local FAISS vector store, local rule-based skill taxonomies, and SQLite. No external API key or internet connection is required.

### 13. Why FastAPI?
> **Answer**: FastAPI provides asynchronous request handling, high throughput via Starlette/Uvicorn, automatic Pydantic request/response validation, and auto-generated interactive OpenAPI/Swagger documentation.

### 14. Why React?
> **Answer**: React 18 with Vite provides immediate UI re-rendering, modular component reusability, and instant state synchronization for our interactive skill gap meters, filter panels, and timeline visualizations.

### 15. Why SQLite?
> **Answer**: SQLite offers zero-configuration, serverless, self-contained ACID transactions with zero network latency. It stores student feedback and course records cleanly on Windows without requiring Docker or a dedicated database daemon.

### 16. What are the limitations of the current implementation?
> **Answer**: The system uses a public Coursera dataset of 884 courses; highly proprietary or enterprise-niche tools are mapped to parent competencies. Additionally, weekly module syllabi are not in the raw CSV, so prerequisites are inferred at the skill level rather than individual lecture level.

### 17. What is the future scope?
> **Answer**: Incorporating continuous online feedback learning (RLHF for recommendation weights), multi-platform course ingestion (edX, MIT OCW), and user account profile persistence.
