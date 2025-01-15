from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    calories = Column(Float, nullable=False)

class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    duration = Column(Float, nullable=False)  # in minutes
    calories_burned = Column(Float, nullable=False)
