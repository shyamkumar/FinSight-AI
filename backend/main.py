from fastapi import FastAPI

from backend.agents.research_agent import research_stock

from backend.agents.report_agent import generate_report

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

    research_data = research_stock(ticker)

    analysis = generate_report(
        research_data["stock_info"],
        research_data["news"],
        research_data["financial_ratios"]
    )

    return {
        "ticker": ticker,
        "analysis": analysis
    }

@app.get("/ratios/{ticker}")
def financial_ratios(ticker: str):

    result = get_financial_ratios(ticker)

    return result