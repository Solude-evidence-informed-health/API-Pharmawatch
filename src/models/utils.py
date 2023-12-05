from pydantic import BaseModel
from fastapi import Query


class InfoMaterial(BaseModel):
    material: str
    tipo: str
    quantidade_unidade: float
    valor_unidade: float
    valor_total: float


class AbcBase(InfoMaterial):
    percentual_valor_total: float
    curva_abc: str
    variacao_cp: float


class PaginationBase(BaseModel):
    page : int = Query(1, gt=0)
    per_page : int = Query(10, gt=0)