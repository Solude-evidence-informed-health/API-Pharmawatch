from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Destination(BaseModel):
    id_destination : Optional[int] = None
    descr_destination : str


class DestinationTable(Base):
    __tablename__ = "destination"
    
    id_destination = Column(Integer, primary_key=True, index=True)
    descr_destination = Column(String, unique=True)