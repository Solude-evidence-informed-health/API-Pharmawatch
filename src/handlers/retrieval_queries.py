import os
from typing import List

from src.models.requests_data import MedicineFilters


FILTERS = ["medicine", "type", "origin", "destination"]


class MedicinesQuerier:
    def __init__(self, user_dataset: str):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.dataset_id = user_dataset

    def prepare_where_clause(self, id_medicine: List[int], id_type: List[int], id_origin: List[int], id_destination: List[int]):
        filters = []
        where_clause = ""
        # filter by a list of ids for each column
        if id_medicine:
            filters.append(f"id_medicine IN ({', '.join([str(id) for id in id_medicine])})")
        if id_type:
            filters.append(f"id_type IN ({', '.join([str(id) for id in id_type])})")
        if id_origin:
            filters.append(f"id_origin IN ({', '.join([str(id) for id in id_origin])})")
        if id_destination:
            filters.append(f"id_destination IN ({', '.join([str(id) for id in id_destination])})")
        if filters:
            where_clause = "WHERE " + " AND ".join(filters)
        return where_clause
    
    def prepare_order_by_clause(self, sort: List[str], ascending: bool):
        order_by_clause = ""
        # order by a list of columns in ascending or descending order
        if sort:
            order_by_clause = "ORDER BY " + ", ".join([f"{column} {'ASC' if ascending else 'DESC'}" for column in sort])
        return order_by_clause

    def make_count_all_query(self, filters: MedicineFilters):
        where_clause = self.prepare_where_clause(filters.id_type, filters.id_origin, filters.id_destination)
        query = f"SELECT COUNT(*) as total FROM `{self.project_id}.{self.dataset_id}.medicines` {where_clause}"
        return query
    
    def make_select_query(self, filters: MedicineFilters):
        offset = (filters.page - 1) * filters.per_page
        where_clause = self.prepare_where_clause(type, filters.id_origin, filters.id_destination)
        order_by_clause = self.prepare_order_by_clause(filters.sort)
        query = f"""
            SELECT
                m.id_medicine,
                m.descr_medicine,
                m.id_type
            FROM
                `{self.project_id}.{self.dataset_id}.medicines` m
            JOIN
                `{self.project_id}.{self.dataset_id}.control` c
            ON
                m.id_medicine = c.id_medicine
            {where_clause}
            {order_by_clause}
            LIMIT
                {filters.per_page}
            OFFSET
                {offset}
        """
        return query
    
    def make_dict_filters_queries(self):
        filters = {}
        for filter in FILTERS:
            query = f"SELECT id_{filter}, descr_{filter} FROM `{self.project_id}.{self.dataset_id}.{filter}`"
            filters[filter] = query
        return filters