
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.missions import Mission, MissionCreate, Target, TargetUpdate
from app.db import mission_actions
from app.db.postgres_connection import get_db

router = APIRouter(prefix='/missions')

@router.post("/", response_model=Mission)
async def create_mission_route(mission_data: MissionCreate, db: Session = Depends(get_db)):
    return mission_actions.create_mission(db, mission_data)

@router.delete("/{mission_id}")
async def delete_mission_route(mission_id: int, db: Session = Depends(get_db)):
    try:
        mission = mission_actions.delete_mission(db, mission_id)
        if mission is None:
            raise HTTPException(status_code=404, detail="Mission not found")
        return mission
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/targets/{target_id}", response_model=Target)
async def update_target_route(target_id: int, target_data: TargetUpdate, db: Session = Depends(get_db)):
    try:
        target = mission_actions.update_target(db, target_id, target_data.complete, target_data.notes)
        if target is None:
            raise HTTPException(status_code=404, detail="Target not found")
        return target
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{mission_id}/assign_cat/{cat_id}", response_model=Mission)
async def assign_cat_route(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    try:
        mission = mission_actions.assign_cat_to_mission(db, mission_id, cat_id)
        return mission
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/")
def list_missions(db: Session = Depends(get_db)):
    return mission_actions.get_all_missions(db)

@router.get("/{mission_id}")
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    return mission_actions.get_mission_by_id(db, mission_id)