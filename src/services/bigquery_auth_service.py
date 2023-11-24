from google.cloud import bigquery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from icecream import ic

from src.models.user import User
from src.models.control import Base as ControlBase
from src.models.medicine import Base as MedicineBase
from src.models.origin import Base as OriginBase
from src.models.destination import Base as DestinationBase
from src.models.file import Base as FileBase
from src.models.type import Base as TypeBase


AUTHDATASET = {
    'mocktoken': 'Pharmawatch'
}

load_dotenv()


class BigQueryAuthService:
    def __init__(self, user: User = None):
        try:
            if user is not None:      
                self.user = user
                self.user_dataset = self.validate_user_token(user.token)
                self.project_id = os.getenv("GCP_PROJECT_ID")
                self.client = bigquery.Client.from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
                self.session = None
                self.engine = None
                self.initiate_session()
        except Exception as e:
            ic(e)
            raise Exception("Error creating BigQuery client")

    def _create_engine(self):
        if self.engine is None:
            try:
                connection_string = f"bigquery://{self.project_id}/{self.user_dataset}"
                self.engine = create_engine(connection_string)
            except Exception as e:
                ic(e)
                raise Exception("Error creating SQLAlchemy engine")

    def _create_session(self):
        if self.session is None:
            try:
                Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
                self.session = Session()
            except Exception as e:
                ic(e)
                raise Exception("Error creating SQLAlchemy session")

    def initiate_session(self):
        self._create_engine()
        self._create_session()

    def finish_session(self):
        self.session.close()

    def validate_user_token(self, user_token):
        # TODO: validate user token and return user dataset
        try:
            user_dataset = AUTHDATASET[user_token]
            return user_dataset
        except KeyError:
            raise Exception("Invalid user token")

    def get_credentials(self):
        return self.client, self.session, self.user_dataset
    
    
    def create_all_tables(self, project_id: str = None, dataset: str = None):
        try:
            project_id = project_id if project_id != None else os.getenv("GCP_PROJECT_ID")
            connection_string = f"bigquery://{project_id}/{dataset}"
            client = bigquery.Client.from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
            engine = create_engine(connection_string)
            Session = sessionmaker(bind=engine)
            session = Session()
        except Exception as e:
            ic(e)
            raise Exception("Error creating SQLAlchemy session")

        try:
            ic('Trying to create File table')
            FileBase.metadata.create_all(engine)
            ic('File table already exists')
        except Exception as e:
            ic(e)
        try:
            ic('Trying to create Type table')
            TypeBase.metadata.create_all(engine)
            ic('Type table already exists')
        except Exception as e:
            ic(e)
        try:
            ic('Trying to create Medicine table')
            MedicineBase.metadata.create_all(engine)
            ic('Medicine table already exists')
        except Exception as e:
            ic(e)
        try:
            ic('Trying to create Origin table')
            OriginBase.metadata.create_all(engine)
            ic('Origin table already exists')
        except Exception as e:
            ic(e)
        try:
            ic('Trying to create Destination table')
            DestinationBase.metadata.create_all(engine)
            ic('Destination table already exists')
        except Exception as e:
            ic(e)
        try:
            ic('Trying to create Control table')
            ControlBase.metadata.create_all(engine)
            ic('Control table already exists')
        except Exception as e:
            ic(e)
        
        ic("Tables created successfully!")

        session.close()