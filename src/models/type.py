from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Type(BaseModel):
    id_type : Optional[int] = None
    descr_type : str


class TypeTable(Base):
    __tablename__ = "type"
    
    id_type = Column(Integer, primary_key=True, index=True)
    descr_type = Column(String, unique=True)