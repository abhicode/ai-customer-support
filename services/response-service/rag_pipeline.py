from typing import Optional, List, Dict
import httpx
from openai import OpenAI
import os

class RAGPipeline:
    def __init__(self, top_k: int = 3, llm_model: str = "gpt-4o-mini"):
        self.top_k = top_k
        self.client = OpenAI()
        self.llm_model = llm_model

    async def retrieve(self, query: str) -> List[str]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://kb-service:8000/search",
                json={"query": query, "top_k": self.top_k},
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("docs", [])

    async def generate(self, query: str, intent: Optional[str] = None, context: Optional[Dict] = {}) -> str:
        """Generate response using retrieved context + LLM."""
        # Step 1: Retrieve
        retrieved_docs = await self.retrieve(query)

        # Step 2: Build prompt
        context_str = "\n".join(retrieved_docs) if retrieved_docs else "No relevant context found."
        intent_str = f"(Intent: {intent})" if intent else ""
        prompt = f"""
        You are an AI customer support assistant. 
        Context documents:
        {context_str}

        User query: {query}
        User intent: {intent_str}
        User conversation context: {context}

        Answer the query concisely and helpfully using the context.
        """

        # Step 3: Generate via LLM
        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": "You are a helpful support assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=300,
        )

        return response.choices[0].message.content.strip()


# single instance for import
rag_pipeline = RAGPipeline()