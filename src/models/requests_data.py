from models.utils import PaginationBase
from typing import List, Optional


class MedicineFilters(PaginationBase):
    sort : Optional[str] = None
    type : Optional[str] = None
    origin : Optional[str] = None
    destination : Optional[str] = None
    start_date : Optional[str] = None
    end_date : Optional[str] = None