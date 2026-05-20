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

def get_financial_ratios(ticker):

    try:

        stock = yf.Ticker(ticker)

        info = stock.info

        print("YFINANCE INFO:")
        print(info)

        return {

            "marketCap": info.get("marketCap", 0),

            "trailingPE": info.get("trailingPE", 0),

            "profitMargins": info.get("profitMargins", 0),

            "revenueGrowth": info.get("revenueGrowth", 0),

            "currentRatio": info.get("currentRatio", 0),

            "debtToEquity": info.get("debtToEquity", 0),

            "returnOnEquity": info.get("returnOnEquity", 0)
        }

    except Exception as e:

        print("FINANCIAL RATIOS ERROR:")
        print(e)

        return {}
def get_stock_chart_data(ticker):

    stock = yf.Ticker(ticker)

    history = stock.history(period="6mo")

    history.reset_index(inplace=True)

    return history.to_dict(orient="records")