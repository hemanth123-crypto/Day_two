from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FactorDetail(BaseModel):
    name: str
    weight: float
    raw_score: float
    normalized_score: float
    points_contributed: float
    percentage_of_final: float
    explanation: str


class PrerequisiteReadiness(BaseModel):
    status: str = Field(..., description="'READY' or 'PREREQUISITES_NEEDED'")
    readiness_score: float = Field(..., ge=0.0, le=1.0)
    satisfied_prerequisites: List[str] = Field(default_factory=list)
    missing_prerequisites: List[str] = Field(default_factory=list)
    guidance: str


class CourseEvaluation(BaseModel):
    course_id: str
    course_name: str
    organization: str = 'Top Institution'
    difficulty: str = 'Intermediate'
    rating: Optional[float] = 4.5
    final_score: float
    rank: int = 1
    verdict: str
    verdict_badge: str
    prerequisite_readiness: PrerequisiteReadiness
    factors: Dict[str, FactorDetail]
    closed_skill_gaps: List[str] = Field(default_factory=list)
    reinforced_skills: List[str] = Field(default_factory=list)
    key_strengths: List[str] = Field(default_factory=list)
    considerations: List[str] = Field(default_factory=list)
    detailed_justification: str


class EvaluationRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Student's natural language goal or question")
    current_skills: Optional[List[str]] = Field(default=None, description="Current skills override")
    target_career: Optional[str] = Field(default=None, description="Target career override")
    preferred_difficulty: Optional[str] = Field(default=None, description="Preferred difficulty level")
    course_id: Optional[str] = Field(default=None, description="Specific course ID to evaluate (or top recommendations if None)")
    top_k: int = Field(default=5, ge=1, le=20)


class EvaluationResponse(BaseModel):
    query: str
    target_career: str
    student_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    career_coverage_pct: float
    evaluations: List[CourseEvaluation]
    evaluation_methodology: Dict[str, Any]
