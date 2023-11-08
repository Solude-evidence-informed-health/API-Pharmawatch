from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from services.bigquery_auth_service import BigQueryAuthService
from services.bigquery_upload_service import BigQueryDataUploadService
from models.upload_data import UploadData
from models.user import User
import csv
import io


router = APIRouter()


@router.post("/")
async def upload_data(
    file: UploadFile = File(...),
    user: User = {"Mock user"}
):
    try:
        client = BigQueryAuthService.get_client()
        upload_service = BigQueryDataUploadService(client)

        contents = await file.read()
        
        decoded_file = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(decoded_file)
        
        for row in csv_reader:
            upload_data = UploadData(
                description_medicine=row['description_medicine'],
                quantity=int(row['quantity']),
                unit_value=float(row['unit_value']),
                type=row['type'],
                month=int(row['month']),
                year=int(row['year']),
                origin=row['origin'],
                destination=row['destination'],
            )
            upload_service.upload_data(upload_data)

        return {"message": "Data uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))