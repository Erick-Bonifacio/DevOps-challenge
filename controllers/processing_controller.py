# controllers/processing_controller.py

from models.spreadsheet import Spreadsheet
from agents.decisionAgent import DecisionAgent
from agents.transformAgent import TransformAgent
from agents.mergeAgent import MergeAgent
import os
import json
from dotenv import load_dotenv
from colorama import init, Fore, Style
init(autoreset=True)

load_dotenv()

class ProcessingController:
    def run(self):
        input_dir = os.getenv('INPUT_DIR')
        decisor = DecisionAgent()
        transform_agent = TransformAgent()
        files = {}
        processed_files = {}

        print(Fore.YELLOW + '[1/4] Lendo arquivos...')
        reader = Spreadsheet()
        for filename in os.listdir(input_dir):
            if filename.endswith('.xlsx'):
                full_path = os.path.join(input_dir, filename)
                df = reader.load(full_path).get_csv_string()
                files[filename] = df
        print(Fore.GREEN + '[1/4] OK')

        print(Fore.YELLOW + '[2/4] Gerando fluxo de transformação...')
        flow_string = decisor.generate_flow(files)

        #{'Beneficio 1 - Unimed.xlsx': ['standardize', 'lean'], 'Beneficio 2 - Gympass.xlsx': ['standardize', 'lean'], 'Dados Colaboradores.xlsx': ['standardize']}
        json_flow = json.loads(flow_string)
        print(Fore.GREEN + '[2/4] OK')
        

        print(Fore.YELLOW + '[3/4] Padronizando e enxugando dados...')
        for filename, steps in json_flow.items():
            csv = files[filename]

            if "standardize" in steps:
                csv = transform_agent.call_llm_standardize(csv, filename) 
            if "lean" in steps:
                csv = transform_agent.call_llm_lean(csv, filename)

            processed_files[filename] = csv
        print(Fore.GREEN + '[3/4] OK')

        print(Fore.YELLOW + '[4/4] Ligando planilhas e calculando rateio...')
        merge_agent = MergeAgent()
        csv_string = merge_agent.call_llm(processed_files)
        print(Fore.GREEN + '[4/4] OK')

        return reader.transform_and_save(csv_string)
    
    
