from fastapi import APIRouter, Query, HTTPException
from services.bigquery_auth_service import BigQueryAuthService
from services.bigquery_upload_service import BigQueryDataUploadService
from services.bigquery_retrieval_service import BigQueryDataRetrievalService
from src.handlers.retrieval_queries import MedicinesQuerier
from models.response_data import ResponseMedicineList, ResponseFilters
from models.requests_data import MedicineFilters
from models.user import User
from icecream import ic


router = APIRouter()


mock_user = User(
    token="mocktoken",
    descr_first_name="Mock",
    descr_last_name="User",
    organization=99,
    descr_email="mockuser@mockorg.com"
)


@router.get(
        "/",
        response_model = ResponseMedicineList
        )
async def get_medicamentos(
    filters : MedicineFilters = MedicineFilters(),
    user : User = mock_user
):
    try:
        client, user_dataset = BigQueryAuthService.get_client(user.token)
        retrieval_service = BigQueryDataRetrievalService(client)
        med_querier = MedicinesQuerier(user_dataset)

        count_all_query = med_querier.make_count_all_query(type, filters.origin, filters.destination)
        total_results = retrieval_service.execute_query(count_all_query).to_dataframe().total[0]

        select_query = med_querier.make_select_query(type, filters.origin, filters.destination, filters.sort, filters.page, filters.per_page)
        results = retrieval_service.execute_query(select_query)
        ic(type(results))

        total_pages = retrieval_service.get_total_pages(total_results, filters.per_page)

        response_data = ResponseMedicineList(
            data = results,
            page = filters.page,
            per_page = filters.per_page,
            total_pages = total_pages,
            total = total_results,
        )
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
        "/filtros",
        response_model=ResponseFilters
        )
async def get_medicamentos_filters(
    user: User = mock_user
):
    try:
        client, user_dataset = BigQueryAuthService.get_client(user.token)
        upload_service = BigQueryDataUploadService(client)
        med_querier = MedicinesQuerier(user_dataset)

        filters_queries = med_querier.make_dict_filters_queries() 

        data = {}

        for filter, query in filters_queries.items():
            data[filter] = upload_service.execute_query(query).to_dataframe()[f"descr_{filter}"].tolist()
        
        response_data = {}

        for filter, values in data.items():
            response_data[filter] = values
    
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
