import os
from typing import List
from icecream import ic

from src.services.bigquery_retrieval_service import BigQueryDataRetrievalService
from src.models.requests_data import FiltrosMaterialRequest
from src.models.response_data import FiltrosResponse, CurvaAbcMaterialResponse
from src.models.utils import AbcBase


FILTERS = {
    "material": "c",
    "tipo": "m",
    "origem": "c",
    "destino": "c"
}


class RetrievalHandler:
    def __init__(self, retrieval_service: BigQueryDataRetrievalService):
        self.retrieval_service = retrieval_service

    
    def _parse_dates(self, start_date: str = None, end_date: str = None):
        start_month = start_date.split("/")[1]
        end_month = end_date.split("/")[1]
        start_year = start_date.split("/")[2]
        end_year = end_date.split("/")[2]
        return int(start_month), int(end_month), int(start_year), int(end_year)
    
    def _parse_valid_months_and_years(self, start_month: int, end_month: int, start_year: int, end_year: int):
        valid_dates = ""
        # uniques valid dates
        set_dates = set()
        for year in range(start_year, end_year + 1):
            if year == start_year:
                for month in range(start_month, 13):
                    set_dates.add(f"{month}-{year}")
            elif year == end_year:
                for month in range(1, end_month + 1):
                    set_dates.add(f"{month}-{year}")
            else:
                for month in range(1, 13):
                    set_dates.add(f"{month}-{year}")
        valid_dates = "(" + ", ".join(set_dates) + ")"
        return valid_dates


    def _prepare_filters_where_clause(self, medicineFilters: FiltrosMaterialRequest, last_month: bool = False, last_last_month: bool = False):
        ic("Preparing filters where clause")
        try:
            filters = []
            where_clause = ""
            medicineFilters = medicineFilters.model_dump()
            ic(medicineFilters)
            ic("Filtering ids...")
            for filter in FILTERS.keys():
                if (f'id_{filter}' in medicineFilters):
                    if (medicineFilters[f'id_{filter}']) != None:
                        prefix = FILTERS[filter]
                        filters.append(f"{prefix}.id_{filter} IN ({', '.join([str(value) for value in medicineFilters[f'id_{filter}']])})")
            ic("Filtering dates...")
            if (medicineFilters['data_inicio'] != None) and (medicineFilters['data_fim'] != None):
                start_month, end_month, start_year, end_year = self._parse_dates(medicineFilters['data_inicio'], medicineFilters['data_fim'])
                if last_last_month or last_month:
                    if last_last_month and (end_month == 1):
                        month = 12
                        year = end_year - 1
                    if last_last_month and (end_month != 1):
                        month = end_month - 1
                        year = end_year
                    elif last_month:
                        month = end_month
                        year = end_year
                    date = f"{month}-{year}"
                    operation = "="
                else:
                    date = self._parse_valid_months_and_years(start_month, end_month, start_year, end_year)
                    operation = "IN"
                filters.append(f"c.uid_mes_ano {operation} {date}")
            if filters:
                where_clause = "WHERE " + " AND ".join(filters)
            ic(f"Where clause: {where_clause}")
            return where_clause
        except Exception as e:
            ic(f"Error preparing where clause: {e}")
            raise e
    

    def _prepare_order_by_clause(self, sort: List[str], ascending: bool, abc: bool = False):
        try:
            ic("Preparing order by clause")
            order_by_clause = ""
            if sort:
                prefix = ""
                order_by_clause = "ORDER BY " + ", ".join([f"{prefix}{column} {'ASC' if ascending else 'DESC'}" for column in sort])
            ic(f"Order by clause: {order_by_clause}")
            return order_by_clause
        except Exception as e:
            ic(f"Error preparing order by clause: {e}")
            raise e
        
    def _prepare_limit_offset_clause(self, page: int, per_page: int):
        try:
            ic("Preparing limit and offset clause")
            limit_offset_clause = f"LIMIT {per_page} OFFSET {per_page * (page - 1)}"
            ic(f"Limit offset clause: {limit_offset_clause}")
            return limit_offset_clause
        except Exception as e:
            ic(f"Error preparing limit offset clause: {e}")
            raise e
        
    def get_total_pages(self, result_dict, page_size):
        ic("Getting total for pagination")
        total_records = len(result_dict)
        return total_records, (total_records + page_size - 1) // page_size

    def retrieve_curva_abc(self, medicineFilters: FiltrosMaterialRequest):
        try:
            ic("Retrieving data with filters...")
            where_clause = self._prepare_filters_where_clause(medicineFilters)
            last_month_where_clause = self._prepare_filters_where_clause(medicineFilters, last_month=True)
            last_last_month_where_clause = self._prepare_filters_where_clause(medicineFilters, last_last_month=True)
            order_by_clause = self._prepare_order_by_clause(medicineFilters.ordenacao, medicineFilters.ordenacao_crescente)
            limit_offset_clause = self._prepare_limit_offset_clause(medicineFilters.page, medicineFilters.per_page)
            query = f"""
                WITH 
                    MATERIALINFO AS (
                        SELECT
                            m.descr_material AS material,
                            t.descr_tipo AS tipo,
                            SUM(c.quantidade_unidade) AS quantidade_unidade,
                            c.valor_unidade AS valor_unidade,
                            ROUND(SUM(c.valor_total), 2) AS valor_total,
                            ROUND(SUM(c.valor_total) / SUM(SUM(c.valor_total)) OVER(), 2) as percentual,
                            CASE
                                WHEN ROUND(SUM(c.valor_total) / SUM(SUM(c.valor_total)) OVER(), 2) >= 0.8 THEN 'A'
                                WHEN ROUND(SUM(c.valor_total) / SUM(SUM(c.valor_total)) OVER(), 2) < 0.8 AND ROUND(SUM(c.valor_total) / SUM(SUM(c.valor_total)) OVER(), 2) >= 0.05 THEN 'B'
                                ELSE 'C'
                            END AS curva_abc
                        FROM
                            `{self.retrieval_service.bq_auth_service.project_id}.{self.retrieval_service.bq_auth_service.user_dataset}.controle` AS c
                        LEFT JOIN
                            `{self.retrieval_service.bq_auth_service.project_id}.{self.retrieval_service.bq_auth_service.user_dataset}.material` AS m
                        ON
                            c.id_material = m.id
                        LEFT JOIN
                            `{self.retrieval_service.bq_auth_service.project_id}.{self.retrieval_service.bq_auth_service.user_dataset}.tipo` AS t
                        ON
                            m.id_tipo = t.id
                        {where_clause}
                        GROUP BY
                            m.descr_material,
                            t.descr_tipo,
                            c.valor_unidade
                    ),

                    ULTIMOMMES AS (
                        SELECT
                            m.descr_material AS material,
                            SUM(c.quantidade_unidade) AS quantidade_unidade
                        FROM
                            `{self.retrieval_service.bq_auth_service.project_id}.{self.retrieval_service.bq_auth_service.user_dataset}.controle` AS c
                        LEFT JOIN
                            `{self.retrieval_service.bq_auth_service.project_id}.{self.retrieval_service.bq_auth_service.user_dataset}.material` AS m
                        ON
                            c.id_material = m.id
                        LEFT JOIN
                            `{self.retrieval_service.bq_auth_service.project_id}.{self.retrieval_service.bq_auth_service.user_dataset}.tipo` AS t
                        ON
                            m.id_tipo = t.id
                        {last_month_where_clause}
                        GROUP BY
                            m.descr_material,
                            c.valor_unidade
                    ),

                    PENULTIMOMES AS (
                        SELECT
                            m.descr_material AS material,
                            SUM(c.quantidade_unidade) AS quantidade_unidade
                        FROM
                            `{self.retrieval_service.bq_auth_service.project_id}.{self.retrieval_service.bq_auth_service.user_dataset}.controle` AS c
                        LEFT JOIN
                            `{self.retrieval_service.bq_auth_service.project_id}.{self.retrieval_service.bq_auth_service.user_dataset}.material` AS m
                        ON
                            c.id_material = m.id
                        LEFT JOIN
                            `{self.retrieval_service.bq_auth_service.project_id}.{self.retrieval_service.bq_auth_service.user_dataset}.tipo` AS t
                        ON
                            m.id_tipo = t.id
                        {last_last_month_where_clause}
                        GROUP BY
                            m.descr_material,
                            c.valor_unidade
                    )

                SELECT
                    mi.material AS material,
                    mi.tipo AS tipo,
                    mi.quantidade_unidade AS quantidade_unidade,
                    mi.valor_unidade AS valor_unidade,
                    mi.valor_total AS valor_total,
                    mi.percentual AS percentual_valor_total,
                    mi.curva_abc AS curva_abc,
                    ROUND((um.quantidade_unidade / pm.quantidade_unidade) * 100, 2) as variacao_cp
                FROM
                    MATERIALINFO AS mi
                LEFT JOIN
                    ULTIMOMMES AS um
                ON
                    mi.material = um.material
                LEFT JOIN
                    PENULTIMOMES AS pm
                ON
                    mi.material = pm.material
                {order_by_clause}
                {limit_offset_clause}
            """
            result = self.retrieval_service.execute_query(query)
            return result
        except Exception as e:
            ic(f"Error retrieving data with filters: {e}")
            raise e
     

    def parse_response_curva_abc(self, result, page, per_page):
        try:
            ic("Parsing response material list")
            material_list = []
            for result_record in result:
                ic(result)
                material_list.append(AbcBase(**result_record))
            total_records, total_pages = self.get_total_pages(material_list, per_page)
            response_material_list = CurvaAbcMaterialResponse(
                data = material_list,
                page = page,
                per_page = per_page,
                total_pages = total_pages,
                total = total_records,
            )
            ic(response_material_list)
            return response_material_list
        except Exception as e:
            ic(f"Error parsing response material list: {e}")
            raise e
    
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