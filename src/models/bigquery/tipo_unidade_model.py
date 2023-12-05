from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TipoUnidadeBase(BaseModel):
    id : Optional[int] = None
    descr_tipo_unidade : str


class TipoUnidadeTable(Base):
    __tablename__ = "tipo_unidade"
    
    id = Column(Integer, primary_key=True)
    descr_tipo_unidade = Column(String, unique=True)

