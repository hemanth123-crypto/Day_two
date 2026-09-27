from sqlalchemy import Column, Integer, String, Boolean, DateTime

from backend.app.database import Base


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(String, nullable=True)
    rating = Column(Integer, nullable=False)
    useful = Column(Boolean, default=True)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
