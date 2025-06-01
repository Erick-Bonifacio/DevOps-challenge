from agents.chatAgent import ChatSession
from tools.tools import (
    sum_column,
    avg_column,
    group_by,
    min_column,
    max_column,
    sort_column,
    group_avg,
    group_sum,
    median_column,
    std_column,
    var_column,
    describe_column,
    group_median,
    group_std,
    stream_print,
    load_files_dataframes,
    lines_count
)
import os
import json
from dotenv import load_dotenv # type: ignore
from colorama import init, Fore, Style, Back
import pandas as pd
pd.set_option('display.max_rows', 10)

init(autoreset=True)
load_dotenv()
        
class DiscussingController:
    def run(self):
        output_dir = os.getenv('OUTPUT_DIR')
        chat_agent = ChatSession()
        files = load_files_dataframes(output_dir)

        if not files:
            print("Nenhum arquivo encontrado.")
            return

        stream_print("\n🤖 Olá, eu sou seu agente especializado em rateio de custos! Estou pronto para te ajudar com suas dúvidas. Digite sua pergunta ou 'sair' para sair.")

        # Loop de chamada e resposta (chat) até o usuario sair
        while True:
            filename = self.get_file_wanted(files)
            if not filename:
                break

            user_prompt = input("\nSua pergunta:\n> ").strip()
            if user_prompt.lower() in ['exit', 'sair']:
                break

            # chama a LLM para decidir tool
            user_prompt = f'DATA: ${filename}: ${files[filename].to_csv()} - USER PROMPT: {user_prompt}'
            tool = chat_agent.ask(user_prompt)

            # Match entre as tools disponíveis e a que será usada 
            try:
                tool = json.loads(tool)
                tool_function = tool['tool_name']
                result = self._apply_match_function(tool, tool_function, files, filename)

                # Result é falso quando o usuario não permite o envio massivo para a llm
                if isinstance(result, bool):
                    break

            except Exception as e:
                print(Back.RED + f"❌ Ocorreu um erro inesperado: {e}")
                print(Fore.RED + f"Uma possível causa é o agente se 'embaralhando' no seu retorno, por favor, reinicie o script e pergunte novamente ao agente")
                break

            # Existem dois tipos de resposta possíveis
            # Se retornou um dataframe, peço para a LLM explicar o resultado esperado
            # Se retornou um valor fixo, peço para a LLM explicar ele
            if type(result) == pd.DataFrame:
                chat_final_prompt = 'The tool that you recommended returned a dataframe that will be showed to user. Write the explanation for it based in your previous response. Now dont give me a json, but a objective explanation in portuguese'
                chat_final_response = chat_agent.ask(chat_final_prompt)
                stream_print("\n🤖 Resultado:\n" + chat_final_response)
                with pd.option_context('display.max_rows', None):
                    print("\nDataframe:\n", result)
            else:
                chat_final_prompt = 'The tool that you recommended returned: ' + str(result) + 'Write the explanation for it based in your previous response. Now dont give me a json, but a objective a explanation in portuguese - convert any currency value to brazilian Real format'
                chat_final_response = chat_agent.ask(chat_final_prompt)
                stream_print("\n🤖 Resultado:\n\n" + chat_final_response + '\n')
            
            chat_agent.reset()


    def _apply_match_function(self, tool :json, tool_function :str, files :dict, filename :str):
        if tool_function == 'sum_column':
            parameters = tool['parameters']
            result = sum_column(files[filename], parameters['column_name'])

        elif tool_function == 'avg_column':
            parameters = tool['parameters']
            result = avg_column(files[filename], parameters['column_name'])

        elif tool_function == 'group_by':
            parameters = tool['parameters']
            result = group_by(files[filename], parameters['column_name'])

        elif tool_function == 'min_column':
            parameters = tool['parameters']
            result = min_column(files[filename], parameters['column_name'])

        elif tool_function == 'max_column':
            parameters = tool['parameters']
            result = max_column(files[filename], parameters['column_name'])

        elif tool_function == 'sort_column':
            parameters = tool['parameters']
            result = sort_column(files[filename], parameters['column_name'], parameters.get('ascending', True))

        elif tool_function == 'group_avg':
            parameters = tool['parameters']
            result = group_avg(files[filename], parameters['column_name_group'], parameters['column_name_avg'])

        elif tool_function == 'group_sum':
            parameters = tool['parameters']
            result = group_sum(files[filename], parameters['column_name_group'], parameters['column_name_sum'])

        elif tool_function == 'median_column':
            parameters = tool['parameters']
            result = median_column(files[filename], parameters['column_name'])

        elif tool_function == 'std_column':
            parameters = tool['parameters']
            result = std_column(files[filename], parameters['column_name'])

        elif tool_function == 'var_column':
            parameters = tool['parameters']
            result = var_column(files[filename], parameters['column_name'])

        elif tool_function == 'describe_column':
            parameters = tool['parameters']
            result = describe_column(files[filename], parameters['column_name'])

        elif tool_function == 'group_median':
            parameters = tool['parameters']
            result = group_median(files[filename], parameters['column_name_group'], parameters['column_name_median'])

        elif tool_function == 'group_std':
            parameters = tool['parameters']
            result = group_std(files[filename], parameters['column_name_group'], parameters['column_name_std'])

        elif tool_function == 'lines_count':
            result = lines_count(files[filename])

        elif tool_function == 'insufficient_tools':
            confirmation = self.ask_confirmation()
            if confirmation != '1':
                return False
            result = f'Once dont have tools enough, analyze the entire file and give a response for the user question. Do not tell that does not have tools enough. FILE:' + files[filename].to_csv()

        elif tool_function == 'show_dataframe':
            result = files[filename]

        else:
            result = 'Funcao invalida'
        
        return result

    def ask_confirmation(self):
        stream_print("\n⚠️ ATENÇÃO:")
        stream_print("Parece que não temos recursos locais suficientes para responder sua pergunta!")
        stream_print("Será necessário enviar os arquivos completos à LLM para análise direta.")
        stream_print("Isso eleva significativamente o custo por operação e a resposta pode estar imprecisa devido ao volume de dados.")
        stream_print("Dica: Se você fez mais de uma pergunta no mesmo prompt, pode tentar fazer uma por vez e ver se funciona :)")
        decision = 0
        while decision != '1' and decision != '2':
            decision = input("\nDeseja continuar?\n1 - Sim\n2 - Não\n> ")
        
        return decision
    
    def get_file_wanted(self, files: dict) -> str:
        stream_print("\nArquivos disponíveis para discussão:")
        filenames = list(files.keys())
        
        for idx, filename in enumerate(filenames, start=1):
            print(f"{idx}: {filename}")
        
        while True:
            try:
                choice = input(f'\nDigite o número correspondente ao arquivo (ou sair):\n> ')
                if choice.lower() in ['exit', 'sair']:
                    return False
                if 1 <= int(choice) <= len(filenames):
                    return filenames[int(choice) - 1]
                else:
                    print(f'\nNúmero inválido. Tente novamente.')
            except ValueError:
                print(f'\nEntrada inválida. Digite um número.')
