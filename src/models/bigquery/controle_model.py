from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Controle(BaseModel):
    id : Optional[int] = None
    id_material : int
    quantidade_unidade : float
    valor_unidade : float
    valor_total : float
    mes_ref : int
    ano_ref : int
    uid_mes_ano : str
    id_origem : int
    id_destino : int
    id_arquivo : int


class ControleTable(Base):
    __tablename__ = "controle"

    id = Column(Integer, primary_key=True)
    id_material = Column(Integer)
    valor_unidade = Column(Float)
    quantidade_unidade = Column(Float)
    valor_total = Column(Float)
    mes_ref = Column(Integer)
    ano_ref = Column(Integer)
    uid_mes_ano = Column(String)
    id_origem = Column(Integer)
    id_destino = Column(Integer)
    id_arquivo = Column(Integer)
