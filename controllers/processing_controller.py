from agents.decisionAgent import DecisionAgent
from tools.tools import normalize_column_names, rename_column, drop_column, standardize_column_to_real_currency, add_total_cost_column, load_files_dataframes, save_result, sort_column
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
        tools_to_apply = {}

        print(Fore.YELLOW + '[1/6] Lendo arquivos...')

        files = load_files_dataframes(input_dir)
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
            tools = (tools_to_apply[filename]).replace('\n', '').replace("'", '"') 
            tools = json.loads(tools)
            for tool in tools:
                if isinstance(tool, str):
                    tool = json.loads(tool)
                tool_function = tool['tool_name']

                files[filename] = self._apply_match_function(tool, tool_function, files, filename)

                
                    
        print(Fore.GREEN + '[3/6] OK')

        print(Fore.YELLOW + '[4/6] Executando merge de dados...')

        result = reduce(lambda left, right: pd.merge(left, right, on=['cpf', 'nome'], how='outer'), files.values())

        # colapsar a coluna nome em uma só
        df_merged = self._merge_columns(result, 'nome')

        print(Fore.GREEN + '[4/6] OK')

        print(Fore.YELLOW + '[5/6] Calculando rateio...')
        result = add_total_cost_column(df_merged)
        result = sort_column(result, 'nome')
        print(Fore.GREEN + '[5/6] OK')

        print(Fore.YELLOW + '[6/6] Salvando...')
        sucess, path = save_result(result)
        print(Fore.GREEN + '[6/6] OK')

        return sucess, path
    
    def _apply_match_function(self, tool, tool_function, files, filename):
        if tool_function == 'normalize_column_names':
            result = normalize_column_names(files[filename])

        elif tool_function == 'rename_column':
            parameters = tool['parameters']
            result = rename_column(files[filename], parameters['rename_map'])

        elif tool_function == 'standardize_column_to_real_currency':
            parameters = tool['parameters']
            result = standardize_column_to_real_currency(files[filename], parameters['columns'])

        elif tool_function == 'drop_column':
            parameters = tool['parameters']
            result = drop_column(files[filename], parameters['columns'])
        
        else:
            result = files[filename]
        
        return result

    def _merge_columns(self, df, col_base):
            col_x = f"{col_base}_x"
            col_y = f"{col_base}_y"
            if col_x in df.columns and col_y in df.columns:
                df[col_base] = df[col_x].combine_first(df[col_y])
                df.drop([col_x, col_y], axis=1, inplace=True)
            return df