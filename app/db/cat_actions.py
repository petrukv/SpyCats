from dotenv import load_dotenv
import os
import requests

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.cat_schema import SpyCatCreate
from app.db.models import SpyCat


load_dotenv()
CAT_API_URL = os.getenv("CAT_API_URL") 

def validate_breed(breed: str) -> bool:
    response = requests.get(CAT_API_URL)
    if response.status_code != 200:
        raise HTTPException(status_code=503, detail="Could not fetch breed data")
    breeds = response.json()
    return any(breed_data["name"].lower() == breed.lower() for breed_data in breeds)

def create_spy_cat(db: Session, cat_data: SpyCatCreate):
    if not validate_breed(cat_data.breed):
        raise HTTPException(status_code=400, detail="Invalid cat breed")
    
    new_cat = SpyCat(
        name=cat_data.name,
        years_of_experience=cat_data.years_of_experience,
        breed=cat_data.breed,
        salary=cat_data.salary
    )
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

def remove_spy_cat(db: Session, cat_id: int):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    
    db.delete(cat)
    db.commit()
    return {"detail": "Spy cat deleted successfully"}

def update_spy_cat_salary(db: Session, cat_id: int, new_salary: float):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    
    cat.salary = new_salary
    db.commit()
    db.refresh(cat)
    return cat

def list_spy_cats(db: Session):
    return db.query(SpyCat).all()

def get_spy_cat(db: Session, cat_id: int):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    return cat