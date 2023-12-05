from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class AdministracaoBase(BaseModel):
    id : Optional[int] = None
    descr_administracao : str


class AdministracaoTable(Base):
    __tablename__ = "administracao"
    
    id = Column(Integer, primary_key=True)
    descr_administracao = Column(String, unique=True)

