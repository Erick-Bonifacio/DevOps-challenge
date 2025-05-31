import pandas as pd
from dotenv import load_dotenv # type: ignore
import os
from io import StringIO
from datetime import datetime

load_dotenv()
class Spreadsheet:
    def __init__(self):
        self.df = None

    # Carrega o DF
    def load(self, path):
        try:
            self.df = pd.read_excel(path, index_col=False, engine='openpyxl')
            return self
        except Exception as e:
            raise ValueError(f"Erro ao carregar planilha {path}: {e}")

    # Retorna o dataframe lido
    def get_df(self):
        if self.df is None:
            raise RuntimeError("Planilha ainda não carregada.")
        return self.df
    
    
    def save(self, dataframe):
        output_dir = os.getenv('OUTPUT_DIR')
        os.makedirs(output_dir, exist_ok=True)
        filename = 'resultado_' + datetime.now().strftime('%y%m%d_%H%M%S') + '.xlsx'
        put_file = os.path.join(output_dir, filename)
        
        try:
            # Salvar df em excel
            with pd.ExcelWriter(put_file, engine='openpyxl', mode='w') as writer:
                dataframe.to_excel(writer, index=False)
                
        except Exception as e:
            raise Exception(f'Erro ao salvar resultado: {e}')
        
        return True, put_file


