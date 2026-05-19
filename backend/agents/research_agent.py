from backend.tools.finance_tools import (
    get_stock_info,
    get_stock_news,
    get_financial_ratios
)


def research_stock(ticker: str):

    stock_info = get_stock_info(ticker)

    news = get_stock_news(ticker)

    ratios = get_financial_ratios(ticker)

    return {
        "stock_info": stock_info,
        "news": news,
        "financial_ratios": ratios
    }