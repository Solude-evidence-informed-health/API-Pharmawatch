from datetime import datetime
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from icecream import ic

from src.services.bigquery_retrieval_service import BigQueryDataRetrievalService
from src.services.bigquery_auth_service import BigQueryAuthService


load_dotenv()


class BigQueryDataUploadService:
    def __init__(self, bq_auth_service: BigQueryAuthService):
        self.bq_auth_service = bq_auth_service
        self.retrieval_service = BigQueryDataRetrievalService(bq_auth_service)


    def insert_into_table(self, model, key : str, data : dict):
        try:
            ic(f"Inserting {key} descr_{key}")
            last_id = self.retrieval_service.fetch_last_id_from_table(key)
            if last_id is not None:
                new_id = last_id + 1
            else:
                new_id = 1
            data["id"] = new_id
            ic(new_id)
            ic(data)
            instance = model(**data)
            ic("Adding...")
            self.bq_auth_service.session.add(instance)
            ic("Commiting...")
            self.bq_auth_service.session.commit()
            ic("Commited...")
            return instance
        except Exception as e:
            ic(f"Error inserting {key} data: {e}")
            raise e

    def insert_and_get_id(self, model, key : str, data : dict, month : int = None, year : int = None):
        try:
            ic(f"Inserting and getting {key} id")
            month_year_clause = ""
            descr_key = data[f"descr_{key}"]

            if month and year:
                month_year_clause = f" AND month = {month} AND year = {year}"

            query = f"SELECT id FROM `{self.bq_auth_service.project_id}.{self.bq_auth_service.user_dataset}.{key}` WHERE descr_{key} = '{descr_key}'{month_year_clause}"

            result = self.retrieval_service.execute_query(query)
            
            if result is None:
                return self.insert_into_table(model, key, data).id

            return result[0][0]
        except Exception as e:
            ic(f"Error inserting and getting {key} id: {e}")
            raise e
        
    