from sqlalchemy import Column,Float,Integer,String
from app.core.database import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer,primary_key=True,index=True)
    title=Column(String(100))
    description=Column(String(500))
    salary=Column(Float)
    company=Column(String(100))


# class job:
#     def __init__(self,title,description,salary,company):
#         self.title=title
#         self.description=description
#         self.salary=salary
#         self.company=company
