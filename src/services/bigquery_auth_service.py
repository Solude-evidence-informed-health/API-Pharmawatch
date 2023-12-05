from google.cloud import bigquery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from icecream import ic

from src.models.bigquery.usuario_model import UsuarioBase

from src.models.bigquery.usuario_model import Base as UserBase
from src.models.bigquery.controle_model import Base as ControleBase
from src.models.bigquery.material_model import Base as MaterialBase
from src.models.bigquery.tipo_model import Base as TipoBase
from src.models.bigquery.tipo_unidade_model import Base as TipoUnidadeBase
from src.models.bigquery.administracao_model import Base as AdministracaoBase
from src.models.bigquery.apresent_farmaceutica_model import Base as ApresentFarmaceuticaBase
from src.models.bigquery.origem_recurso_model import Base as OrigemRecursoBase
from src.models.bigquery.origem_model import Base as OrigemBase
from src.models.bigquery.destino_model import Base as DestinoBase
from src.models.bigquery.arquivo_model import Base as ArquivoBase


bases = [UserBase, ControleBase, MaterialBase, TipoBase, TipoUnidadeBase, AdministracaoBase, ApresentFarmaceuticaBase, OrigemRecursoBase, OrigemBase, DestinoBase, ArquivoBase]

AUTHDATASET = {
    'mocktoken': 'Pharmawatch'
}

load_dotenv()


class BigQueryAuthService:
    def __init__(self, user: UsuarioBase = None):
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
    

    def delete_all_tables(self, project_id: str = None, dataset: str = None):
        try:
            project_id = project_id if project_id != None else os.getenv("GCP_PROJECT_ID")
            connection_string = f"bigquery://{project_id}/{dataset}"
            ic(f'Connection string: {connection_string}')
            client = bigquery.Client.from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
            engine = create_engine(connection_string)
            Session = sessionmaker(bind=engine)
            session = Session()
        except Exception as e:
            ic(e)
            raise Exception("Error creating SQLAlchemy session")
        
        try:
            for base in bases:
                ic(f'Trying to delete {base} table')
                base.metadata.drop_all(engine)
                ic(f'{base} table deleted successfully!')
        except Exception as e:
            ic(e)
            ic(f'{base} table does not exist or could not be deleted')

        ic("Tables deleted successfully!")

        session.close()
    
    def create_all_tables(self, project_id: str = None, dataset: str = None):
        try:
            project_id = project_id if project_id != None else os.getenv("GCP_PROJECT_ID")
            connection_string = f"bigquery://{project_id}/{dataset}"
            ic(connection_string)
            client = bigquery.Client.from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
            engine = create_engine(connection_string)
            Session = sessionmaker(bind=engine)
            session = Session()
        except Exception as e:
            ic(e)
            raise Exception("Error creating SQLAlchemy session")


        for base in bases:
            try:
                ic(f'Trying to create {base} table')
                base.metadata.create_all(engine)
                ic(f'{base} table created successfully!')
            except Exception as e:
                ic(e)
                ic(f'{base} table already exists')
        
        ic("Tables created successfully!")

        session.close()