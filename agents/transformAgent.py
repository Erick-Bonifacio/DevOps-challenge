from groq import Groq  # type: ignore
import os
import pandas as pd
import json
import requests  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()

class TransformAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = os.getenv('TRANSFORMING_MODEL')
        self.role = os.getenv('TRANSFORMER_ROLE')
        self.standardize_prompt = os.getenv('TRANSFORMER_PROMPT_STANDARDIZE')
        self.lean_prompt = os.getenv('TRANSFORMER_PROMPT_LEAN')

    def call_llm_standardize(self, csv_string, filename) ->str:

        # csv_string = df.to_csv(index=False)
        prompt = self.standardize_prompt.replace('csv_content', csv_string)
        prompt = prompt.replace('filename', filename)

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
            max_completion_tokens=75000
            # top_p=0.95,
            # stream=False,
            # reasoning_format="hidden"
        )

        return completion.choices[0].message.content

    def call_llm_lean(self, csv_string, filename) ->str:

        prompt = self.lean_prompt.replace('csv_content', csv_string)
        prompt = prompt.replace('filename', filename)
        
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
            temperature=0.6,
            max_completion_tokens=75000
            # top_p=0.95,
            # stream=False,
            # reasoning_format="hidden"
        )

        return completion.choices[0].message.content
