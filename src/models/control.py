from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from src.models.medicine import MedicineTable
from src.models.origin import OriginTable
from src.models.destination import DestinationTable
from src.models.file import FileTable


Base = declarative_base()


class Control(BaseModel):
    id_control : Optional[int] = None
    id_medicine : int
    unit_value : float
    unit_quantity : float
    total_value : float
    month : int
    year : int
    id_origin : int
    id_destination : int
    id_upload_file : int


class ControlTable(Base):
    __tablename__ = "control"

    id_control = Column(Integer, primary_key=True, index=True)
    id_medicine = Column(Integer, ForeignKey("medicine.id_medicine"))
    unit_value = Column(Float)
    unit_quantity = Column(Float)
    total_value = Column(Float)
    month = Column(Integer)
    year = Column(Integer)
    id_origin = Column(Integer, ForeignKey("origin.id_origin"))
    id_destination = Column(Integer, ForeignKey("destination.id_destination"))
    id_upload_file = Column(Integer, ForeignKey("file.id_file"))

    medicine = relationship("MedicineTable", back_populates="controls")
    origin = relationship("OriginTable", back_populates="controls")
    destination = relationship("DestinationTable", back_populates="controls")
    upload_file = relationship("FileTable", back_populates="controls")