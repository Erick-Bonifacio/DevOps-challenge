# ESSE ARQUIVO É RESPONSÁVEL POR CRIAR UMA INTERFACE COM O USUARIO 
# E MANEJAR AGENTS NA LEITURA, PROCESSAMENTO E VISUALIZAÇÃO DOS DADOS
 
from models.spreadsheet import Spreadsheet
from agents.transformAgent import call_llm
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    print('Iniciando leitura dos arquivos...')
    input_dir = os.getenv('INPUT_DIR')
    output_dir = os.getenv('OUTPUT_DIR')
    files =  {}
    reader = Spreadsheet()
    # Ler todos os arquivos .xslx no diretorio de entrada
    for filename in os.listdir(input_dir):
        if filename.endswith('.xlsx'):
            full_path = os.path.join(input_dir, filename)
            df = reader.load(full_path).get_df()
            files[filename] = df
    
    print(files)
    
    # Chamar agent para analisar e juntar arquivos
    print('Submetendo os dados para a LLM')
    result_df = call_llm(files)
    print(result_df)

    # Salvar no diretorio de saida
    saved, name = reader.transform_and_save(result_df)
    if saved:
        print("Arquivo ", name, " gerado com sucesso!")
    else:
        print('Erro ao salvar arquivo!')