from app.utils.azure_openai import (
    client
)

from app.config.settings import (
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT
)


def generate_embedding(text):

    response = client.embeddings.create(
        input=text,
        model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT
    )

    return response.data[
        0
    ].embedding