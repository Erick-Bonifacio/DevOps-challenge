from models.spreadsheet import Spreadsheet
import pandas as pd
import unicodedata
import re
import time
import sys
import os

# Apaga uma coluna do Dataframe
def drop_column(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    return df.drop(columns=[col for col in columns if col in df.columns], errors='ignore')

# Renomeia coluna do Dataframe
def rename_column(df: pd.DataFrame, rename_map: dict) -> pd.DataFrame:
    return df.rename(columns=rename_map)

# Padronizao nome das colunas no Dataframe
def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    def normalize(col):
        col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8')
        col = col.lower()
        col = re.sub(r'\s+', '_', col)
        col = re.sub(r'[^\w]', '', col)
        return col
    df.columns = [normalize(col) for col in df.columns]
    return df

# Converte uma lista de colunas inteiras pro padrão Real Brasileiro
def standardize_column_to_real_currency(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    def format_real(value):
        try:
            value = float(value)
            return f"R$ {value:,.2f}".replace('.', '#').replace(',', ',').replace('#', '.')
        except:
            return value
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(format_real)
    return df

# Converte string no formato 'R$ 1.234,56' ou 'R$ -1.234,56' para float.
def parse_brl_to_float(value: str) -> float:
    try:
        value = re.sub(r'[^\d,-]', '', value)  # remove tudo exceto números, vírgula e traço
        value = value.replace('.', '').replace(',', '')
        value = value.zfill(3)  # garante ao menos 3 dígitos para evitar erro de index
        value = value[:-2] + '.' + value[-2:]
        return float(value)
    except:
        return 0.0

# Converte float no formato '1234.56' ou '-1234.56' para string com mask Real.
def format_float_to_brl(value: float) -> str:
    return f"R$ {value:,.2f}".replace('.', '#').replace(',', ',').replace('#', '.')

# Soma os valores em R$ por linha e adiciona a coluna 'custo_total', já formatada.
def add_total_cost_column(df: pd.DataFrame) -> pd.DataFrame:
    currency_pattern = r'^R\$ ?-?\d'
    currency_columns = [
        col for col in df.columns
        if df[col].astype(str).head(5).str.match(currency_pattern).all()
    ]

    df["custo_total_agregado"] = df[currency_columns].applymap(parse_brl_to_float).sum(axis=1)
    df["custo_total_agregado"] = df["custo_total_agregado"].apply(format_float_to_brl)

    return df

# Soma de uma coluna inteira
def sum_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).sum()

# Média de uma coluna inteira
def avg_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).mean()

# Agrupa dados baseado em dados de uma coluna
def group_by(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df.groupby(column_name)

# Retorna o valor mínimo da coluna
def min_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).min()

# Retorna o valor maximo da coluna
def max_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).max()

# Ordena coluna (descrescente/crescente)
def sort_column(df: pd.DataFrame, column_name: str, ascending=True):
    df = df.copy()
    return df.sort_values(by=column_name, ascending=ascending)

# Média agrupada
def group_avg(df: pd.DataFrame, column_name_group: str, column_name_avg: str):
    df = df.copy()
    df[column_name_avg] = df[column_name_avg].apply(parse_brl_to_float)
    return df.groupby(column_name_group)[column_name_avg].mean().reset_index()

# Soma agrupada
def group_sum(df: pd.DataFrame, column_name_group: str, column_name_sum: str):
    df = df.copy()
    df[column_name_sum] = df[column_name_sum].apply(parse_brl_to_float)
    return df.groupby(column_name_group)[column_name_sum].sum().reset_index()

# Mediana de uma coluna
def median_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).median()

# Desvio padrão de uma coluna
def std_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).std()

# Variância padrão de uma coluna
def var_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).var()

# Descreve uma coluna (num de linhas, ...)
def describe_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].describe()

# Mediana por grupos
def group_median(df: pd.DataFrame, column_name_group: str, column_name_median: str):
    df = df.copy()
    df[column_name_median] = df[column_name_median].apply(parse_brl_to_float)
    return df.groupby(column_name_group)[column_name_median].median().reset_index()

# Desvio padrao por grupos
def group_std(df: pd.DataFrame, column_name_group: str, column_name_std: str):
    df = df.copy()
    df[column_name_std] = df[column_name_std].apply(parse_brl_to_float)
    return df.groupby(column_name_group)[column_name_std].std().reset_index()

#retorna o numero de linhas
def lines_count(df: pd.DataFrame) -> int:
    return len(df)

# Printar em partes - fluidez
def stream_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print() 

def load_files_dataframes(dir):
    reader = Spreadsheet()
    files = {}
    for filename in os.listdir(dir):
        if filename.endswith('.xlsx'):
            full_path = os.path.join(dir, filename)
            df = reader.load(full_path).get_df()
            files[filename] = df 
    
    if files:
        return files
    return False

def save_result(file_content :pd.DataFrame):
    reader = Spreadsheet()
    return reader.save(file_content)
