from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class MedicineBase(BaseModel):
    id : Optional[int] = None
    descr_medicine : str
class Medicine(MedicineBase):
    id_type : str


class MedicineTable(Base):
    __tablename__ = "medicine"

    id = Column(Integer, primary_key=True)
    descr_medicine = Column(String, unique=True)
    id_type = Column(Integer)
