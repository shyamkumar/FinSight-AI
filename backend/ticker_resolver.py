import yfinance as yf


def resolve_ticker(company_name: str):

    try:

        search = yf.Search(
            company_name
        )

        quotes = search.quotes

        print("SEARCH RESULTS:")
        print(quotes)

        if quotes and len(quotes) > 0:

            return quotes[0].get(
                "symbol",
                company_name.upper()
            )

        return company_name.upper()

    except Exception as e:

        print("TICKER RESOLUTION ERROR:")
        print(e)

        return company_name.upper()