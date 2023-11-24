import os
from typing import List
from icecream import ic

from src.services.bigquery_retrieval_service import BigQueryDataRetrievalService
from src.models.requests_data import MedicineFilters
from src.models.response_data import ResponseMedicineList, ResponseControlList


FILTERS = {
    "medicine": "c",
    "type": "m",
    "origin": "c",
    "destination": "c"
}


class RetrievalHandler:
    def __init__(self, retrieval_service: BigQueryDataRetrievalService):
        self.retrieval_service = retrieval_service

    def _prepare_filters_where_clause(self, medicineFilters: MedicineFilters):
        ic("Preparing filters where clause")
        try:
            filters = []
            where_clause = ""
            medicineFilters = medicineFilters.model_dump()
            for filter in FILTERS.keys():
                if (f'id_{filter}' in medicineFilters):
                    if (medicineFilters[f'id_{filter}']) != None:
                        prefix = FILTERS[filter]
                        filters.append(f"{prefix}.id_{filter} IN ({', '.join([str(value) for value in medicineFilters[f'id_{filter}']])})")
            if filters:
                where_clause = "WHERE " + " AND ".join(filters)
            ic(f"Where clause: {where_clause}")
            return where_clause
        except Exception as e:
            ic(f"Error preparing filters where clause: {e}")
            raise e
    
    def _prepare_order_by_clause(self, sort: List[str], ascending: bool):
        try:
            ic("Preparing order by clause")
            order_by_clause = ""
            if sort:
                order_by_clause = "ORDER BY " + ", ".join([f"{FILTERS[column]}.id_{column} {'ASC' if ascending else 'DESC'}" for column in sort])
            ic(f"Order by clause: {order_by_clause}")
            return order_by_clause
        except Exception as e:
            ic(f"Error preparing order by clause: {e}")
            raise e

    def retrieve_all_with_medicine_filters(self, medicineFilters: MedicineFilters):
        try:
            ic("Retrieving data with filters...")
            where_clause = self._prepare_filters_where_clause(medicineFilters)
            order_by_clause = self._prepare_order_by_clause(medicineFilters.sort, medicineFilters.ascending)
            query = f"""
                SELECT
                    c.id,
                    c.id_medicine,
                    m.descr_medicine,
                    m.id_type,
                    c.unit_value,
                    c.unit_quantity,
                    c.total_value,
                    c.month,
                    c.year,
                    c.id_origin,
                    c.id_destination,
                    c.id_file
                FROM
                    `{self.retrieval_service.bq_auth_service.project_id}.{self.retrieval_service.bq_auth_service.user_dataset}.medicine` m
                JOIN
                    `{self.retrieval_service.bq_auth_service.project_id}.{self.retrieval_service.bq_auth_service.user_dataset}.control` c
                ON
                    m.id = c.id_medicine
                {where_clause}
                {order_by_clause}
            """
            result = self.retrieval_service.execute_query(query)
            return result
        except Exception as e:
            ic(f"Error retrieving data with filters: {e}")
            raise e

    def parse_response_medicine_list(self, result, page, per_page):
        try:
            ic("Parsing response medicine list")
            medicine_list = []
            for result_record in result:
                medicine_list.append(ResponseControlList(**result_record))
            total_records, total_pages = self.get_total(medicine_list, per_page)
            response_medicine_list = ResponseMedicineList(
                data = medicine_list,
                page = page,
                per_page = per_page,
                total_pages = total_pages,
                total = total_records,
            )
            ic(response_medicine_list)
            return response_medicine_list
        except Exception as e:
            ic(f"Error parsing response medicine list: {e}")
            raise e
    
    def get_total(self, result_dict, page_size):
        ic("Getting total for pagination")
        total_records = len(result_dict)
        return total_records, (total_records + page_size - 1) // page_size
    
    def retrieve_valid_filters(self):
        try:
            ic("Making dict filters queries")
            result_filters = {}
            for filter in FILTERS.keys():
                query = f"SELECT id, descr_{filter} FROM `{self.retrieval_service.bq_auth_service.project_id}.{self.retrieval_service.bq_auth_service.user_dataset}.{filter}`"
                result_filters[filter] = self.retrieval_service.execute_query(query)
            return result_filters
        except Exception as e:
            ic(f"Error making dict filters queries: {e}")
            raise e
    
    def parse_valid_filters(self, result_filters):
        try:
            ic("Parsing valid filters")
            valid_filters = {}
            for filter, result in result_filters.items():
                result = sorted(result, key=lambda x: x[1])
                valid_filters[filter] = result
            ic(valid_filters)
            return valid_filters
        except Exception as e:
            ic(f"Error parsing valid filters: {e}")
            raise e