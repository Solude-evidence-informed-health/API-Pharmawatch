import os

FILTERS = ["type", "origin", "destination"]

class MedicinesQuerier:
    def __init__(self, user_dataset):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.dataset_id = user_dataset

    def prepare_where_clause(self, type, origin, destination):
        filters = []
        if type:
            filters.append(f"type = '{type}'")
        if origin:
            filters.append(f"origin = '{origin}'")
        if destination:
            filters.append(f"destination = '{destination}'")
        where_clause = ""
        if filters:
            where_clause = "WHERE " + " AND ".join(filters)
        return where_clause
    
    def prepare_order_by_clause(self, sort):
        order_by_clause = ""
        if sort:
            order_by_clause = f"ORDER BY {sort}"
        return order_by_clause

    def make_count_all_query(self, type, origin, destination):
        where_clause = self.prepare_where_clause(type, origin, destination)
        query = f"SELECT COUNT(*) as total FROM `{self.project_id}.{self.dataset_id}.medicines` {where_clause}"
        return query
    
    def make_select_query(self, type, origin, destination, sort, page, per_page):
        offset = (page - 1) * per_page
        where_clause = self.prepare_where_clause(type, origin, destination)
        order_by_clause = self.prepare_order_by_clause(sort)
        query = f"SELECT * FROM `{self.project_id}.{self.dataset_id}.medicines` {where_clause} {order_by_clause} LIMIT {per_page} OFFSET {offset}"
        return query
    
    def make_dict_filters_queries(self):
        filters = {}
        for filter in FILTERS:
            query = f"SELECT DISTINCT descr_{filter} FROM `{self.project_id}.{self.dataset_id}.{filter}`"
            filters[filter] = query
        return filters
    
    def make_insert_query(self, table, data):
        pass