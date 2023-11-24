import requests
from icecream import ic

BASE_URL = "http://localhost:8000/medicamentos"
MEDICINES_URL = BASE_URL + "/"
FILTERS_URL = BASE_URL + "/filtros"

filters = {
    "id_medicine" : [1, 2, 3],
    "id_type" : [1, 2, 3],
    "id_origin" : [1, 2, 3],
    "id_destination" : [1, 2, 3],
    "sort" : ["medicine", "type", "origin", "destination"],
    "ascending" : True,
    "page" : 1,
    "per_page" : 10
}

try:
    if False:
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
    ic("Retrieving valid medicines...")
    response = requests.get(
        MEDICINES_URL,
        json = {
            "filters" : filters
        }
    )
    response.raise_for_status()
    ic(response.json())
    ic("Medicines data retrieved successfully")
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