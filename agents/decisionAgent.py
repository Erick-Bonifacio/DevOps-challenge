import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class DecisionAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = os.getenv('ANALYTICAL_MODEL')
        self.role = os.getenv('DECISOR_ROLE')
        with open(os.getenv('DECISOR_PROMPT_PATH'), 'r', encoding='utf-8') as f:
            self.description_prompt = f.read()
        with open(os.getenv('DECISOR_CHECK_PROMPT_PATH'), 'r', encoding='utf-8') as f:
            self.check_prompt = f.read()

    def generate_flow(self, dados_consolidados: str) -> pd.DataFrame:

        # Primeira chamada
        json_inicial = self._call_llm(dados_consolidados)
        # Chamada de conferência - mitiga erros 
        json_final = self._check_json(json_inicial, dados_consolidados)

        return json_final.replace('`', '').replace('json', '')

    def _call_llm(self, dados_consolidados: str):
        prompt = self.description_prompt.replace('dados_consolidados', dados_consolidados)

        # Enviar dataframes ao agent para definir o flow de tratamento de dados a ser seguido
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.role
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            reasoning_format='hidden'
        )
        return completion.choices[0].message.content.replace('`', '').replace('json', '')    
    
    def _check_json(self, json, dados_consolidados):
        prompt = self.check_prompt.replace('dados_consolidados', dados_consolidados)
        prompt = prompt.replace('json_to_check', json)

        # Enviar dataframes ao agent para checar o flow de tratamento
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.role
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            reasoning_format='hidden'
        )
        return completion.choices[0].message.content.replace('`', '').replace('json', '')    