from app.rag.rag_pipeline import (
    FinancialRAG
)

from app.utils.pdf_generator import (
    generate_pdf_report
)

rag = FinancialRAG()

rag.ingest_pdf(
    "app/data/sample.pdf"
)

query = "What are the major risks mentioned?"

response = rag.ask(query)

print("\n")
print("AI RESPONSE:")
print(response)

generate_pdf_report(
    query=query,
    ai_response=response,
    output_path="financial_analysis_report.pdf"
)