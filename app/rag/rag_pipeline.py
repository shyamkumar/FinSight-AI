import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

import fitz  # PyMuPDF

load_dotenv()


class FinancialRAG:

    def __init__(self):

        # ============================================
        # Azure OpenAI Embeddings
        # ============================================

        self.embedding_model = AzureOpenAIEmbeddings(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=os.getenv(
                "AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
            ),
        )

        # ============================================
        # Azure OpenAI LLM
        # ============================================

        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=os.getenv(
                "AZURE_OPENAI_DEPLOYMENT"
            ),
            temperature=0.2,
        )

        self.vectorstore = None

    # ============================================
    # Extract Text From PDF
    # ============================================

    def extract_text_from_pdf(self, pdf_path):

        text = ""

        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        return text

    # ============================================
    # Create Text Chunks
    # ============================================

    def create_chunks(self, text):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200
        )

        chunks = splitter.split_text(text)

        return chunks

    # ============================================
    # Build Vector Store
    # ============================================

    def build_vector_store(self, chunks):

        self.vectorstore = FAISS.from_texts(
            texts=chunks,
            embedding=self.embedding_model
        )

    # ============================================
    # Ingest PDF
    # ============================================

    def ingest_pdf(self, pdf_path):

        print("Extracting PDF text...")

        text = self.extract_text_from_pdf(pdf_path)

        print("Chunking text...")

        chunks = self.create_chunks(text)

        print("Generating embeddings...")

        self.build_vector_store(chunks)

        print("PDF ingestion completed.")

    # ============================================
    # Ask Questions
    # ============================================

    def ask_question(self, question):

        if self.vectorstore is None:

            return (
                "Please upload and process a PDF first."
            )

        # ============================================
        # Retrieve Relevant Chunks
        # ============================================

        docs = self.vectorstore.similarity_search_with_score(
            question,
            k=4
        )

        context = ""

        sources = []

        for i, (doc, score) in enumerate(docs):

            context += f"\n\n{doc.page_content}"

            sources.append(
                f"Source Chunk {i+1} | "
                f"Similarity Score: {round(score, 2)}"
            )

        # ============================================
        # System Prompt
        # ============================================

        prompt = f"""
You are a senior Wall Street financial strategist and institutional equity research analyst.

Use the financial report context below to answer professionally.

Provide:
- executive-level analysis
- financial intelligence
- strategic reasoning
- investment perspective
- risks
- growth opportunities
- professional explanation

Use consulting-style language similar to:
- Bloomberg
- Goldman Sachs
- McKinsey

Financial Context:
{context}

Question:
{question}
"""

        # ============================================
        # Generate Response
        # ============================================

        response = self.llm.invoke(
            [HumanMessage(content=prompt)]
        )

        # ============================================
        # Final Response With Sources
        # ============================================

        final_response = f"""
{response.content}

---

## 📚 AI Source References

{chr(10).join(sources)}
"""

        return final_response