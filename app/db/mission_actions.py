from sqlalchemy.orm import Session, joinedload

from app.db.models import Mission, SpyCat, Target
from app.schemas.missions import MissionCreate

def create_mission(db: Session, mission_data: MissionCreate):
    mission = Mission(
        cat_id=mission_data.cat_id,
        complete=mission_data.complete
    )
    db.add(mission)
    db.commit()
    db.refresh(mission)

    for target in mission_data.targets:
        target_db = Target(
            name=target.name,
            country=target.country,
            notes=target.notes,
            complete=target.complete,
            mission_id=mission.id 
        )
        db.add(target_db)

    db.commit()
    return mission

def delete_mission(db: Session, mission_id: int):
    mission = db.query(Mission).filter(Mission.id == mission_id).options(joinedload(Mission.targets)).first()
    
    if not mission:
        return {"detail": "Mission not found"}

    if mission.cat_id:
        raise Exception("Cannot delete a mission assigned to a cat.")

    db.query(Target).filter(Target.mission_id == mission.id).delete()
    
    db.delete(mission)
    db.commit()

    return mission

def update_target(db: Session, target_id: int, completed: bool, notes: str):
    target = db.query(Target).filter(Target.id == target_id).first()

    if not target:
        return None 

    if target.complete or target.mission.complete:
        raise Exception("Cannot update notes for a completed target or mission.")

    target.complete = completed
    target.notes = notes
    db.commit()
    db.refresh(target)
    
    return target

def assign_cat_to_mission(db: Session, mission_id: int, cat_id: int):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()

    if not mission:
        raise Exception("Mission not found")
    
    if not cat:
        raise Exception("Cat not found")
    
    if mission.cat_id is not None:
        raise Exception("Mission is already assigned to a cat")
    
    mission.cat_id = cat_id
    db.commit()
    db.refresh(mission)

    return mission

def get_all_missions(db: Session):
    return db.query(Mission).options(joinedload(Mission.targets)).all()

def get_mission_by_id(db: Session, mission_id: int):
    return db.query(Mission).options(joinedload(Mission.targets)).filter(Mission.id == mission_id).first()