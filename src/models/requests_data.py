from typing import List, Optional
from pydantic import Field
from fastapi import Query

from src.models.utils import PaginationBase


class FiltrosMaterialRequest(PaginationBase):
    ordenacao: Optional[List[str]] = Field(Query(None), description="Description for ordenacao")
    ordenacao_crescente: Optional[bool] = Query(None, description="Description for ordenacao_crescente")
    id_material: Optional[List[int]] = Field(Query(None) , description="Description for id_material")
    id_tipo: Optional[List[int]] = Field(Query(None), description="Description for id_tipo")
    id_origem: Optional[List[int]] = Field(Query(None), description="Description for id_origem")
    id_destino: Optional[List[int]] = Field(Query(None), description="Description for id_destino")
    data_inicio: Optional[str] = Query(None, description="Description for data_inicio, must be passed along with data_fim, must be in format dd/mm/yyyy")
    data_fim: Optional[str] = Query(None, description="Description for data_fim, must be passed along with data_inicio, must be in format dd/mm/yyyy")