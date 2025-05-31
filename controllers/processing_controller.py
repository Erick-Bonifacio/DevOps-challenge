from models.spreadsheet import Spreadsheet
from agents.decisionAgent import DecisionAgent
from tools.tools import normalize_column_names, rename_column, drop_column, standardize_column_to_real_currency, add_total_cost_column
import os
import json
from dotenv import load_dotenv # type: ignore
from colorama import init, Fore, Style
from functools import reduce
import pandas as pd

init(autoreset=True)
load_dotenv()

class ProcessingController:
    def run(self):
        input_dir = os.getenv('INPUT_DIR')
        decisor = DecisionAgent()
        files = {}
        tools_to_apply = {}

        print(Fore.YELLOW + '[1/6] Lendo arquivos...')

        reader = Spreadsheet()
        for filename in os.listdir(input_dir):
            if filename.endswith('.xlsx'):
                full_path = os.path.join(input_dir, filename)
                df = reader.load(full_path).get_df()
                files[filename] = df
        
        if not files:
            print("Nenhum arquivo encontrado.")
            return False, ''

        print(Fore.GREEN + '[1/6] OK')
        print(Fore.YELLOW + '[2/6] Gerando fluxo de transformação...')

        for filename, df in files.items():
            tools_to_apply[filename] = decisor.generate_flow(f"### {filename}\n{df.head().to_csv()}")
        

        print(Fore.GREEN + '[2/6] OK')
        print(Fore.YELLOW + '[3/6] Executando transformações...')

        for filename, df in files.items():
            tools = (tools_to_apply[filename]).replace('\n', '').replace("'", '"') # tools aqui eh uma lista de jsons com cada tool e seus parametros
            tools = json.loads(tools)
            # print(filename)
            for tool in tools:
                if isinstance(tool, str):
                    tool = json.loads(tool)
                tool_function = tool['tool_name']

                if tool_function == 'normalize_column_names':
                    files[filename] = normalize_column_names(files[filename])

                elif tool_function == 'rename_column':
                    parameters = tool['parameters']
                    files[filename] = rename_column(files[filename], parameters['rename_map'])

                elif tool_function == 'standardize_column_to_real_currency':
                    parameters = tool['parameters']
                    files[filename] = standardize_column_to_real_currency(files[filename], parameters['columns'])

                elif tool_function == 'drop_column':
                    parameters = tool['parameters']
                    files[filename] = drop_column(files[filename], parameters['columns'])
                    
        print(Fore.GREEN + '[3/6] OK')

        print(Fore.YELLOW + '[4/6] Executando merge de dados...')

        result = reduce(lambda left, right: pd.merge(left, right, on=['cpf', 'nome'], how='outer'), files.values())

        df_merged = self._merge_columns(result, 'nome')

        print(Fore.GREEN + '[4/6] OK')

        print(Fore.YELLOW + '[5/6] Calculando rateio...')
        result = add_total_cost_column(df_merged)
        print(Fore.GREEN + '[5/6] OK')

        print(Fore.YELLOW + '[6/6] Salvando...')
        sucess, path = reader.save(result)
        print(Fore.GREEN + '[6/6] OK')

        return sucess, path
    
    def _merge_columns(self, df, col_base):
            col_x = f"{col_base}_x"
            col_y = f"{col_base}_y"
            if col_x in df.columns and col_y in df.columns:
                df[col_base] = df[col_x].combine_first(df[col_y])
                df.drop([col_x, col_y], axis=1, inplace=True)
            return df