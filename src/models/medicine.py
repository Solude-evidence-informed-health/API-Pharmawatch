from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Medicine(BaseModel):
    id_medicine : Optional[int] = None
    descr_medicine : str
    id_type : str


class MedicineTable(Base):
    __tablename__ = "medicine"

    id_medicine = Column(Integer, primary_key=True, index=True)
    descr_medicine = Column(String, unique=True)
    id_type = Column(Integer, ForeignKey("type.id_type"))