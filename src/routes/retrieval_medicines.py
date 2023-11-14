from fastapi import APIRouter, HTTPException
from icecream import ic

from src.services.bigquery_auth_service import BigQueryAuthService
from src.services.bigquery_upload_service import BigQueryDataUploadService
from src.services.bigquery_retrieval_service import BigQueryDataRetrievalService
from src.handlers.retrieval_queries import MedicinesQuerier
from src.models.response_data import ResponseMedicineList, ResponseFilters
from src.models.requests_data import MedicineFilters
from src.models.medicine import Medicine
from src.models.user import User


router = APIRouter()
bq_auth_service = BigQueryAuthService()


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
        client, user_dataset = bq_auth_service.get_client(user.token)
        retrieval_service = BigQueryDataRetrievalService(client)
        med_querier = MedicinesQuerier(user_dataset)

        count_all_query = med_querier.make_count_all_query(filters)
        total_results = retrieval_service.execute_query(count_all_query).to_dataframe().total[0]

        select_query = med_querier.make_select_query(filters)

        results = retrieval_service.execute_query(select_query).to_dataframe().to_dict(orient="records")
        results = [dict(result) for result in results]
        results_list = []
        for result in results:
            results_list.append(
                Medicine(
                    id_medicine = result["id_medicine"],
                    descr_medicine = result["descr_medicine"],
                    id_type = result["id_type"],    
                )
            )

        total_pages = retrieval_service.get_total_pages(total_results, filters.per_page)

        response_data = ResponseMedicineList(
            data = results_list,
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
        client, user_dataset = bq_auth_service.get_client(user.token)
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