from app.rag.rag_pipeline import (
    FinancialRAG
)

rag = FinancialRAG()

rag.ingest_pdf(
    "app/data/sample.pdf"
)

response = rag.ask(
    "What are the major risks mentioned?"
)

print("\n")
print("AI RESPONSE:")
print(response)