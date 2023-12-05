from icecream import ic
from datetime import datetime
import pandas as pd

from src.models.upload_data import MateriaisBrutosData
from src.models.bigquery.tipo_model import TipoBase, TipoTable
from src.models.bigquery.tipo_unidade_model import TipoUnidadeBase, TipoUnidadeTable
from src.models.bigquery.administracao_model import AdministracaoBase, AdministracaoTable
from src.models.bigquery.apresent_farmaceutica_model import ApresentFarmaceuticaBase, ApresentFarmaceuticaTable
from src.models.bigquery.origem_recurso_model import OrigemRecursoBase, OrigemRecursoTable
from src.models.bigquery.material_model import Material, MaterialTable
from src.models.bigquery.origem_model import OrigemBase, OrigemTable
from src.models.bigquery.destino_model import DestinoBase, DestinoTable
from src.models.bigquery.arquivo_model import Arquivo, ArquivoTable
from src.models.bigquery.controle_model import Controle, ControleTable
from src.pipes.pre_upload_material_pipe import PreUploadMedicinePipe as Pipe
from src.services.bigquery_upload_service import BigQueryDataUploadService


class UploadHandler:
    def __init__(self, upload_service: BigQueryDataUploadService):
        self.upload_service = upload_service


    def upload_material_data(self, df: pd.DataFrame):
        ic("Uploading data...")
        upload_data = Pipe().run(df)
        # show first 5 columns of the dataframe
        #ic(upload_data.loc[0:5, ['Material', 'Material Base', 'Material Comp', 'Metod Administracao']])

        upload_data = upload_data.to_dict('records')

        current_date = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")
        random_hash = hash(str(upload_data)) % 10000000000
        ic(random_hash)

        for data in upload_data:
            ic(data)
            data = MateriaisBrutosData(
                descr_material= str(data['Material']),
                descr_material_base = str(data['Material Base']),
                descr_material_comp = str(data['Material Comp']),
                descr_metod_administracao = str(data['Metod Administracao']),
                descr_apresent_farmaceutica = str(data['Apresentação farmacêutica']),
                descr_administracao = str(data['Via de administração']),
                descr_tipo = str(data['Tipo']),
                descr_origem_recurso = str(data['Origem do recurso']),
                descr_tipo_unidade = str(data['Unidade']),
                quantidade_unidade = float(data['Quantidade']),
                valor_unidade = float(data['Valor unitário (R$)']),
                valor_total = float(data['Valor total (R$)']),
                mes_ref = int(data['Mês']),
                ano_ref = int(data['Ano']),
                descr_origem = str(data['Local']),
                descr_destino = str(data['Destino'])
            )
            try:
                tipo_data = TipoBase(
                    descr_tipo = data.descr_tipo
                ).model_dump()

                tipo_unidade_data = TipoUnidadeBase(
                    descr_tipo_unidade = data.descr_tipo_unidade
                ).model_dump()

                administracao_data = AdministracaoBase(
                    descr_administracao = data.descr_administracao
                ).model_dump()

                apresent_farmaceutica_data = ApresentFarmaceuticaBase(
                    descr_apresent_farmaceutica = data.descr_apresent_farmaceutica
                ).model_dump()

                origem_recurso_data = OrigemRecursoBase(
                    descr_origem_recurso = data.descr_origem_recurso
                ).model_dump()

                material_data = Material(
                    descr_material = data.descr_material,
                    descr_material_base = data.descr_material_base,
                    descr_material_comp = data.descr_material_comp,
                    descr_metod_administracao = data.descr_metod_administracao,
                    id_tipo = self.upload_service.insert_and_get_id(TipoTable, "tipo", tipo_data),
                    id_tipo_unidade = self.upload_service.insert_and_get_id(TipoUnidadeTable, "tipo_unidade", tipo_unidade_data),
                    id_administracao = self.upload_service.insert_and_get_id(AdministracaoTable, "administracao", administracao_data),
                    id_apresent_farmaceutica = self.upload_service.insert_and_get_id(ApresentFarmaceuticaTable, "apresent_farmaceutica", apresent_farmaceutica_data),
                    id_origem_recurso = self.upload_service.insert_and_get_id(OrigemRecursoTable, "origem_recurso", origem_recurso_data),
                ).model_dump()

                origem_data = OrigemBase(
                    descr_origem = data.descr_origem
                ).model_dump()

                destino_data = DestinoBase(
                    descr_destino = data.descr_destino
                ).model_dump()

                arquivo_data = Arquivo(
                    token_usuario = self.upload_service.bq_auth_service.user.token,
                    mes_ref = data.mes_ref,
                    ano_ref = data.ano_ref,
                    data_upload = current_date,
                    descr_arquivo = f'{random_hash}-{self.upload_service.bq_auth_service.user.descr_email}-{current_date}.csv'
                ).model_dump()

                controle_data = Controle(
                    id_material = self.upload_service.insert_and_get_id(MaterialTable, "material", material_data),
                    quantidade_unidade = data.quantidade_unidade,
                    valor_unidade = data.valor_unidade,
                    valor_total = data.valor_total,
                    mes_ref = data.mes_ref,
                    ano_ref = data.ano_ref,
                    uid_mes_ano = f'{data.mes_ref}-{data.ano_ref}',
                    id_origem = self.upload_service.insert_and_get_id(OrigemTable, "origem", origem_data),
                    id_destino = self.upload_service.insert_and_get_id(DestinoTable, "destino", destino_data),
                    id_arquivo = self.upload_service.insert_and_get_id(ArquivoTable, "arquivo", arquivo_data)
                ).model_dump()

                self.upload_service.insert_into_table(ControleTable, "controle", controle_data)
            except Exception as e:
                ic(f"Error uploading data: {e}")
                raise e