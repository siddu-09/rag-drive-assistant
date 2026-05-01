"""
Query service – orchestrates the full query pipeline:
  question → embed → retrieve → generate answer via LLM
"""

from typing import Dict

from app.retrieval.retriever import Retriever
from app.llm.generator import LLMGenerator


class QueryService:
    """Full query pipeline from user question to LLM-generated answer."""

    def __init__(self):
        self.retriever = Retriever()
        self.generator = LLMGenerator()

    async def query(self, question: str) -> Dict:
        """
        Run the full query pipeline.

        Args:
            question: The user's natural-language question.

        Returns:
            Dict with 'answer' and 'sources'.
        """
        # 1. Load the persisted vector store
        self.retriever.load_store()

        # 2. Retrieve relevant chunks
        results = self.retriever.retrieve(question)
        context_chunks = [text for text, _ in results]
        sources = list(set(text[:80] + "..." for text, _ in results))

        # 3. Generate answer using LLM
        answer = self.generator.generate(question, context_chunks)

        return {"answer": answer, "sources": sources}
