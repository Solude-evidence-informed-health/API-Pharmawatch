from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from services.bigquery_auth_service import BigQueryAuthService
from services.bigquery_upload_service import BigQueryDataUploadService
from src.models.upload_data import RawMedicineData
from models.user import User
import csv
import io


router = APIRouter()


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
        client, user_dataset = BigQueryAuthService.get_client(user.token)
        upload_service = BigQueryDataUploadService(client, user_dataset, user)

        contents = await file.read()
        
        decoded_file = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(decoded_file)
        
        for row in csv_reader:
            try:
                upload_data = RawMedicineData(
                    descr_medicine=str(row['descr_medicine']),
                    descr_unit_type=str(row['descr_unit_type']),
                    unit_quantity=int(row['unit_quantity']),
                    unit_value=float(row['unit_value']),
                    total_value=float(row['total_value']),
                    month=int(row['month']),
                    year=int(row['year']),
                    descr_origin=str(row['descr_origin']),
                    descr_destination=str(row['descr_destination']),
                )
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
            upload_service.upload_medicine_data(upload_data)

        return {"message": "Data uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))