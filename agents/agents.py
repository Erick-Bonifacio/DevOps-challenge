from groq import Groq # type: ignore
import os
import pandas as pd
import json
import requests # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

def call_llm(df_dict :dict):

    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    csv_sections = []

    for filename, df in df_dict.items():
        csv_str = df.to_csv(index=False)
        csv_sections.append(f"### {filename}\n{csv_str}")

    dados_consolidados = "\n\n".join(csv_sections)

    prompt = os.getenv('DESCRIPTION_PROMPT').replace('dados_consolidados', dados_consolidados)

    completion = client.chat.completions.create(
        model=os.getenv('REASONING_MODEL'),
        messages=[
            {
                "role": "system",
                "content": os.getenv('SYSTEM_PROMPT')
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.6,
        max_completion_tokens=75000,
        top_p=0.95,
        stream=False,
        reasoning_format="hidden"
    )

    return completion.choices[0].message.content