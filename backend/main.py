from fastapi import FastAPI

from backend.agents.research_agent import research_stock

from backend.agents.report_agent import generate_report
from backend.graph.workflow import financial_workflow
from fastapi import UploadFile, File

from backend.rag.pdf_extractor import extract_pdf_text
from backend.rag.chunking import chunk_text
from backend.rag.embeddings import create_embeddings
from backend.rag.azure_search import create_search_index
from backend.rag.azure_search import upload_documents
from backend.rag.retrieval import retrieve_relevant_chunks
from backend.rag.rag_qa import generate_rag_answer
from backend.tools.finance_tools import (
    get_stock_chart_data
)
from pydantic import BaseModel

from backend.tools.finance_tools import (
    get_stock_info,
    get_financial_ratios
)

from backend.tools.ai_tools import (
    generate_stock_analysis
)
from backend.tools.blob_tools import (
    upload_pdf_to_blob
)

class StockRequest(BaseModel):
    ticker: str

app = FastAPI()


@app.post("/analyze")
def analyze_stock(request: StockRequest):

    stock_data = get_stock_info(request.ticker)

    ratios = get_financial_ratios(request.ticker)

    analysis = generate_stock_analysis(
        request.ticker,
        stock_data,
        ratios
    )

    return {
        "ticker": request.ticker,
        "analysis": analysis
    }

@app.get("/")
def home():

    return {
        "message": "Backend Running Successfully"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/stock/{ticker}")
def stock_info(ticker: str):

    result = get_stock_info(ticker)

    return result

@app.get("/news/{ticker}")
def stock_news(ticker: str):

    result = get_stock_news(ticker)

    return result

@app.get("/analyze/{ticker}")
def analyze_stock(ticker: str):

    result = financial_workflow.invoke({
        "ticker": ticker
    })

    return {
        "ticker": ticker,
        "analysis": result["analysis"]
    }

@app.get("/ratios/{ticker}")
def financial_ratios(ticker: str):

    result = get_financial_ratios(ticker)

    return result

@app.post("/upload-report")
async def upload_report(file: UploadFile = File(...)):

    # ======================================
    # SAVE FILE LOCALLY TEMPORARILY
    # ======================================

    file_location = f"uploaded_{file.filename}"

    file_content = await file.read()

    with open(file_location, "wb") as f:

        f.write(file_content)

    # ======================================
    # UPLOAD TO AZURE BLOB STORAGE
    # ======================================

    blob_url = upload_pdf_to_blob(
        file.filename,
        file_content
    )

    # ======================================
    # EXTRACT PDF TEXT
    # ======================================

    extracted_text = extract_pdf_text(
        file_location
    )

    # ======================================
    # CHUNKING
    # ======================================

    chunks = chunk_text(
        extracted_text
    )

    # ======================================
    # CREATE EMBEDDINGS
    # ======================================

    embeddings = create_embeddings(
        chunks[:50]
    )

    # ======================================
    # UPLOAD TO AZURE AI SEARCH
    # ======================================

    upload_documents(
        embeddings
    )

    # ======================================
    # RESPONSE
    # ======================================

    return {

        "filename": file.filename,

        "blob_url": blob_url,

        "text_length": len(extracted_text),

        "total_chunks": len(chunks),

        "embeddings_created": len(embeddings),

        "uploaded_to_azure_search": True,

        "uploaded_to_blob_storage": True,

        "first_chunk_preview": chunks[0]
    }

@app.get("/create-index")
def create_index():

    result = create_search_index()

    return {
        "message": result
    }
@app.get("/rag-search")
def rag_search(query: str):

    chunks = retrieve_relevant_chunks(query)

    return {
        "query": query,
        "retrieved_chunks": chunks
    }

@app.get("/rag-qa")
def rag_qa(query: str):

    result = generate_rag_answer(query)

    return result

@app.get("/stock-chart/{ticker}")
def stock_chart(ticker: str):

    data = get_stock_chart_data(ticker)

    return data