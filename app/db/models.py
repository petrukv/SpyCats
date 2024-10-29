from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .postgres_connection import Base

class SpyCat(Base):
    __tablename__ = 'spy_cats'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    years_of_experience = Column(Integer)
    breed = Column(String)
    salary = Column(Float)



class Mission(Base):
    __tablename__ = 'missions'

    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey('spy_cats.id'), nullable=True)
    complete = Column(Boolean, default=False)

    targets = relationship("Target", back_populates="mission")



class Target(Base):
    __tablename__ = 'targets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    complete = Column(Boolean, default=False)
    mission_id = Column(Integer, ForeignKey('missions.id'), nullable=True)

    mission = relationship("Mission", back_populates="targets")
