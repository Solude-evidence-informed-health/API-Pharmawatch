title="Pharmawatch API"

description="Pharmawatch API is a Solude's REST API that allows communication between the Pharmawatch web application and the Pharmawatch database on BigQuery to retrieve and upload data in a secure way and with the proper authentication."

version="1.2.10"

tags_metadata = [
        {"name": "Filters", "description": "Operations related to filters of data"},
        {"name": "Materials", "description": "Operations related to hospital materials"},
        {"name": "Upload", "description": "Operations related to data upload of data"},
        {"name": "Retrieval", "description": "Operations related to data retrieval of data"},
        {"name": "Management", "description": "Operations related to data management as upload and removal in user level"},
        {"name": "Removal", "description": "Operations related to data removal"},
        {"name": "Admin", "description": "Operations related to administrative tasks"}
    ]

openapi_url="/openapi.json"

docs_url="/docs"

redoc_url="/redoc"

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