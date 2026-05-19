import os

from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential

from azure.search.documents.indexes import SearchIndexClient

from azure.search.documents.indexes.models import (
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)

load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")

key = os.getenv("AZURE_SEARCH_KEY")

index_name = os.getenv("AZURE_SEARCH_INDEX")

credential = AzureKeyCredential(key)

client = SearchIndexClient(
    endpoint=endpoint,
    credential=credential
)


def create_search_index():

    fields = [

        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True
        ),

        SearchField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True
        ),

        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(
                SearchFieldDataType.Single
            ),
            searchable=True,
            vector_search_dimensions=3072,
            vector_search_profile_name="my-vector-profile"
        )
    ]

    vector_search = VectorSearch(

        algorithms=[
            HnswAlgorithmConfiguration(
                name="my-hnsw"
            )
        ],

        profiles=[
            VectorSearchProfile(
                name="my-vector-profile",
                algorithm_configuration_name="my-hnsw"
            )
        ]
    )

    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search
    )

    client.create_or_update_index(index)

    return "Index created successfully"
from azure.search.documents import SearchClient

search_client = SearchClient(
    endpoint=endpoint,
    index_name=index_name,
    credential=credential
)


def upload_documents(embeddings):

    documents = []

    for idx, item in enumerate(embeddings):

        documents.append({
            "id": str(idx),
            "content": item["text"],
            "embedding": item["embedding"]
        })

    result = search_client.upload_documents(documents)

    return result