from pydantic import BaseModel
from typing import List, Optional

class Target(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None
    complete: bool = False

class MissionCreate(BaseModel):
    cat_id: Optional[int]
    complete: bool
    targets: List[Target]

class Mission(MissionCreate):
    id: int

    class Config:
        orm_mode = True

class TargetUpdate(BaseModel):
    complete: bool
    notes: str
