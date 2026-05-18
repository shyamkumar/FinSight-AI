from app.utils.pdf_loader import (
    extract_text_from_pdf
)

from app.rag.chunker import (
    chunk_text
)

from app.rag.embeddings import (
    generate_embedding
)

from app.rag.vector_store import (
    VectorStore
)

from app.utils.azure_openai import (
    client
)

from app.config.settings import (
    AZURE_OPENAI_DEPLOYMENT
)


class FinancialRAG:

    def __init__(self):

        self.vector_store = None

    def ingest_pdf(
        self,
        pdf_path
    ):

        print(
            "Extracting PDF text..."
        )

        text = extract_text_from_pdf(
            pdf_path
        )

        print(
            "Chunking text..."
        )

        chunks = chunk_text(text)

        print(
            "Generating embeddings..."
        )

        embeddings = []

        for chunk in chunks:

            embedding = (
                generate_embedding(
                    chunk
                )
            )

            embeddings.append(
                embedding
            )

        dimension = len(
            embeddings[0]
        )

        print(
            "Creating vector store..."
        )

        self.vector_store = (
            VectorStore(dimension)
        )

        self.vector_store.add_embeddings(
            embeddings,
            chunks
        )

        print(
            "PDF ingestion completed."
        )

    def ask(
        self,
        query
    ):

        query_embedding = (
            generate_embedding(query)
        )

        retrieved_chunks = (
            self.vector_store.search(
                query_embedding
            )
        )

        context = "\n".join(
            retrieved_chunks
        )

        prompt = f"""
        You are an expert financial analyst AI.

        Answer only from provided context.

        Context:
        {context}

        Question:
        {query}

        Give professional financial insights.
        """

        response = (
            client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )

        return response.choices[
            0
        ].message.content