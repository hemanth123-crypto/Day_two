# University Course Finder — Complete API Documentation

Interactive Swagger documentation is available at runtime at:
```text
http://127.0.0.1:8000/docs
```
OpenAPI specification JSON is available at:
```text
http://127.0.0.1:8000/openapi.json
```

---

## 1. System Health & Metadata

### `GET /api/v1/health`
Checks whether the microservice is running and ready.

#### Response `200 OK`
```json
{
  "status": "ok",
  "app": "University Course Finder"
}
```

---

## 2. Course Discovery & Search

### `GET /api/v1/courses`
Retrieves paginated course metadata with optional filters.

#### Query Parameters
- `page` (int, default: 1): Page index (1-based)
- `page_size` (int, default: 20, max: 100): Courses per page
- `difficulty` (string, optional): Filter by `Beginner`, `Intermediate`, or `Advanced`
- `search` (string, optional): Substring search across course title, description, or skills
- `organization` (string, optional): Filter by institution (e.g. `Stanford`, `Google`, `DeepLearning.AI`)

#### Sample Request
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/courses?page=1&page_size=3&difficulty=Beginner"
```

#### Response `200 OK`
```json
{
  "count": 3,
  "total": 312,
  "page": 1,
  "page_size": 3,
  "courses": [
    {
      "course_id": "course_0000",
      "course_name": "(ISC)2 Systems Security Certified Practitioner (SSCP)",
      "description": "(ISC)2 Systems Security Certified Practitioner covers cloud-native systems...",
      "skills": "Security Fundamentals; Risk Management",
      "difficulty": "Beginner",
      "rating": 4.7,
      "organization": "(ISC)2",
      "url": "https://www.coursera.org/..."
    }
  ]
}
```

---

### `GET /api/v1/courses/{course_id}`
Retrieves detailed metadata for a single course.

#### Path Parameters
- `course_id` (string): Stable course identifier (e.g. `course_0002`)

#### Response `200 OK`
```json
{
  "course_id": "course_0002",
  "course_name": "A Crash Course in Data Science",
  "description": "Introduces learners to data analysis, statistical reasoning, and practical decision-making.",
  "skills": "Data Analysis; Statistics; Python",
  "difficulty": "Intermediate",
  "rating": 4.5,
  "organization": "Johns Hopkins University",
  "url": "https://www.coursera.org/..."
}
```

#### Error Response `404 Not Found`
```json
{
  "detail": "Course with ID 'course_99999' not found."
}
```

---

### `POST /api/v1/courses/search`
Performs semantic vector search using the FAISS index with optional filters.

#### Request Body
```json
{
  "query": "I want to learn predictive models",
  "top_k": 3,
  "difficulty": "Intermediate",
  "min_rating": 4.5
}
```

#### Response `200 OK`
```json
{
  "query": "I want to learn predictive models",
  "count": 3,
  "courses": [
    {
      "course_id": "course_0566",
      "course_name": "Machine Learning for Business Professionals",
      "difficulty": "Intermediate",
      "rating": 4.6,
      "organization": "Google Cloud",
      "semantic_score": 0.724,
      "retrieval_method": "faiss_dense"
    }
  ]
}
```

---

## 3. End-to-End Recommendations

### `POST /api/v1/recommendations`
Full recommendation pipeline: natural language understanding, skill-gap analysis, FAISS semantic search, hybrid reranking, and learning path synthesis.

#### Request Body
```json
{
  "query": "I know Python and SQL and want to become a machine learning engineer.",
  "top_k": 5
}
```

#### Response `200 OK`
```json
{
  "query": {
    "query": "I know Python and SQL and want to become a machine learning engineer.",
    "existing_skills": ["Python", "SQL"],
    "target_career": "Machine Learning Engineer",
    "desired_skills": ["Machine Learning"],
    "difficulty": "Adaptive"
  },
  "skill_gap": {
    "current_skills": ["Python", "SQL"],
    "required_skills": ["Deep Learning", "Machine Learning", "Mathematics", "Model Deployment", "Python", "Scikit-learn", "TensorFlow"],
    "existing_skills": ["Python"],
    "missing_skills": ["Deep Learning", "Machine Learning", "Mathematics", "Model Deployment", "Scikit-learn", "TensorFlow"],
    "coverage_percentage": 14.3
  },
  "recommendations": [
    {
      "course_id": "course_0567",
      "course_name": "Machine Learning with Python",
      "difficulty": "Intermediate",
      "rating": 4.7,
      "organization": "IBM",
      "skills": "Python; Machine Learning",
      "semantic_score": 0.8258,
      "final_score": 0.8258,
      "explanation": "Recommended because it directly targets skills you need (Machine Learning) and helps close your identified skill gap."
    }
  ],
  "learning_path": [
    {
      "order": 1,
      "course": "Mathematics for Machine Learning: Linear Algebra",
      "difficulty": "Beginner",
      "skills": ["Mathematics"],
      "prerequisites": [],
      "reason": "[Foundations] Establish fundamental capability in Mathematics to anchor your ML path."
    },
    {
      "order": 2,
      "course": "Machine Learning for All",
      "difficulty": "Beginner",
      "skills": ["Machine Learning"],
      "prerequisites": ["Python", "Mathematics"],
      "reason": "[Core Competency] Master core machine learning algorithms."
    }
  ]
}
```

---

## 4. Skill Gap Analysis & Taxonomy

### `POST /api/v1/skills/analyze`
Compares student skills against target career competency benchmarks.

#### Request Body
```json
{
  "current_skills": ["Python", "SQL"],
  "target_career": "Data Scientist"
}
```

#### Response `200 OK`
```json
{
  "current_skills": ["Python", "SQL"],
  "required_skills": ["Data Visualization", "Machine Learning", "NumPy", "Pandas", "Python", "SQL", "Statistics"],
  "existing_skills": ["Python", "SQL"],
  "missing_skills": ["Data Visualization", "Machine Learning", "NumPy", "Pandas", "Statistics"],
  "coverage_percentage": 28.6,
  "target_career": "Data Scientist",
  "missing_skills_courses": {
    "Statistics": [
      {
        "course_id": "course_0002",
        "course_name": "A Crash Course in Data Science",
        "rating": 4.5
      }
    ]
  }
}
```

---

### `GET /api/v1/skills/taxonomy`
Returns all 60+ canonical skills recognized by the system.

#### Response `200 OK`
```json
{
  "count": 62,
  "skills": ["Algorithms", "APIs", "Artificial Intelligence", "AWS", "Azure", "Big Data", "Cloud Computing", "Deep Learning", "Docker", "Machine Learning", "Python", "SQL", "TensorFlow"]
}
```

---

### `GET /api/v1/skills/careers`
Returns supported career paths and their required skills.

---

## 5. Topological Learning Path

### `POST /api/v1/learning-path`
Generates a prerequisite-safe curriculum progression mapped to real courses.

#### Request Body
```json
{
  "current_skills": ["Python"],
  "target_career": "Machine Learning Engineer",
  "missing_skills": ["Statistics", "Machine Learning", "Deep Learning"]
}
```

#### Response `200 OK`
```json
{
  "target_career": "Machine Learning Engineer",
  "total_steps": 3,
  "path": [
    {
      "order": 1,
      "course": "Mathematics for Machine Learning: Linear Algebra",
      "difficulty": "Beginner",
      "prerequisites": [],
      "reason": "[Foundations] Address prerequisite concept Mathematics."
    }
  ]
}
```

---

## 6. Feedback System

### `POST /api/v1/feedback`
Records student feedback in SQLite.

#### Request Body
```json
{
  "course_id": "course_0567",
  "rating": 5,
  "useful": true,
  "comment": "Super helpful recommendation for my career switch."
}
```

#### Response `200 OK`
```json
{
  "message": "Feedback recorded successfully. Thank you for helping improve recommendations!",
  "feedback_id": 1,
  "course_id": "course_0567",
  "rating": 5,
  "useful": true,
  "comment": "Super helpful recommendation for my career switch.",
  "created_at": "2026-09-27T08:12:00Z"
}
```

---

### `GET /api/v1/feedback/stats`
Retrieves aggregated satisfaction metrics.

#### Response `200 OK`
```json
{
  "total_feedback": 4,
  "average_rating": 5.0,
  "usefulness_rate": 100.0,
  "rating_distribution": { "1": 0, "2": 0, "3": 0, "4": 0, "5": 4 },
  "recent_feedback": []
}
```
