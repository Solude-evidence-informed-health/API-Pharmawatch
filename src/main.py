from fastapi import FastAPI
from src.routes import upload_medicines
from services import bigquery_auth_service
from dotenv import load_dotenv
from icecream import ic
import os
from src.routes import retrieval_medicines


load_dotenv()
ic(os.getenv("GCP_CREDENTIALS_PATH"))
ic(os.getenv("GCP_PROJECT_ID"))


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


bigquery_auth_service.set_credentials(os.getenv("GCP_CREDENTIALS_PATH"))


app.include_router(retrieval_medicines.router, prefix="/medicamentos", tags=["medicamentos"])
app.include_router(upload_medicines.router, prefix="/upload", tags=["upload"])
