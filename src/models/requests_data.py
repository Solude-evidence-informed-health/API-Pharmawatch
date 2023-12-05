from typing import List, Optional

from src.models.utils import PaginationBase


class FiltrosMaterialRequest(PaginationBase):
    ordenacao : Optional[List[str]] = None
    ordenacao_crescente: Optional[bool] = None
    id_material : Optional[List[int]] = None
    id_tipo : Optional[List[int]] = None
    id_origem : Optional[List[int]] = None
    id_destino : Optional[List[int]] = None
    data_inicio : Optional[str] = None
    data_fim : Optional[str] = None