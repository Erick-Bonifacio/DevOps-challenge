import pandas as pd
import unicodedata
import re
import time
import sys

def drop_column(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    return df.drop(columns=[col for col in columns if col in df.columns], errors='ignore')

def rename_column(df: pd.DataFrame, rename_map: dict) -> pd.DataFrame:
    return df.rename(columns=rename_map)

def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    def normalize(col):
        col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8')
        col = col.lower()
        col = re.sub(r'\s+', '_', col)
        col = re.sub(r'[^\w]', '', col)
        return col
    df.columns = [normalize(col) for col in df.columns]
    return df

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


def parse_brl_to_float(value: str) -> float:
    """
    Converte string no formato 'R$ 1.234,56' ou 'R$ -1.234,56' para float.
    """
    try:
        value = re.sub(r'[^\d,-]', '', value)  # remove tudo exceto números, vírgula e traço
        value = value.replace('.', '').replace(',', '')
        value = value.zfill(3)  # garante ao menos 3 dígitos para evitar erro de index
        value = value[:-2] + '.' + value[-2:]
        return float(value)
    except:
        return 0.0

def format_float_to_brl(value: float) -> str:
    """
    Converte float para formato 'R$ x.xxx,xx', mantendo sinal negativo.
    """
    return f"R$ {value:,.2f}".replace('.', '#').replace(',', ',').replace('#', '.')

def add_total_cost_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Soma os valores em R$ por linha e adiciona a coluna 'custo_total', já formatada.
    """
    currency_pattern = r'^R\$ ?-?\d'
    currency_columns = [
        col for col in df.columns
        if df[col].astype(str).head(5).str.match(currency_pattern).all()
    ]

    df["custo_total"] = df[currency_columns].applymap(parse_brl_to_float).sum(axis=1)
    df["custo_total"] = df["custo_total"].apply(format_float_to_brl)

    return df

def sum_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).sum()

def avg_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).mean()

def group_by(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df.groupby(column_name)

def min_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).min()

def max_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).max()

def sort_column(df: pd.DataFrame, column_name: str, ascending=True):
    df = df.copy()
    return df.sort_values(by=column_name, ascending=ascending)

def group_avg(df: pd.DataFrame, column_name_group: str, column_name_avg: str):
    df = df.copy()
    df[column_name_avg] = df[column_name_avg].apply(parse_brl_to_float)
    return df.groupby(column_name_group)[column_name_avg].mean().reset_index()

def group_sum(df: pd.DataFrame, column_name_group: str, column_name_sum: str):
    df = df.copy()
    df[column_name_sum] = df[column_name_sum].apply(parse_brl_to_float)
    return df.groupby(column_name_group)[column_name_sum].sum().reset_index()

def median_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).median()

def std_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).std()

def var_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].apply(parse_brl_to_float).var()

def describe_column(df: pd.DataFrame, column_name: str):
    df = df.copy()
    return df[column_name].describe()

def group_median(df: pd.DataFrame, column_name_group: str, column_name_median: str):
    df = df.copy()
    df[column_name_median] = df[column_name_median].apply(parse_brl_to_float)
    return df.groupby(column_name_group)[column_name_median].median().reset_index()

def group_std(df: pd.DataFrame, column_name_group: str, column_name_std: str):
    df = df.copy()
    df[column_name_std] = df[column_name_std].apply(parse_brl_to_float)
    return df.groupby(column_name_group)[column_name_std].std().reset_index()

def stream_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print() 