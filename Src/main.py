from fastapi import FastAPI, APIRouter
from Src.Controllers.root.root_controller import router as root_router


app = FastAPI()
router = APIRouter()


app.include_router(root_router, tags=["root"])