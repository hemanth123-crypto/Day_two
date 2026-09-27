from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    course_id: Optional[str] = Field(default=None, description="Course ID if feedback is for a specific course")
    rating: int = Field(..., ge=1, le=5, description="1 to 5 star rating")
    useful: bool = Field(default=True, description="Whether the recommendation was useful")
    comment: Optional[str] = Field(default="", description="Optional student feedback or suggestion")


class FeedbackResponse(BaseModel):
    message: str
    feedback_id: int
    course_id: Optional[str] = None
    rating: int
    useful: bool
    comment: str
    created_at: datetime
