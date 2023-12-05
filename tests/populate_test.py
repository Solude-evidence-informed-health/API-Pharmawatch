import requests
from icecream import ic


BASE_URL = "http://localhost:8000"
#BASE_URL = "https://pharmawatch-api-iqdmxo5f2a-rj.a.run.app"
UPLOAD_URL = BASE_URL + "/upload"
RESET_URL = UPLOAD_URL + "/reset-database"
CSV_FILE_PATH = "./tests/data/pharmawatch.csv"

#user_token = "your_user_token"

#headers = {
#    "Authorization": f"Bearer {user_token}",
#}

files = {"file": ("pharmawatch.csv", open(CSV_FILE_PATH, "rb"))}
ic(files)


try:
    response = requests.get(RESET_URL)
    response = requests.post(UPLOAD_URL, files = files)
    response.raise_for_status()
    print("Data uploaded successfully")
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