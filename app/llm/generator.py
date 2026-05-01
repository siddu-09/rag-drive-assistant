import os
from typing import Iterable, Optional

from dotenv import load_dotenv
from groq import Groq

from app.config.settings import GROQ_API_KEY, GROQ_MODEL

load_dotenv()


class LLMGenerator:
    def __init__(self, model_name: str = GROQ_MODEL):
        self.model_name = model_name
        self.api_key = os.getenv("GROQ_API_KEY", GROQ_API_KEY)
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def generate(self, query: str, context_chunks: Optional[Iterable[str]] = None):
        if not self.client:
            return "GROQ_API_KEY is not set. Add it as a Hugging Face secret to enable answers."

        if isinstance(context_chunks, str):
            context_text = context_chunks
        else:
            context_text = "\n\n".join(list(context_chunks or []))

        prompt = f"""
You are an AI assistant.

Answer ONLY using the context below.
If the answer is not present, say "I don't know".

Context:
{context_text}

Question:
{query}
"""

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        return response.choices[0].message.content


def generate_answer(context, query):
    return LLMGenerator().generate(query, context)