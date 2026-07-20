# from fastapi import FastAPI
# from app.models.job import Job
# from app.schemas.job_schema import JobCreate
# #This imports the FastAPI class from the fastapi package

# app = FastAPI()
# #This creates a FastAPI application object.

# @app.get('/')
# def home():
#     #create a job object model
#     job = Job(
#         title="Backend Developer",
#         description="Develop FastAPI Applications",
#         salary=750000,
#         company="ABC Technologies"
#     )
    
#     job_schema = JobCreate(
#         title=job.title,
#         description=job.description,
#         salary=job.salary,
#         company=job.company
#     )

#     return{
#         "Model": job.__dict__,
#         "Schema": job_schema.model_dump()
#     }
    
# @app.post("/jobs")
# def create_jobs(job: JobCreate):
#     #Convert Schema to Model
#     job_model = Job(
#         title=job.title,
#         description=job.description,
#         salary=job.salary,
#         company=job.company
#     )
    
#     return{
#         "message": "Job Created Successfully",
#         "data": job_model.__dict__
#     }
    
    
# # @app.get('/')
# # def home():
# #     return {"message": "Welcome to FastAPI"}

# # @app.post("/jobs")
# # def create_jobs():
# #     return {"message": "Job Created"}

# # @app.get("/jobs")
# # def get_jobs():
# #     return {"message": "List of jobs"}

# # @app.put("/jobs")
# # def update_job():
# #     return {"message": "Job Updated"}

# # @app.patch("/jobs")
# # def update_salary():
# #     return {"message": "Salary Updated"}

# # #/jobs  - static query
# # @app.delete("/jobs") 
# # def delete_job():
# #     return {"message": "Job Deleted"}

# # #Path Parameters - /jobs/13  - dynamic query
# # @app.get("/jobs/{job_id}")
# # def get_job_path(job_id:int):
# #     return {"job_id": job_id}

# # #Query Parameters - http://127.0.0.1:8000/jobs?location=Chennai
# # #Searching, Filteration, Sorting, Specific search
# # @app.get("/jobsquery")
# # def get_jobs_query(location:str):
# #     return {"location":location}

# # #Multiple query parameter
# # @app.get("/jobslocation")
# # def get_jobs_location(location: str, experience: int):
# #     return {
# #         "location": location,
# #         "experience": experience
# #     }
    
# # #/jobs?location=Chennai&experience=3

# '''
# @app.get("/")

# This is called a decorator.
# It tells FastAPI:
# "When someone sends a GET request to /, execute the function below."

# home() - Python function
# return - FastAPI automatically converts the Python dictionary into JSON
# '''

from fastapi import FastAPI

from app.core.database import Base, engine

# Import models so SQLAlchemy registers them
from app.models.job import Job

app = FastAPI(
    title="Hiring Application"
)

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Hiring Application Started Successfully"
    }