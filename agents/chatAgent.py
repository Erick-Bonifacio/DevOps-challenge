from groq import Groq  # type: ignore
import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

class ChatSession:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = os.getenv('ANALYTICAL_MODEL')
        self.system_prompt = os.getenv('CHAT_ROLE')
        self.initial_prompt = os.getenv('CHAT_PROMPT')
        
        # Histórico da conversa
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.initial_prompt},
        ]

    def ask(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=0.2,
                reasoning_format='hidden'
            )
        except Exception as e:
            return f"Erro ao chamar modelo: {str(e)}"

        # Resposta do modelo
        reply = completion.choices[0].message.content.strip()
        self.messages.append({"role": "assistant", "content": reply})
        return reply.replace('`', '').replace('json', '').replace('\n', '').replace("'", '"') # Tratamento para garantir que resposta seja uma string JSON

    def reset(self):
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.initial_prompt}
        ]
