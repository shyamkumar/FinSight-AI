from fastapi import FastAPI
from backend.tools.finance_tools import (
    get_stock_info,
    get_stock_news
)
from backend.tools.ai_tools import generate_stock_analysis
from backend.tools.finance_tools import (
    get_stock_info,
    get_stock_news,
    get_financial_ratios
)

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

    stock_data = get_stock_info(ticker)

    news_data = get_stock_news(ticker)

    financial_ratios = get_financial_ratios(ticker)

    analysis = generate_stock_analysis(
    stock_data,
    news_data,
    financial_ratios
    )

    return {
        "ticker": ticker,
        "analysis": analysis
    }

@app.get("/ratios/{ticker}")
def financial_ratios(ticker: str):

    result = get_financial_ratios(ticker)

    return result