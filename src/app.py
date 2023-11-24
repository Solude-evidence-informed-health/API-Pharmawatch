from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
        {"url": "https://pharmawatch-api-iqdmxo5f2a-rj.a.run.app", "description": "Homologation server"},
        {"url": "https://localhost:80", "description": "Docker local development server"},
        {"url": "http://localhost:8000", "description": "Local development server"},
    ]

security = [
        {"Mock Security Token": ["read", "write"]},
    ]

external_docs = {
        "description": "Solude site with more information",
        "url": "https://www.solude.tech",
    }

allowed_origins = ["*"]
allowed_methods = ["*"]
allowed_headers = ["*"]


app = FastAPI(
    title="Pharmawatch API",
    description="Pharmawatch API is a Solude's REST API that allows communication between the Pharmawatch web application and the Pharmawatch database on BigQuery to retrieve and upload data in a secure way and with the proper authentication.",
    version="1.1.0",
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    servers=servers,
    security=security,
    external_docs=external_docs
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=allowed_methods,
    allow_headers=allowed_headers,
)


@app.get("/")
async def root():
    return {"message": "Welcome to Pharmawatch API"}


bq_auth_service = BigQueryAuthService()
bq_auth_service.create_all_tables(dataset="Pharmawatch")


app.include_router(retrieval_medicines.router, prefix="/medicamentos", tags=["Medicines"])
app.include_router(upload_medicines.router, prefix="/upload", tags=["Upload"])