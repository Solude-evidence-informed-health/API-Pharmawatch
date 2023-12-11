from fastapi import APIRouter, HTTPException, Query, Depends
from icecream import ic

from src.services.bigquery_auth_service import BigQueryAuthService
from src.services.bigquery_retrieval_service import BigQueryDataRetrievalService
from src.handlers.retrieval_handler import RetrievalHandler
from src.models.response_data import FiltrosResponse, CurvaAbcMaterialResponse
from src.models.requests_data import FiltrosMaterialRequest
from src.models.bigquery.usuario_model import UsuarioBase


router = APIRouter()

mock_user = UsuarioBase(
    token="mocktoken",
    descr_prim_nome="Mock",
    descr_ult_nome="User",
    organizacao=99,
    descr_email="mockuser@mockorg.com",
    data_criacao="30/11/2023"
)


@router.get(
        "/",
        tags=["Materials", "Retrieval"],
        response_model = CurvaAbcMaterialResponse,
        summary="Retrieve Complete ABC Curve of materials used in a given period",
        description="Given a set of filters, retrieves the complete ABC Curve of materials used in a given period."
        )
async def get_materials_abc_curve(
    filters: FiltrosMaterialRequest = Depends(FiltrosMaterialRequest),
    user: UsuarioBase = mock_user
):
    """
    Retrieve Complete Information of materials

    This endpoint allows you to retrieve a list of materials based on the provided filters.

    - **filters**: The filters to apply to the materials list.
    - **user**: (Optional) The user making the request. Right now, this is only used to mock the user making the request. When not provided, it's used the mock token provided by the own server.

    Returns:
    - **CurvaAbcMaterialResponse**: The list of materials matching the provided filters.
    - **500 Error**: An unexpected error occurred.
    """
    try:
        bq_auth_service = BigQueryAuthService(user)
        client, session, user_dataset = bq_auth_service.get_credentials()
        ic(f'User: {user.descr_email} with token: {user.token} from {user.organizacao}')
        ic(f'BigQuery client: {client} with session: {session} on dataset: {user_dataset}')
        ic(f'Requesting data with filters: {filters}')
        bq_retrieval_service = BigQueryDataRetrievalService(bq_auth_service)
        retrieval_handler = RetrievalHandler(bq_retrieval_service)

        result = retrieval_handler.retrieve_curva_abc(filters)
        response_medicine_list = retrieval_handler.parse_response_curva_abc(result, filters.page, filters.per_page)

        bq_auth_service.finish_session()

        return response_medicine_list
    except Exception as e:
        ic(f"Error retrieving data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
        "/filtros",
        response_model = FiltrosResponse,
        tags=["Materials", "Filters", "Retrieval"],
        summary="Retrieve Valid Materials Filters",
        description="Retrieve the valid filters that can be applied to the materials list."
        )
async def get_materials_filters(
    user: UsuarioBase = mock_user
):
    """
    Retrieve Valid Materials Filters

    This endpoint allows you to retrieve the valid filters that can be applied to the materials list.

    - **user**: (Optional) The user making the request. Right now, this is only used to mock the user making the request. When not provided, it's used the mock token provided by the own server.

    Returns:
    - **ResponseFilters**: The valid filters for materials.
    - **500 Error**: An unexpected error occurred.
    """
    try:
        bq_auth_service = BigQueryAuthService(user)
        client, session, user_dataset = bq_auth_service.get_credentials()
        ic(f'User: {user.descr_email} with token: {user.token} from {user.organizacao}')
        ic(f'BigQuery client: {client} with session: {session} on dataset: {user_dataset}')
        bq_retrieval_service = BigQueryDataRetrievalService(bq_auth_service)
        retrieval_handler = RetrievalHandler(bq_retrieval_service)

        result_filters = retrieval_handler.retrieve_valid_filters()
        valid_filters = retrieval_handler.parse_valid_filters(result_filters)

        bq_auth_service.finish_session()

        return valid_filters
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))