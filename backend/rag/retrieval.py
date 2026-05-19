import os

from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential

from azure.search.documents import SearchClient

from azure.search.documents.models import VectorizedQuery

from openai import AzureOpenAI

load_dotenv()


# Azure OpenAI
openai_client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

embedding_model = os.getenv(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
)


# Azure AI Search
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(
        os.getenv("AZURE_SEARCH_KEY")
    )
)


def retrieve_relevant_chunks(query: str):

    embedding_response = openai_client.embeddings.create(
        input=query,
        model=embedding_model
    )

    query_vector = embedding_response.data[0].embedding

    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=3,
        fields="embedding"
    )

    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query]
    )

    retrieved_chunks = []

    for result in results:

        retrieved_chunks.append(result["content"])

    return retrieved_chunks