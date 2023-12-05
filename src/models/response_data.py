from pydantic import BaseModel
from typing import List

from src.models.utils import PaginationBase, AbcBase
from src.models.bigquery.tipo_model import TipoBase
from src.models.bigquery.origem_model import OrigemBase
from src.models.bigquery.destino_model import DestinoBase
from src.models.bigquery.material_model import MaterialBase


class CurvaAbcMaterialResponse(PaginationBase):
    data: List[AbcBase]
    total_pages: int
    total: int


class FiltrosResponse(BaseModel):
    material: List[MaterialBase]
    tipo: List[TipoBase]
    origem:  List[OrigemBase]
    destino:  List[DestinoBase]