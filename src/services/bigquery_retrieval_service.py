from sqlalchemy.orm import Session
from dotenv import load_dotenv
from icecream import ic
import os

from src.services.bigquery_auth_service import BigQueryAuthService


load_dotenv()


class BigQueryDataRetrievalService:
    def __init__(self, bq_auth_service: BigQueryAuthService):
        self.bq_auth_service = bq_auth_service


    def execute_query(self, query : str):
        try:
            ic(f"Trying to execute query: {query}")
            result = self.bq_auth_service.session.execute(query)
            result = result.fetchall()
            ic(f'Query result: {result}')
            if result is None or result == []:
                ic("Result is none")
                return None
            return result
        except Exception as e:
            ic(f"Error on executing query: {e}")
            return None
        
    def fetch_last_id_from_table(self, key : str):
        try:
            ic(f"Fetching last ID from {key} table")
            query = f"SELECT id FROM `{self.bq_auth_service.project_id}.{self.bq_auth_service.user_dataset}.{key}` ORDER BY id DESC LIMIT 1"
            result = self.execute_query(query)
            if result is not None:
                last_id = result[0][0]
                ic(last_id)
                return last_id
            return None
        except Exception as e:
            ic(f"Error fetching last ID from {key} table: {e}")
            return None