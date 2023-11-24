from icecream import ic
from datetime import datetime

from src.models.type import TypeTable
from src.models.medicine import MedicineTable
from src.models.origin import OriginTable
from src.models.destination import DestinationTable
from src.models.file import FileTable
from src.models.upload_data import RawMedicineData
from src.models.control import ControlTable
from src.services.bigquery_upload_service import BigQueryDataUploadService

class UploadHandler:
    def __init__(self, upload_service: BigQueryDataUploadService):
        self.upload_service = upload_service

    def upload_medicine_data(self, upload_data: dict):
        ic("Uploading data...")
        current_date = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")
        random_hash = hash(str(upload_data)) % 10000000000
        ic(random_hash)

        for data in upload_data:
            data = RawMedicineData(
                descr_medicine=str(data['Material']),
                descr_unit_type=str(data['Unidade']),
                unit_quantity=float(data['Quantidade']),
                unit_value=float(data['Valor unitário (R$)']),
                total_value=float(data['Valor total (R$)']),
                month=int(data['Mês']),
                year=int(data['Ano']),
                descr_origin=str(data['Local']),
                descr_destination=str(data['Destino']),
            )
            try:
                type_data = {
                    "descr_type": data.descr_unit_type
                }

                medicine_data = {
                    "descr_medicine": data.descr_medicine,
                    "id_type": self.upload_service.insert_and_get_id(TypeTable, "type", type_data),
                }

                origin_data = {
                    "descr_origin": data.descr_origin
                }

                destination_data = {
                    "descr_destination": data.descr_destination
                }

                upload_file_data = {
                    "user_token": self.upload_service.bq_auth_service.user.token,
                    "upload_date": current_date,

                    "descr_file": f'{random_hash}-{self.upload_service.bq_auth_service.user.descr_email}-{current_date}.csv'
                }

                main_data = {
                    "id_medicine": self.upload_service.insert_and_get_id(MedicineTable, "medicine", medicine_data),
                    "unit_value": data.unit_value,
                    "unit_quantity": data.unit_quantity,
                    "total_value": data.total_value,
                    "month": data.month,
                    "year": data.year,
                    "id_origin": self.upload_service.insert_and_get_id(OriginTable, "origin", origin_data),
                    "id_destination": self.upload_service.insert_and_get_id(DestinationTable, "destination", destination_data),
                    "id_file": self.upload_service.insert_and_get_id(FileTable, "file", upload_file_data),
                }

                self.upload_service.insert_into_table(ControlTable, "control", main_data)
            except Exception as e:
                ic(f"Error uploading data: {e}")
                raise e