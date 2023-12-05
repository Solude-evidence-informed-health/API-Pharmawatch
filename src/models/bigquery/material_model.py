from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class MaterialBase(BaseModel):
    id: Optional[int] = None
    descr_material: str

    
class Material(MaterialBase):
    descr_material_base: Optional[int] = None
    descr_material_comp: Optional[int] = None
    descr_metod_administracao: Optional[str] = None
    id_tipo: int
    id_tipo_unidade: int
    id_administracao: int
    id_apresent_farmaceutica: int
    id_origem_recurso: int


class MaterialTable(Base):
    __tablename__ = "material"

    id = Column(Integer, primary_key=True)
    descr_material = Column(String, unique=True)
    descr_material_base = Column(Integer)
    descr_material_comp = Column(Integer)
    descr_metod_administracao = Column(String)
    id_tipo = Column(Integer)
    id_tipo_unidade = Column(Integer)
    id_administracao = Column(Integer)
    id_apresent_farmaceutica = Column(Integer)
    id_origem_recurso = Column(Integer)

