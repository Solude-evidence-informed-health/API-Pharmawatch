from datetime import datetime
import os
from icecream import ic

from models.type import Type
from models.medicine import Medicine
from models.origin import Origin
from models.destination import Destination
from models.file import File
from models.upload_data import RawMedicineData
from models.user import User
from models.control import Control

class BigQueryDataUploadService:
    def __init__(self, bigquery_client, user_dataset: str, user: User) -> None:
        self.client = bigquery_client
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.dataset_id = user_dataset
        self.user = user


    def execute_query(self, query: str):
        query_job = self.client.query(query)
        results = query_job.result()
        return results

    def insert_into_table(self, table_name, data):
        table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"

        table = self.client.get_table(table_id)
        errors = self.client.insert_rows_json(table, [data], ignore_unknown_values=True)

        if errors:
            raise Exception(f"Error inserting data into table {table_id}")

        query = f"SELECT MAX(id) as id FROM `{self.project_id}.{self.dataset_id}.{table_name}`"
        result = self.execute_query(query).to_dataframe()
        return result.iloc[0]["id"]

    def insert_and_get_id(self, key, data, month=None, year=None):
        month_year_clause = ""
        params = {"descr_key": data.get(f"descr_{key}")}
        
        if month and year:
            month_year_clause = " AND month = @month AND year = @year"
            params.update({"month": month, "year": year})

        query = f"SELECT id_{key} FROM `{self.project_id}.{self.dataset_id}.{key}` WHERE descr_{key} = @descr_key{month_year_clause}"
        ic(query)

        result = self.execute_query(query, params).to_dataframe()

        if result.empty:
            id = self.insert_into_table(key, data)
        else:
            id = result.iloc[0][f"id_{key}"]

        return id
    

    def upload_medicine_data(self, data: RawMedicineData):
        current_date = datetime.utcnow().strftime("%Y%m%d%H%M%S")

        type_data = Type(
            descr_type = data.descr_unit_type
        )
        medicine_data = Medicine(
            descr_medicine = data.descr_medicine,
            id_type = self.insert_and_get_id("type", type_data),
            unit_value = data.unit_value,
            month = data.month,
            year = data.year,
        )
        origin_data = Origin(
            descr_origin = data.descr_origin
        )
        destination_data = Destination(
            descr_destination = data.descr_destination
        )
        upload_file_data = File(
            user_token = self.user.token,
            month = data.month,
            year = data.year,
            upload_date = current_date,
            descr_file = f'{data.month}-{data.year}-{self.user.descr_email}-{current_date}.csv'
        )

        main_data = Control(
            id_medicine = self.insert_and_get_id("medicine", medicine_data, data.month, data.year),
            unit_quantity = data.unit_quantity,
            total_value = data.total_value,
            month = data.month,
            year = data.year,
            id_origin = self.insert_and_get_id("origin", origin_data),
            id_destination = self.insert_and_get_id("destination", destination_data),
            id_upload_file = self.insert_and_get_id("file", upload_file_data, data.month, data.year),
        )

        self.insert_into_table("control", main_data)