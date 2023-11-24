from pydantic import BaseModel
from fastapi import Query


class PaginationBase(BaseModel):
    page : int = Query(1, gt=0)
    per_page : int = Query(10, gt=0)