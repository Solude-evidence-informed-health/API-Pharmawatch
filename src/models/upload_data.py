from pydantic import BaseModel


class MateriaisBrutosData(BaseModel):
    descr_material: str
    descr_material_base: str
    descr_material_comp: str
    descr_metod_administracao: str
    descr_apresent_farmaceutica: str
    descr_administracao: str
    descr_tipo: str
    descr_origem_recurso: str
    descr_tipo_unidade: str
    quantidade_unidade: float
    valor_unidade: float
    valor_total: float
    mes_ref: int
    ano_ref: int
    descr_origem: str
    descr_destino: str