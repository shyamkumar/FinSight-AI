from fastapi import FastAPI
from backend.tools.finance_tools import get_stock_price

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
def stock_price(ticker: str):

    result = get_stock_price(ticker)

    return result