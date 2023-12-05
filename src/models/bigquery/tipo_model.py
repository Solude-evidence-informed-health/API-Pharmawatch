from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TipoBase(BaseModel):
    id : Optional[int] = None
    descr_tipo : str


class TipoTable(Base):
    __tablename__ = "tipo"
    
    id = Column(Integer, primary_key=True)
    descr_tipo = Column(String, unique=True)

