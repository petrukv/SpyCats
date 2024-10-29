from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.cat_schema import SpyCatCreate, SpyCatSalaryUpdate, SpyCatBase
from app.db import cat_actions
from app.db.postgres_connection import get_db

router = APIRouter(prefix='/cat')

@router.post("/spy_cats", response_model=SpyCatBase)
async def add_spy_cat_route(cat_data: SpyCatCreate, db: Session = Depends(get_db)):
    return cat_actions.create_spy_cat(db, cat_data)

@router.delete("/spy_cats/{cat_id}")
async def delete_spy_cat_route(cat_id: int, db: Session = Depends(get_db)):
    return cat_actions.remove_spy_cat(db, cat_id)

@router.patch("/spy_cats/{cat_id}/salary")
async def update_spy_cat_salary_route(cat_id: int, salary_data: SpyCatSalaryUpdate, db: Session = Depends(get_db)):
    return cat_actions.update_spy_cat_salary(db, cat_id, salary_data.salary)

@router.get("/spy_cats", response_model=list[SpyCatBase])
async def list_spy_cats_route(db: Session = Depends(get_db)):
    return cat_actions.list_spy_cats(db)

@router.get("/spy_cats/{cat_id}")
async def get_spy_cat_route(cat_id: int, db: Session = Depends(get_db)):
    return cat_actions.get_spy_cat(db, cat_id)