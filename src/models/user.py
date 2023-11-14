from pydantic import BaseModel
from typing import Optional
from typing import List
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(BaseModel):
    id_user : Optional[int] = None
    token : str
    descr_first_name : str
    descr_last_name : str
    tags : List[str] = []
    organization : int
    descr_email : str


class UserTable(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True)
    descr_first_name = Column(String)
    descr_last_name = Column(String)
    tags = Column(String)
    organization = Column(Integer, ForeignKey("organization.id_organization"))
    descr_email = Column(String, unique=True)