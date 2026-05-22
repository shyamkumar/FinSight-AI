import yfinance as yf

from backend.utils.ticker_resolver import (
    resolve_ticker
)

# ======================================
# STOCK INFO
# ======================================

def get_stock_info(ticker: str):

    resolved_ticker = resolve_ticker(
        ticker
    )

    print(
        "Resolved Ticker:",
        resolved_ticker
    )

    stock = yf.Ticker(
        resolved_ticker
    )

    info = stock.info

    current_price = info.get(
        "currentPrice"
    )

    return {

        "ticker": resolved_ticker,

        "company": info.get(
            "longName"
        ),

        "sector": info.get(
            "sector"
        ),

        "industry": info.get(
            "industry"
        ),

        "market_cap": info.get(
            "marketCap"
        ),

        "current_price": current_price
    }

# ======================================
# STOCK NEWS
# ======================================

def get_stock_news(ticker: str):

    resolved_ticker = resolve_ticker(
        ticker
    )

    stock = yf.Ticker(
        resolved_ticker
    )

    news = stock.news

    latest_news = []

    for article in news[:5]:

        latest_news.append({

            "title": article.get(
                "title"
            ),

            "publisher": article.get(
                "publisher"
            ),

            "link": article.get(
                "link"
            )
        })

    return latest_news

# ======================================
# FINANCIAL RATIOS
# ======================================

def get_financial_ratios(ticker):

    try:

        resolved_ticker = resolve_ticker(
            ticker
        )

        stock = yf.Ticker(
            resolved_ticker
        )

        info = stock.info

        print("YFINANCE INFO:")
        print(info)

        return {

            "ticker": resolved_ticker,

            "marketCap": info.get(
                "marketCap",
                0
            ),

            "trailingPE": info.get(
                "trailingPE",
                0
            ),

            "profitMargins": info.get(
                "profitMargins",
                0
            ),

            "revenueGrowth": info.get(
                "revenueGrowth",
                0
            ),

            "currentRatio": info.get(
                "currentRatio",
                0
            ),

            "debtToEquity": info.get(
                "debtToEquity",
                0
            ),

            "returnOnEquity": info.get(
                "returnOnEquity",
                0
            )
        }

    except Exception as e:

        print(
            "FINANCIAL RATIOS ERROR:"
        )

        print(e)

        return {}

# ======================================
# STOCK CHART DATA
# ======================================

def get_stock_chart_data(ticker):

    try:

        resolved_ticker = resolve_ticker(
            ticker
        )

        stock = yf.Ticker(
            resolved_ticker
        )

        history = stock.history(
            period="6mo"
        )

        # ==============================
        # HANDLE EMPTY DATAFRAME
        # ==============================

        if history.empty:

            print(
                "No stock history found."
            )

            return []

        history.reset_index(
            inplace=True
        )

        # ==============================
        # CONVERT DATE TO STRING
        # ==============================

        history["Date"] = history[
            "Date"
        ].astype(str)

        return history.to_dict(
            orient="records"
        )

    except Exception as e:

        print(
            "STOCK CHART ERROR:"
        )

        print(e)

        return []