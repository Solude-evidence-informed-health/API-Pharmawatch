import requests
from icecream import ic

BASE_URL = "http://localhost:8000/materiais"
#BASE_URL = "https://pharmawatch-api-iqdmxo5f2a-rj.a.run.app/materiais"
MATERIALS_URL = BASE_URL + "/"
FILTERS_URL = BASE_URL + "/filtros"

filters = {
    #"ordenacao" : ["material", "tipo", "curva_abc"],
    #"ordenacao_crescente" : True,
    #"id_material" : [1, 2, 3, 4, 5],
    #"id_tipo" : [1, 2, 3],
    #"id_origem" : [1, 2, 3],
    #"id_destino" : [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "data_inicio" : "01/08/2021",
    "data_fim": "01/02/2022",
    "page" : 1,
    "per_page" : 5
}

try:
    if True:
        ic("Skipping valid filters retrieval...")
    else:
        ic("Retrieving valid filters...")
        response = requests.get(FILTERS_URL)
        response.raise_for_status()
        ic(response.json())
        ic("Valid filters data retrieved successfully")
except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
    print(f"An unexpected error occurred: {err}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


try:
    ic("Retrieving valid materials abc curve...")
    ic(MATERIALS_URL)
    response = requests.get(
        MATERIALS_URL,
        params=filters
    )
    response.raise_for_status()
    ic(response.json())
    ic("materials abc curve data retrieved successfully")
except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
    print(f"An unexpected error occurred: {err}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")