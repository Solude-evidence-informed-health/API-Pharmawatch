from pydantic import BaseModel
from typing import Optional
from typing import List
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UsuarioBase(BaseModel):
    id_usuario : Optional[int] = None
    token : str
    descr_prim_nome: str
    descr_ult_nome : str
    tags : List[str] = []
    organizacao : int
    descr_email : str
    data_criacao : str


class UsuarioTable(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True)
    token = Column(String, unique=True)
    descr_prim_nome = Column(String)
    descr_ult_nome = Column(String)
    tags = Column(String)
    organizacao = Column(Integer)
    descr_email = Column(String, unique=True)
    data_criacao = Column(String)