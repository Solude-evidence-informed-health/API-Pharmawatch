from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DestinationBase(BaseModel):
    id : Optional[int] = None
    descr_destination : str


class DestinationTable(Base):
    __tablename__ = "destination"
    
    id = Column(Integer, primary_key=True)
    descr_destination = Column(String, unique=True)