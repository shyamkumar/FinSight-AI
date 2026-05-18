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

from app.agents.crew_manager import (
    FinancialCrew
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

        print(
            "Generating query embedding..."
        )

        query_embedding = (
            generate_embedding(query)
        )

        print(
            "Retrieving relevant chunks..."
        )

        retrieved_chunks = (
            self.vector_store.search(
                query_embedding
            )
        )

        context = "\n".join(
            retrieved_chunks
        )

        print(
            "Running multi-agent analysis..."
        )

        crew = FinancialCrew()

        result = crew.run_analysis(
            context,
            query
        )

        return result