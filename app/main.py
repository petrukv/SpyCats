from fastapi import FastAPI
from app.db import models
from app.db.postgres_connection import engine
from app.routes import cat_route, mission_route


app = FastAPI()
app.include_router(cat_route.router)
app.include_router(mission_route.router)

models.Base.metadata.create_all(engine)

