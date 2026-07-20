from pydantic import BaseModel, ConfigDict

class JobBase():
    title:str
    salary:float
    company:str
    description:str

class JobCreate(JobBase):
    pass
class JobUpdate(JobBase):
    title:str | None=None
    description:str | None=None
    salary:float | None=None
    comoany:str | None=None

class JobResponse(JobBase):
    id:int

    # class Configs:
    #     form_attributes=True
    model_config=ConfigDict(form_attributes=True)


