import pandas as pd
from icecream import ic
from src.pipes.functions.pre_upload_material_functions import *


ENRICHED_MATERIAL_DATA = "src/pipes/data/enriched_material.csv"


class PreUploadMedicinePipe:
    def __init__(self):
        self.df_enriched_material = pd.read_csv(ENRICHED_MATERIAL_DATA, sep=",")
        #ic(self.df_enriched_material)

        self.enrich_data = {
            "Material": self.df_enriched_material
        }
        self.words_to_remove = [
            "POMADA",
        ]
        self.floating_pointers_to_adjust = [
            'Quantidade',
            'Valor unitário (R$)',
            'Valor total (R$)'
        ]


    def run(self, upload_data: pd.DataFrame):  
        ic("Running pre upload material data pipe...")
        df = upload_data.copy()
        df = adjust_number_floating_pointers(df, self.floating_pointers_to_adjust)
        df = group_by_material(df)
        df = split_material_components(df)
        df = clean_material_components(df, self.words_to_remove)
        df = enrich_dataframe(df, enriched_data=self.enrich_data)
        ic(df.info())
        return df