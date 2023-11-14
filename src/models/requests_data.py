from typing import List, Optional

from src.models.utils import PaginationBase


class MedicineFilters(PaginationBase):
    sort : List[Optional[str]] = None
    ascending: Optional[bool] = None
    id_medicine : List[Optional[int]] = None
    id_type : List[Optional[int]] = None
    id_origin : List[Optional[int]] = None
    id_destination : List[Optional[int]] = None
    start_date : Optional[str] = None
    end_date : Optional[str] = None