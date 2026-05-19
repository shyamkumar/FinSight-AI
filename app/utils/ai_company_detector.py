import os

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage


class AICompanyDetector:

    def __init__(self):

        self.llm = AzureChatOpenAI(

            azure_endpoint=os.getenv(
                "AZURE_OPENAI_ENDPOINT"
            ),

            api_key=os.getenv(
                "AZURE_OPENAI_API_KEY"
            ),

            api_version=os.getenv(
                "AZURE_OPENAI_API_VERSION"
            ),

            azure_deployment=os.getenv(
                "AZURE_OPENAI_DEPLOYMENT"
            ),

            temperature=0
        )

    def detect(self, text):

        sample_text = text[:8000]

        prompt = f'''
You are an AI financial analyst.

From the uploaded annual report text below:

1. Identify the company name
2. Identify the stock ticker symbol

Return ONLY this format:

Company: <company name>
Ticker: <ticker>

Annual Report Text:
{sample_text}
'''

        response = self.llm.invoke(
            [HumanMessage(content=prompt)]
        )

        output = response.content

        company = "Unknown"

        ticker = "TSLA"

        lines = output.splitlines()

        for line in lines:

            if "Company:" in line:

                company = (
                    line.replace(
                        "Company:",
                        ""
                    ).strip()
                )

            if "Ticker:" in line:

                ticker = (
                    line.replace(
                        "Ticker:",
                        ""
                    ).strip()
                )

        return {

            "company": company,

            "ticker": ticker
        }