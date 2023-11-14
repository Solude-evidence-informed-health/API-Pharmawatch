from google.cloud import bigquery
from icecream import ic

AUTHDATASET = {
    'mocktoken': 'Pharmawatch'
}

class BigQueryAuthService:
    client = None

    def __init__(self):
        pass

    def set_credentials(self, json_key_path):
        self.__class__.client = bigquery.Client.from_service_account_json(json_key_path)
        ic(self.__class__.client)

    def validate_user_token(self, user_token):
        try:
            user_dataset = AUTHDATASET[user_token]
            return user_dataset
        except:
            raise Exception("Invalid user token")

    def get_client(self, user_token):
        user_dataset = self.validate_user_token(user_token)
        return self.__class__.client, user_dataset
