from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class OriginBase(BaseModel):
    id : Optional[int] = None
    descr_origin : str


class OriginTable(Base):
    __tablename__ = "origin"

    id = Column(Integer, primary_key=True)
    descr_origin = Column(String, unique=True)

