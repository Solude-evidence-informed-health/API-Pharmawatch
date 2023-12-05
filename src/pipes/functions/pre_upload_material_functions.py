import pandas as pd
from typing import List

def adjust_number_floating_pointers(df: pd.DataFrame, columns: List[str]):
    for column in columns:
        df[column] = df[column].apply(lambda x: x.replace(".", ""))
        df[column] = df[column].apply(lambda x: x.replace(",", "."))
        df[column] = df[column].astype(float)
    return df

def group_by_material(df: pd.DataFrame):
    df = df.groupby(["Material", "Unidade", "Mês", "Ano", "Local", "Destino", "Valor unitário (R$)"]).agg({"Quantidade": "sum", "Valor total (R$)": "sum"}).reset_index()
    return df

def split_material_components(df: pd.DataFrame):
    """ 
    df has a column named 'material', i need to break it in tree columns: material_base, material_comp and metod_administracao
    material_base is the first part until the first "+" or before any set of numbers that does not finish with "%"
    material_comp is the optional part after the first "+" and before any set of numbers that does not finish with "%"
    metod_administracao is the final part from any set of numbers that does not finish with "%" until the end of the string
    """
    df['Material Base'] = df['Material'].str.extract(r'^(.*?)(?:\+|\d+[^%])')
    df['Material Comp'] = df['Material'].str.extract(r'(?<=\+)(.*?)(?:\d+[^%])')
    df['Metod Administracao'] = df['Material'].str.extract(r'(\d+[^%]*$)')
    df[['Material Base', 'Material Comp', 'Metod Administracao']] = df[['Material Base', 'Material Comp', 'Metod Administracao']].apply(lambda x: x.str.strip())
    return df

def clean_material_components(df: pd.DataFrame, list_words_to_remove: List[str]):
    for word in list_words_to_remove:
        df['Material Base'] = df['Material Base'].str.replace(word, '')
        df['Material Comp'] = df['Material Comp'].str.replace(word, '')
    return df

def enrich_dataframe(df: pd.DataFrame, **enriched_data):
    for column, df_enriched in enriched_data["enriched_data"].items():
        if "Subtipo" in df_enriched.columns:
            df_enriched = df_enriched.drop(columns=['Subtipo'])
        if "Antibiótico (Sim/Não)" in df_enriched.columns:
            df_enriched = df_enriched.drop(columns=['Antibiótico (Sim/Não)'])
        df = df.merge(df_enriched, on=column, how='left')
    return df