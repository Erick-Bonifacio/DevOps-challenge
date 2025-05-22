import pandas as pd
from dotenv import load_dotenv
import os
from io import StringIO

load_dotenv()
class Spreadsheet:
    def __init__(self):
        self.df = None

    # Carrega o DF
    def load(self, path):
        try:
            self.df = pd.read_excel(path)
            return self
        except Exception as e:
            raise ValueError(f"Erro ao carregar planilha {path}: {e}")
        
    def data_clean(self):
        self.df = self.df

    # Retorna o dataframe lido
    def get_df(self):
        if self.df is None:
            raise RuntimeError("Planilha ainda não carregada.")
        return self.df
    
    
    def transform_and_save(self, csv_string :str):
        csv_string = csv_string.replace('`', '')
        csv_string = csv_string.replace('csv', '')
        output_dir = os.getenv('OUTPUT_DIR')
        os.makedirs(output_dir, exist_ok=True)
        put_file = os.path.join(output_dir, 'resultado.xlsx')
        
        try:
            # Converter string CSV para DataFrame
            df = pd.read_csv(StringIO(csv_string))
            
            # Salvar DataFrame em arquivo Excel
            with pd.ExcelWriter(put_file, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, index=False)
                
        except Exception as e:
            raise Exception(f'Erro ao transformar e salvar resultado: {e}')
        
        return True, put_file


