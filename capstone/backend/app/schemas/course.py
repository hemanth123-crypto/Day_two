from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    course_id: str
    course_name: str
    description: Optional[str] = None
    skills: Optional[str] = None
    difficulty: Optional[str] = 'Unknown'
    rating: Optional[float] = None
    organization: Optional[str] = None
    url: Optional[str] = None


class CourseResponse(CourseBase):
    search_text: Optional[str] = None


class CourseListResponse(BaseModel):
    count: int
    total: int
    page: int
    page_size: int
    courses: list[CourseResponse]


class CourseSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language search query")
    top_k: int = Field(default=10, ge=1, le=50, description="Maximum number of courses to return")
    difficulty: Optional[str] = Field(default=None, description="Optional difficulty filter (Beginner, Intermediate, Advanced)")
    min_rating: Optional[float] = Field(default=None, ge=0.0, le=5.0, description="Minimum course rating")
