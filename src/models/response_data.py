from pydantic import BaseModel
from typing import List, Optional

from src.models.utils import PaginationBase, AbcBase
from src.models.bigquery.tipo_model import TipoBase
from src.models.bigquery.origem_model import OrigemBase
from src.models.bigquery.destino_model import DestinoBase
from src.models.bigquery.material_model import MaterialBase


class CurvaAbcMaterialResponse(PaginationBase):
    data: Optional[List[AbcBase]] = []
    total_pages: Optional[int] = 1
    total_records: Optional[int] = 0


class FiltrosResponse(BaseModel):
    material: Optional[List[MaterialBase]] = []
    tipo: Optional[List[TipoBase]] = []
    origem:  Optional[List[OrigemBase]] = []
    destino:  Optional[List[DestinoBase]] = []