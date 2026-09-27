from __future__ import annotations
from fastapi import APIRouter, HTTPException

from backend.app.schemas.evaluation import EvaluationRequest, EvaluationResponse
from backend.app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from backend.app.services.evaluation_service import evaluate_recommendations_workflow
from backend.app.services.recommendation_service import build_recommendations

router = APIRouter(prefix='/recommendations', tags=['recommendations'])


@router.post('', response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):
    """
    Intelligent recommendation endpoint:
    - Natural language query understanding (extracts existing skills, target career, domain, difficulty)
    - FAISS semantic retrieval + hybrid reranking
    - Skill-gap analysis comparing current skills against career requirements
    - Configurable rule-based prerequisite mapping
    - Personalized sequential learning path mapped to actual Coursera courses
    """
    try:
        result = build_recommendations(
            query=request.query,
            top_k=request.top_k,
            current_skills=request.current_skills,
            target_career=request.target_career,
            preferred_difficulty=request.preferred_difficulty,
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Recommendation processing error: {str(exc)}")


@router.post('/evaluate', response_model=EvaluationResponse)
def evaluate_recommendations(request: EvaluationRequest):
    """
    Evaluation & Explainability Endpoint:
    Returns an exhaustive breakdown explaining WHY each course was recommended to this student:
    - Mathematical score decomposition across 5 hybrid factors
    - Prerequisite readiness analysis (satisfied vs missing prerequisites)
    - Direct skill gap closure identification
    - Grounded pedagogical justification narrative
    - Strengths and considerations report
    """
    try:
        return evaluate_recommendations_workflow(
            query=request.query,
            top_k=request.top_k,
            current_skills=request.current_skills,
            target_career=request.target_career,
            preferred_difficulty=request.preferred_difficulty,
            course_id=request.course_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Evaluation processing error: {str(exc)}")


@router.get('/benchmark')
def get_benchmark():
    """
    Returns quantitative evaluation benchmarks across 10 representative student queries:
    - Precision@3, Precision@5
    - NDCG@3, NDCG@5
    - MRR (Mean Reciprocal Rank)
    - Skill-gap accuracy & Topological DAG validity
    - Detailed per-query evaluations
    """
    from backend.app.services.evaluation_service import get_system_benchmark_report
    try:
        return get_system_benchmark_report()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error loading benchmark report: {str(exc)}")

