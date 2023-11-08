from google.cloud import bigquery
from datetime import datetime

class BigQueryDataUploadService:
    def __init__(self, bigquery_client):
        self.client = bigquery_client

    def get_type_id(self, type_description):
        # Get the ID of the medicine type from the 'type_table'
        type_query = f"SELECT id_type FROM `{PROJECT_ID}.{DATASET_ID}.type_table` WHERE description_type = '{type_description}'"
        type_result = self.execute_query(type_query).to_dataframe()

        if type_result.empty:
            # If the type doesn't exist, insert it
            type_data = {"description_type": type_description}
            type_id = self.insert_into_table("type_table", type_data)
        else:
            type_id = type_result.iloc[0]["id_type"]

        return type_id

    def upload_medicine_data(self, data, user):
        type_query = f"SELECT id_medicine FROM `{PROJECT_ID}.{DATASET_ID}.medicine` WHERE description_medicine = '{data.description_medicine}'"
        type_result = self.execute_query(type_query).to_dataframe()

        if type_result.empty:
            # If the type doesn't exist, insert it
            type_data = {"description_medicine": data.description_medicine, "unit_value": data.unit_value}
            type_id = self.insert_into_table("medicine", type_data)
        medicine_data = {
            "description_medicine": data.description_medicine,
            "id_type": self.get_type_id(data.type),
            "unit_value": data.unit_value,
        }


    def upload_data(self, data, user):

        medicine_data = {
            "description_medicine": data.description_medicine,
            "id_type": self.get_type_id(data.type),
            "unit_value": data.unit_value,
        }

        origin_data = {"description_origin": data.origin}
        
        destination_data = {"description_destination": data.destination}

        upload_file_data = {
            "id_user": user.id, # Mock user ID
            "upload_date": datetime.now(),
        }

        medicine_id = self.insert_into_table("medicines_table", medicine_data)
        origin_id = self.insert_into_table("origin_table", origin_data)
        destination_id = self.insert_into_table("destination_table", destination_data)
        file_id = self.insert_into_table("files_table", upload_file_data)

        main_data = {
            "id_medicine": medicine_id,
            
            "quantity": data.quantity,
            "total_value": data.total_value,
            "month": data.month,
            "year": data.year,
            "id_origin": origin_id,
            "id_destination": destination_id,
            "id_upload_file": file_id,
        }

        main_table_id = f"{PROJECT_ID}.{DATASET_ID}.control_table"
        self.insert_into_table(main_table_id, main_data)



    def insert_into_table(self, table_id, data):
        table = self.client.get_table(table_id)
        errors = self.client.insert_rows(table, [data])

        if errors:
            raise Exception(f"Error inserting data into table {table_id}")

        # Get the ID of the inserted row
        query = f"SELECT LAST_INSERT_ID() as id"
        result = self.execute_query(query).to_dataframe()
        return result.iloc[0]["id"]

    def execute_query(self, query):
        query_job = self.client.query(query)
        results = query_job.result()
        return results
