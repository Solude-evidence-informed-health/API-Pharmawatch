from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class OrigemRecursoBase(BaseModel):
    id : Optional[int] = None
    descr_origem_recurso : str


class OrigemRecursoTable(Base):
    __tablename__ = "origem_recurso"
    
    id = Column(Integer, primary_key=True)
    descr_origem_recurso = Column(String, unique=True)