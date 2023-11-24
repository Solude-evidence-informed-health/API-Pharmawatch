from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Control(BaseModel):
    id : Optional[int] = None
    id_medicine : int
    unit_value : float
    unit_quantity : float
    total_value : float
    month : int
    year : int
    id_origin : int
    id_destination : int
    id_file : int


class ControlTable(Base):
    __tablename__ = "control"

    id = Column(Integer, primary_key=True)
    id_medicine = Column(Integer)
    unit_value = Column(Float)
    unit_quantity = Column(Float)
    total_value = Column(Float)
    month = Column(Integer)
    year = Column(Integer)
    id_origin = Column(Integer)
    id_destination = Column(Integer)
    id_file = Column(Integer)
