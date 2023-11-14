from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import csv
import pandas as pd
import io
from icecream import ic

from src.services.bigquery_auth_service import BigQueryAuthService
from src.services.bigquery_upload_service import BigQueryDataUploadService
from src.models.upload_data import RawMedicineData
from src.models.user import User


router = APIRouter()
bq_auth_service = BigQueryAuthService()


mock_user = User(
    token="mocktoken",
    descr_first_name="Mock",
    descr_last_name="User",
    organization=99,
    descr_email="mockuser@mockorg.com"
)


@router.post("/")
async def upload_medicine_data(
    file: UploadFile = File(...),
    user: User = mock_user
):
    try:
        ic(file.filename)
        ic(user.token)
        client, user_dataset = bq_auth_service.get_client(user.token)
        upload_service = BigQueryDataUploadService(client, user_dataset, user)

        contents = await file.read()
        # read the file into a pandas dataframe according to the file type
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        df = df.where(pd.notnull(df), None)
        upload_data = df.to_dict(orient='records')

        for row in upload_data:
            try:
                row['Quantidade'] = row['Quantidade'].replace(',', '.')
                row['Valor unitário (R$)'] = row['Valor unitário (R$)'].replace(',', '.')
                row['Valor unitário (R$)'] = row['Valor unitário (R$)'].replace('.', '')
                row['Valor total (R$)'] = row['Valor total (R$)'].replace(',', '.')
                row['Valor total (R$)'] = row['Valor total (R$)'].replace('.', '')

                upload_data = RawMedicineData(
                    descr_medicine=str(row['Material']),
                    descr_unit_type=str(row['Unidade']),
                    unit_quantity=float(row['Quantidade']),
                    unit_value=float(row['Valor unitário (R$)']),
                    total_value=float(row['Valor total (R$)']),
                    month=int(row['Mês']),
                    year=int(row['Ano']),
                    descr_origin=str(row['Local']),
                    descr_destination=str(row['Destino']),
                )
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
            upload_service.upload_medicine_data(upload_data)

        return {"message": "Data uploaded successfully"}
    except Exception as e:
        ic(e)
        raise HTTPException(status_code=500, detail=str(e))