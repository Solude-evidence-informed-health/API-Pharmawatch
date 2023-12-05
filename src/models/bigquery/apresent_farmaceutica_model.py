from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ApresentFarmaceuticaBase(BaseModel):
    id : Optional[int] = None
    descr_apresent_farmaceutica : str


class ApresentFarmaceuticaTable(Base):
    __tablename__ = "apresent_farmaceutica"
    
    id = Column(Integer, primary_key=True)
    descr_apresent_farmaceutica = Column(String, unique=True)

