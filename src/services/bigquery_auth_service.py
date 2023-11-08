from google.cloud import bigquery

class BigQueryAuthService:
    client = None

    def __init__(self):
        pass

    def set_credentials(self, json_key_path):
        self.__class__.client = bigquery.Client.from_service_account_json(json_key_path)

    def get_client(self):
        return self.__class__.client
