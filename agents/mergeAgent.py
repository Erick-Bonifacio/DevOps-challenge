from groq import Groq  # type: ignore
import os
import pandas as pd
import json
import requests  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()

class MergeAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = os.getenv('ANALYTICAL_MODEL')
        self.system_prompt = os.getenv('MERGE_AGENT_ROLE')
        self.description_prompt = os.getenv('MERGE_AGENT_PROMPT')

    def call_llm(self, processed_files) -> str:
        input_data = "\n\n".join(
            f"# Arquivo: {filename}\n{csv_content}"
            for filename, csv_content in processed_files.items()
        )

        prompt = self.description_prompt.replace("csv_strings", input_data)
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        )

        return completion.choices[0].message.content

