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

        # Azure OpenAI Config
        self.embedding_model = AzureOpenAIEmbeddings(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        )

        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            temperature=0.3,
        )

        self.vectorstore = None

    # -----------------------------
    # Extract text from PDF
    # -----------------------------
    def extract_text_from_pdf(self, pdf_path):

        text = ""

        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        return text

    # -----------------------------
    # Create chunks
    # -----------------------------
    def create_chunks(self, text):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200
        )

        chunks = splitter.split_text(text)

        return chunks

    # -----------------------------
    # Build Vector Store
    # -----------------------------
    def build_vector_store(self, chunks):

        self.vectorstore = FAISS.from_texts(
            texts=chunks,
            embedding=self.embedding_model
        )

    # -----------------------------
    # Ingest PDF
    # -----------------------------
    def ingest_pdf(self, pdf_path):

        print("Extracting PDF text...")

        text = self.extract_text_from_pdf(pdf_path)

        print("Chunking text...")

        chunks = self.create_chunks(text)

        print("Generating embeddings...")

        self.build_vector_store(chunks)

        print("PDF ingestion completed.")

    # -----------------------------
    # Ask Questions
    # -----------------------------
    def ask_question(self, question):

        if self.vectorstore is None:
            return "Please upload and process a PDF first."

        docs = self.vectorstore.similarity_search(
            question,
            k=4
        )

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
You are an expert Financial Research AI Assistant.

Use the financial report context below to answer the user's question professionally.

Financial Context:
{context}

Question:
{question}

Provide:
- detailed analysis
- financial insights
- risks
- growth opportunities
- professional explanation
"""

        response = self.llm.invoke(
            [HumanMessage(content=prompt)]
        )

        return response.content