import os

from dotenv import load_dotenv

from openai import AzureOpenAI

from backend.rag.retrieval import retrieve_relevant_chunks

load_dotenv()


client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def generate_rag_answer(query: str):

    chunks = retrieve_relevant_chunks(query)

    context = "\n\n".join(chunks)

    prompt = f"""
You are a financial research assistant.

Answer the user's question ONLY using the provided annual report context.

If information is not available, say so clearly.

Question:
{query}

Annual Report Context:
{context}

Provide:
1. concise explanation
2. financial/business insights
3. risks if applicable
"""

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": "You are an expert financial analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    answer = response.choices[0].message.content

    return {
        "query": query,
        "answer": answer,
        "sources": chunks
    }