from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class File(BaseModel):
    id_file : Optional[int] = None
    user_token : int
    month : int
    year : int
    upload_date : str
    descr_file : str


class FileTable(Base):
    __tablename__ = "file"
    
    id_file = Column(Integer, primary_key=True, index=True)
    user_token = Column(Integer, ForeignKey("user.token"))
    month = Column(Integer)
    year = Column(Integer)
    upload_date = Column(String)
    descr_file = Column(String, unique=True)