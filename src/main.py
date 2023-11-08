from fastapi import FastAPI
from routes import upload_routes, medicines_routes
from services import bigquery_auth_service
from dotenv import load_dotenv
import os


load_dotenv()


app = FastAPI()


bigquery_auth_service.set_credentials(os.getenv("GCP_CREDENTIALS_PATH"))


app.include_router(medicines_routes.router, prefix="/medicamentos", tags=["medicamentos"])
app.include_router(upload_routes.router, prefix="/upload", tags=["upload"])
