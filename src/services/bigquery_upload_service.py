from datetime import datetime
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import os
from icecream import ic

from src.models.type import Type
from src.models.medicine import Medicine
from src.models.origin import Origin
from src.models.destination import Destination
from src.models.file import File
from src.models.upload_data import RawMedicineData
from src.models.user import User
from src.models.control import Control

class BigQueryDataUploadService:
    def __init__(self, bigquery_client, user_dataset: str, user: User) -> None:
        self.client = bigquery_client
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.dataset_id = user_dataset
        self.user = user


    def execute_query(self, query: str):
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            return results.to_dataframe()
        except NotFound:
            return None
        
    def get_model_schema(self, model_instance):
        # Extract schema from Pydantic model instance
        schema = model_instance.__annotations__
        return [
            bigquery.SchemaField(name=key, field_type=self.get_bigquery_field_type(value))
            for key, value in schema.items()
        ]

    def get_bigquery_field_type(self, python_type):
        # Map Python types to BigQuery field types
        type_mapping = {
            int: "INTEGER",
            float: "FLOAT",
            str: "STRING",
            bool: "BOOLEAN",
        }
        return type_mapping.get(python_type, "STRING")

    def insert_into_table(self, table_name, data):
        table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
        schema = self.get_model_schema(data)
        ic(schema)
        
        try:
            table = self.client.get_table(table_id)
            ic(table)
        except NotFound:            
            table = self.client.create_table(bigquery.Table(table_id, schema=schema))
            ic(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

        data_dict = dict(data)

        # Insert data into the table with auto-detected schema
        errors = self.client.insert_rows_json(table, [data_dict], ignore_unknown_values=True)

        if errors:
            raise Exception(f"Error inserting data into table {table_id}")

        query = f"SELECT MAX(id_{table_name}) as id FROM `{self.project_id}.{self.dataset_id}.{table_name}`"
        result = self.execute_query(query)
        return result.iloc[0]["id"]

    def insert_and_get_id(self, key, data, month=None, year=None):
        month_year_clause = ""
        
        # Use getattr to access attribute values
        descr_key = getattr(data, f"descr_{key}")
        
        if month and year:
            month_year_clause = f" AND month = {month} AND year = {year}"

        query = f"SELECT id_{key} FROM `{self.project_id}.{self.dataset_id}.{key}` WHERE descr_{key} = '{descr_key}'{month_year_clause}"
        ic(query)

        result = self.execute_query(query)
        ic(result)

        ic("insert")
        if result is None:
            id = self.insert_into_table(key, data)
        elif result.empty:
            id = self.insert_into_table(key, data)
        else:
            id = result.iloc[0][f"id_{key}"]

        ic(id)

        return id

    def upload_medicine_data(self, data: RawMedicineData):
        current_date = datetime.utcnow().strftime("%Y%m%d%H%M%S")

        type_data = Type(
            descr_type = data.descr_unit_type
        )
        medicine_data = Medicine(
            descr_medicine = data.descr_medicine,
            id_type = self.insert_and_get_id("type", type_data),
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
            unit_value = data.unit_value,
            unit_quantity = data.unit_quantity,
            total_value = data.total_value,
            month = data.month,
            year = data.year,
            id_origin = self.insert_and_get_id("origin", origin_data),
            id_destination = self.insert_and_get_id("destination", destination_data),
            id_upload_file = self.insert_and_get_id("file", upload_file_data, data.month, data.year),
        )

        self.insert_into_table("control", main_data)