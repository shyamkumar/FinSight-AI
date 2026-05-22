import yfinance as yf


def resolve_ticker(company_name: str):

    try:

        search = yf.Search(company_name)

        quotes = search.quotes

        if quotes:

            return quotes[0]["symbol"]

        return company_name.upper()

    except Exception:

        return company_name.upper()