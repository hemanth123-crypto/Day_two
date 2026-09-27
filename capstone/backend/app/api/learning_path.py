from __future__ import annotations
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.schemas.recommendation import LearningPathStep
from backend.app.services.learning_path_service import build_learning_path

router = APIRouter(prefix='/learning-path', tags=['learning path'])


class LearningPathRequest(BaseModel):
    current_skills: list[str] = Field(default_factory=list, description="Skills the student already knows")
    target_career: str = Field(default='Data Scientist', description="Target career role")
    target_skills: list[str] = Field(default_factory=list, description="Specific skills the student wants to learn")
    missing_skills: list[str] = Field(default_factory=list, description="Skills identified as missing")


class LearningPathResponse(BaseModel):
    target_career: str
    total_steps: int
    path: list[LearningPathStep]


@router.post('', response_model=LearningPathResponse)
def build_learning_path_endpoint(request: LearningPathRequest):
    """
    Generate an ordered, step-by-step personalized learning path:
    - Orders milestones topologically based on prerequisite logic
    - Progresses systematically from Foundations to Core, Applied, and Specialization
    - Maps each step to a real course from the Coursera dataset
    """
    try:
        path = build_learning_path(request.model_dump())
        return LearningPathResponse(
            target_career=request.target_career,
            total_steps=len(path),
            path=path,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
