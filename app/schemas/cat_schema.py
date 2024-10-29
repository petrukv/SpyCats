from pydantic import BaseModel


class SpyCatBase(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float

    class Config:
        orm_mode = True

class SpyCatCreate(SpyCatBase):
    pass
    

class SpyCatSalaryUpdate(BaseModel):
    salary: float