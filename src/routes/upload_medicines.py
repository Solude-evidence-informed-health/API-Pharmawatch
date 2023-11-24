from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import pandas as pd
import io
from icecream import ic

from src.services.bigquery_auth_service import BigQueryAuthService
from src.services.bigquery_upload_service import BigQueryDataUploadService
from src.handlers.upload_handler import UploadHandler
from src.models.user import User


router = APIRouter()


mock_user = User(
    token="mocktoken",
    descr_first_name="Mock",
    descr_last_name="User",
    organization=99,
    descr_email="mockuser@mockorg.com"
)


@router.post(
        "/",
        tags=["Upload", "Management"],
        summary="Upload Medicine Data",
        description="Upload medicine data in CSV or Excel format to BigQuery.",
        response_description="Success message if upload is successful."
)
async def upload_medicine_data(
    file: UploadFile = File(...),
    user: User = mock_user
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
        ic(f'User: {user.descr_email} with token: {user.token} from {user.organization} is uploading data: {file.filename}')
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
        
        number_columns = ['Quantidade', 'Valor unitário (R$)', 'Valor total (R$)']
        for col in number_columns:
            df[col] = df[col].apply(lambda x: x.replace(".", ""))
            df[col] = df[col].apply(lambda x: x.replace(",", "."))
            df[col] = df[col].astype(float)

        upload_data = df.to_dict(orient='records')

        upload_handler.upload_medicine_data(upload_data)
        bq_auth_service.finish_session()

        return {"message": "Data uploaded successfully"}
    except Exception as e:
        ic(e)
        raise HTTPException(status_code=500, detail=str(e))