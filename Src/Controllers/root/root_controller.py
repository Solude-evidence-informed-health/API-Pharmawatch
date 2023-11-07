from fastapi import APIRouter

router = APIRouter()

@router.get(
    "/",
    tags=["root"],
    summary="Root endpoint",
    description="Root endpoint",
    response_description="Root endpoint",
    response_model=dict)
async def root():
    return {"message": "Pharmawatch API"}