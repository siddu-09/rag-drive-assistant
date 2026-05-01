"""
LLM generator – sends context + query to an LLM and returns the answer.
"""

from typing import List
import openai

from app.config.settings import settings


class LLMGenerator:
    """Generates answers using an OpenAI-compatible LLM."""

    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.LLM_MODEL

    def generate(self, query: str, context_chunks: List[str]) -> str:
        """
        Generate an answer given a query and relevant context chunks.

        Args:
            query: The user question.
            context_chunks: List of relevant text chunks from the retriever.

        Returns:
            The generated answer string.
        """
        context = "\n\n---\n\n".join(context_chunks)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Answer the user's question "
                    "based ONLY on the provided context. If the context does not "
                    "contain enough information, say so."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}",
            },
        ]

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            max_tokens=1024,
        )

        return response.choices[0].message.content.strip()
