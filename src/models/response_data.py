from pydantic import BaseModel
from models.medicine import Medicine
from models.utils import PaginationBase
from typing import List

class ResponseMedicineList(PaginationBase):
    data : List[Medicine]
    total_pages : int
    total : int

class ResponseFilters(BaseModel):
    type : List[str]
    origin :  List[str]
    destination :  List[str]