from pydantic import BaseModel
from typing import List

from src.models.medicine import Medicine
from src.models.utils import PaginationBase


class ResponseMedicineList(PaginationBase):
    data : List[Medicine]
    total_pages : int
    total : int

class ResponseFilters(BaseModel):
    type : List[str]
    origin :  List[str]
    destination :  List[str]