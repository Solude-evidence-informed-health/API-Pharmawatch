from fastapi import FastAPI
from fastapi.openapi.models import APIKey, OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from dotenv import load_dotenv
from icecream import ic
import os

from src.services.bigquery_auth_service import BigQueryAuthService
from src.routes import upload_medicines, retrieval_medicines

tags_metadata = [
        {"name": "Filters", "description": "Operations related to filters"},
        {"name": "Medicines", "description": "Operations related to medicines"},
        {"name": "Upload", "description": "Operations related to data upload of data"},
        {"name": "Retrieval", "description": "Operations related to data retrieval of data"},
        {"name": "Management", "description": "Operations related to data management as upload and removal"},
    ]

servers = [
        {"url": "https://api.example.com/v1", "description": "Homologation server"},
        {"url": "http://localhost:8000", "description": "Local development server"},
    ]

security = [
        {"Mock Security Token": ["read", "write"]},
    ]

external_docs = {
        "description": "Solude site with more information",
        "url": "https://www.solude.tech",
    }

app = FastAPI(
    title="Pharmawatch API",
    description="Pharmawatch API is a REST API that allows communication between the Pharmawatch web application and the Pharmawatch database on BigQuery to retrieve and upload data in a secure way and with the proper authentication.",
    version="1.1.0",
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    servers=servers,
    security=security,
    external_docs=external_docs
)
bq_auth_service = BigQueryAuthService()
bq_auth_service.create_all_tables(dataset="Pharmawatch")


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(retrieval_medicines.router, prefix="/medicamentos", tags=["medicamentos"])
app.include_router(upload_medicines.router, prefix="/upload", tags=["upload"])