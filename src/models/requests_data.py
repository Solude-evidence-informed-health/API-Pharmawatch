from typing import List, Optional

from src.models.utils import PaginationBase


class FiltrosMaterialRequest(PaginationBase):
    ordenacao : List[Optional[str]] = None
    ordenacao_crescente: Optional[bool] = None
    id_material : List[Optional[int]] = None
    id_tipo : List[Optional[int]] = None
    id_origem : List[Optional[int]] = None
    id_destino : List[Optional[int]] = None
    data_inicio : Optional[str] = None
    data_fim : Optional[str] = None