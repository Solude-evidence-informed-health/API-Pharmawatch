import requests
from icecream import ic


BASE_URL = "http://localhost:8000"
CSV_FILE_PATH = "./tests/data/pharmawatch.csv"


mock_user = {
    "token" :  "mocktoken",
    "descr_first_name" : "Mock",
    "descr_last_name" : "User",
    "organization" : 99,
    "descr_email" : "mockuser@mockorg.com"
}


# Replace the URL with the actual URL of your API endpoint
api_url = "http://localhost:8000/upload/"

# Replace the path with the actual path to your CSV file
csv_file_path = "./tests/data/pharmawatch.csv"

# Replace with the actual user token
#user_token = "your_user_token"

#headers = {
#    "Authorization": f"Bearer {user_token}",
#}

files = {"file": ("pharmawatch.csv", open(csv_file_path, "rb"))}
ic(files)

try:
    response = requests.post(api_url, files = files)
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