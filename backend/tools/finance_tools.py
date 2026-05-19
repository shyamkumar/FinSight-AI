import yfinance as yf


def get_stock_info(ticker: str):

    stock = yf.Ticker(ticker)

    info = stock.info

    current_price = info.get("currentPrice")

    return {
        "ticker": ticker.upper(),
        "company": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": info.get("marketCap"),
        "current_price": current_price
    }