import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class LLMService:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "groq").lower()

        if self.provider != "groq":
            raise ValueError(
                f"Unsupported LLM provider: {self.provider}"
            )

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.model = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b",
        )

        self.client = Groq(api_key=api_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0,
        )

        return response.choices[0].message.content or ""