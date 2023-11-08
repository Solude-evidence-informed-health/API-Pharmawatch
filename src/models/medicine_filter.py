from pydantic import BaseModel
from typing import List, Optional

class MedicineFilter(BaseModel):
    type: Optional[str] = None
    origin: Optional[List[str]] = None
    destination: Optional[List[str]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None