from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import pandas as pd
import io
from icecream import ic

from src.services.bigquery_auth_service import BigQueryAuthService
from src.services.bigquery_upload_service import BigQueryDataUploadService
from src.handlers.upload_handler import UploadHandler
from src.models.bigquery.usuario_model import UsuarioBase


router = APIRouter()


mock_user = UsuarioBase(
    token="mocktoken",
    descr_prim_nome="Mock",
    descr_ult_nome="User",
    organizacao=99,
    descr_email="mockuser@mockorg.com",
    data_criacao="30/11/2023"
)

@router.post(
    "/",
    tags=["Upload", "Management"],
    summary="Upload Medicine Data",
    description="Upload medicine data in CSV or Excel format to BigQuery.",
    response_description="Success message if upload is successful."
)
async def upload_material_data(
    file: UploadFile = File(...),
    user: UsuarioBase = mock_user
):
    """
    Upload Medicine Data

    This endpoint allows you to upload medicine data in CSV or Excel format to BigQuery.

    - **file**: The CSV or Excel file containing medicine data.
    - **user**: (Optional) The user making the request.

    Returns:
    - **Dict[str, str]**: A success message if the upload is successful.
    - **500 Error**: An unexpected error occurred.
    """
    try:
        bq_auth_service = BigQueryAuthService(user)
        client, session, user_dataset = bq_auth_service.get_credentials()
        ic(f'User: {user.descr_email} with token: {user.token} from {user.organizacao} is uploading data: {file.filename}')
        ic(f'BigQuery client: {client} with session: {session} on dataset: {user_dataset}')
        bq_upload_service = BigQueryDataUploadService(bq_auth_service)
        upload_handler = UploadHandler(bq_upload_service)

        contents = await file.read()
        contents = io.BytesIO(contents)

        if file.filename.endswith('.csv'):
            try:
                ic('Parsing csv...')
                df = pd.read_csv(contents, sep=',', encoding='utf-8')
            except pd.errors.ParserError as e:
                ic(f'Error parsing CSV file: {e}')
                raise HTTPException(status_code=400, detail='Error parsing CSV file') from e
        elif file.filename.endswith('.xlsx'):
            try:
                ic('Parsing excel...')
                df = pd.read_excel(io.BytesIO(contents))
            except pd.errors.ParserError as e:
                ic(f'Error parsing Excel file: {e}')
                raise HTTPException(status_code=400, detail='Error parsing Excel file') from e
        else:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        upload_handler.upload_material_data(df)
        bq_auth_service.finish_session()

        return {"message": "Data uploaded successfully"}
    except Exception as e:
        ic(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get(
    "/reset-database",
    tags=["Remove", "Admin"],
    summary="Reset Database",
    description="Reset the database to its initial state.",
    response_description="Success message if database is reset successfully."
)
async def reset_database(
    user: UsuarioBase = mock_user
):
    """
    Reset Database

    This endpoint allows you to reset the database to its initial state.

    - **user**: (Optional) The user making the request.

    Returns:
    - **Dict[str, str]**: A success message if the database is reset successfully.
    - **500 Error**: An unexpected error occurred.
    """
    try:
        bq_auth_service = BigQueryAuthService(user)
        client, session, user_dataset = bq_auth_service.get_credentials()
        ic(f'User: {user.descr_email} with token: {user.token} from {user.organizacao} is resetting the database')
        ic(f'BigQuery client: {client} with session: {session} on dataset: {user_dataset}')
        #bq_upload_service = BigQueryDataUploadService(bq_auth_service)
        #upload_handler = UploadHandler(bq_upload_service)

        bq_auth_service.delete_all_tables(bq_auth_service.project_id, bq_auth_service.user_dataset) 
        bq_auth_service.create_all_tables(bq_auth_service.project_id, bq_auth_service.user_dataset)
        bq_auth_service.finish_session()

        return {"message": "Database reset successfully"}
    except Exception as e:
        ic(e)
        raise HTTPException(status_code=500, detail=str(e))