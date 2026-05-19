from fastapi import FastAPI

from backend.agents.research_agent import research_stock

from backend.agents.report_agent import generate_report
from backend.graph.workflow import financial_workflow
from fastapi import UploadFile, File

from backend.rag.pdf_extractor import extract_pdf_text
from backend.rag.chunking import chunk_text

app = FastAPI()


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

    file_location = f"uploaded_{file.filename}"

    with open(file_location, "wb") as f:

        f.write(await file.read())
    extracted_text = extract_pdf_text(file_location)
    chunks = chunk_text(extracted_text)

    return {
    "filename": file.filename,
    "text_length": len(extracted_text),
    "total_chunks": len(chunks),
    "first_chunk_preview": chunks[0]
}