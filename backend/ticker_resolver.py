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

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(

            url,

            params=params,

            headers=headers,

            timeout=10
        )

        if response.status_code != 200:

            return company_name.upper()

        data = response.json()

        quotes = data.get(
            "quotes",
            []
        )

        if quotes:

            return quotes[0].get(
                "symbol",
                company_name.upper()
            )

        return company_name.upper()

    except Exception as e:

        print(e)

        return company_name.upper()