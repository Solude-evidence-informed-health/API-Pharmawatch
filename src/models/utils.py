from pydantic import BaseModel, Field
from fastapi import Query
from typing import Optional


class InfoMaterial(BaseModel):
    material: str
    tipo: str
    quantidade_unidade: float
    valor_unidade: float
    valor_total: float


class AbcBase(InfoMaterial):
    percentual_valor_total: float
    curva_abc: str
    variacao_cp: Optional[float]


class PaginationBase(BaseModel):
    page : Optional[int] = Query(1, gt=0)
    per_page : Optional[int] = None