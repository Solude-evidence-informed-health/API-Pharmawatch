from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import APIKey, OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from dotenv import load_dotenv
from icecream import ic
import os

from src.services.bigquery_auth_service import BigQueryAuthService
from src.routes import upload_material, retrieval_material
from src.fastapi_docs import *


app = FastAPI(
    title=title,
    description=description,
    version=version,
    openapi_tags=tags_metadata,
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=redoc_url,
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
#bq_auth_service.create_all_tables(dataset="Pharmawatch")


app.include_router(retrieval_material.router, prefix="/materiais", tags=["Materials"])
app.include_router(upload_material.router, prefix="/upload", tags=["Upload"])