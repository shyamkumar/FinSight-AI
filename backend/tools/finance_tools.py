import yfinance as yf


def get_stock_price(ticker: str):

    stock = yf.Ticker(ticker)

    data = stock.history(period="1d")

    latest_price = data["Close"].iloc[-1]

    return {
        "ticker": ticker.upper(),
        "price": round(latest_price, 2)
    }