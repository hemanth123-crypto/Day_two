from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class SkillAnalysisRequest(BaseModel):
    current_skills: list[str] = Field(default_factory=list, description="List of student's current skills")
    target_career: Optional[str] = Field(default=None, description="Desired target career role")
    target_skills: Optional[list[str]] = Field(default=None, description="Explicit target skills to acquire")


class SkillGapResponse(BaseModel):
    current_skills: list[str]
    required_skills: list[str]
    existing_skills: list[str]
    missing_skills: list[str]
    coverage_percentage: float
    target_career: Optional[str] = None
