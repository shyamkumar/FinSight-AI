import os

from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

embedding_model = os.getenv(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
)


def create_embeddings(chunks):

    embeddings = []

    for chunk in chunks:

        response = client.embeddings.create(
            input=chunk,
            model=embedding_model
        )

        vector = response.data[0].embedding

        embeddings.append({
            "text": chunk,
            "embedding": vector
        })

    return embeddings