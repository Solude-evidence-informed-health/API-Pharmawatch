from fastapi import APIRouter, Query, Depends
from services.bigquery_retrieval_service import RetrievalService
from models.medicamento_filter_model import MedicineFilter
from typing import Optional

router = APIRouter()

@router.get("/medicamentos", response_model=dict)
async def get_medicamentos(
    page: int = Query(1, gt=0),
    per_page: int = Query(10, gt=0),
    sort: Optional[str] = None,
    filter_params: MedicineFilter = Depends(),
    retrieval_service: RetrievalService = Depends(),
):
    pass