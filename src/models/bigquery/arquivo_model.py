from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Arquivo(BaseModel):
    id : Optional[int] = None
    token_usuario : str
    mes_ref : int
    ano_ref : int
    data_upload : str
    descr_arquivo : str


class ArquivoTable(Base):
    __tablename__ = "arquivo"
    
    id = Column(Integer, primary_key=True)
    token_usuario = Column(String)
    mes_ref = Column(Integer)
    ano_ref = Column(Integer)
    data_upload = Column(String)
    descr_arquivo = Column(String, unique=True)