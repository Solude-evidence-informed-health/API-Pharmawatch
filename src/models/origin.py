from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Origin(BaseModel):
    id_origin : Optional[int] = None
    descr_origin : str


class OriginTable(Base):
    __tablename__ = "origin"

    id_origin = Column(Integer, primary_key=True, index=True)
    descr_origin = Column(String, unique=True)