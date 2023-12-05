from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DestinoBase(BaseModel):
    id : Optional[int] = None
    descr_destino : str


class DestinoTable(Base):
    __tablename__ = "destino"
    
    id = Column(Integer, primary_key=True)
    descr_destino = Column(String, unique=True)