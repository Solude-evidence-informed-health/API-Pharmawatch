from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class OrigemBase(BaseModel):
    id : Optional[int] = None
    descr_origem : str


class OrigemTable(Base):
    __tablename__ = "origem"

    id = Column(Integer, primary_key=True)
    descr_origem = Column(String, unique=True)

