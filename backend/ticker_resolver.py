import requests


def resolve_ticker(company_name: str):

    try:

        url = (
            "https://query1.finance.yahoo.com"
            "/v1/finance/search"
        )

        params = {
            "q": company_name,
            "quotesCount": 1,
            "newsCount": 0
        }

        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        data = response.json()

        quotes = data.get(
            "quotes",
            []
        )

        if quotes:

            symbol = quotes[0].get(
                "symbol"
            )

            print(
                "Resolved Ticker:",
                symbol
            )

            return symbol

        return company_name.upper()

    except Exception as e:

        print(
            "Ticker Resolver Error:"
        )

        print(e)

        return company_name.upper()