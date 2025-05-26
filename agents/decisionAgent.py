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
        self.description_prompt = os.getenv('DECISOR_PROMPT')

    def generate_flow(self, df_dict: dict) -> pd.DataFrame:
        csv_sections = []

        for filename, string in df_dict.items():
            csv_sections.append(f"### {filename}\n{string}")

        dados_consolidados = "\n\n".join(csv_sections)
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
            temperature=0.2
            # max_completion_tokens=32768,
            # top_p=0.95,
            # stream=False,
            # reasoning_format="hidden"
        )
        return completion.choices[0].message.content.replace('`', '').replace('json', '')    
    # def generate_result_structure()