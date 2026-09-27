from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field

from backend.app.schemas.course import CourseResponse
from backend.app.schemas.skill import SkillGapResponse


class ParsedQueryInfo(BaseModel):
    query: str
    existing_skills: list[str] = Field(default_factory=list)
    target_career: Optional[str] = None
    desired_skills: list[str] = Field(default_factory=list)
    difficulty: Optional[str] = 'Any'
    domain: Optional[str] = 'General'


class RecommendedCourse(CourseResponse):
    semantic_score: float = 0.0
    skill_score: float = 0.0
    difficulty_score: float = 0.0
    rating_score: float = 0.0
    career_match_score: float = 0.0
    semantic_norm: float = 0.0
    skill_norm: float = 0.0
    difficulty_norm: float = 0.0
    rating_norm: float = 0.0
    career_norm: float = 0.0
    final_score: float = 0.0
    explanation: str = ''
    matched_skills: list[str] = Field(default_factory=list)


class LearningPathStep(BaseModel):
    order: int
    course: str
    course_id: Optional[str] = None
    difficulty: str = 'Beginner'
    skills: list[str] = Field(default_factory=list)
    prerequisites: list[str] = Field(default_factory=list)
    reason: str = ''
    url: Optional[str] = ''
    organization: Optional[str] = ''
    rating: Optional[float] = None


class RecommendationRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language goal or question")
    current_skills: Optional[list[str]] = Field(default=None, description="Explicit current skills override")
    target_career: Optional[str] = Field(default=None, description="Explicit target career override")
    preferred_difficulty: Optional[str] = Field(default=None, description="Difficulty filter override")
    top_k: int = Field(default=10, ge=1, le=50, description="Number of course recommendations")


class RecommendationResponse(BaseModel):
    query: ParsedQueryInfo
    skill_gap: SkillGapResponse
    recommendations: list[RecommendedCourse]
    prerequisites: dict[str, list[str]] = Field(default_factory=dict)
    learning_path: list[LearningPathStep] = Field(default_factory=list)
    llm_answer: Optional[str] = Field(default=None, description="LLM-generated RAG answer from OpenRouter")
