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
def get_stock_news(ticker: str):

    stock = yf.Ticker(ticker)

    news = stock.news

    latest_news = []

    for article in news[:5]:

        latest_news.append({
            "title": article.get("title"),
            "publisher": article.get("publisher"),
            "link": article.get("link")
        })

    return latest_news