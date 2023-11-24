from pydantic import BaseModel
from typing import List

from src.models.utils import PaginationBase
from src.models.type import TypeBase
from src.models.origin import OriginBase
from src.models.destination import DestinationBase
from src.models.medicine import MedicineBase
from src.models.control import Control

class ResponseControlList(Control):
    descr_medicine : str

class ResponseMedicineList(PaginationBase):
    data : List[ResponseControlList]
    total_pages : int
    total : int

class ResponseFilters(BaseModel):
    medicine : List[MedicineBase]
    type : List[TypeBase]
    origin :  List[OriginBase]
    destination :  List[DestinationBase]