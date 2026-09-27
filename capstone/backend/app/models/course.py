from sqlalchemy import Column, String, Float, Text
from backend.app.database import Base


class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(String(64), primary_key=True, index=True)
    course_name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    difficulty = Column(String(64), nullable=True, index=True)
    rating = Column(Float, nullable=True)
    organization = Column(String(255), nullable=True, index=True)
    url = Column(String(512), nullable=True)
    search_text = Column(Text, nullable=True)
