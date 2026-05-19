import os

from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def generate_stock_analysis(stock_data, news_data):

    prompt = f"""
    You are a senior financial analyst.

    Analyze the following stock data and latest news.

    Stock Information:
    {stock_data}

    Latest News:
    {news_data}

    Provide response in this format:

    ## Company Overview

    ## Bullish Factors

    ## Bearish Factors

    ## Risk Analysis

    ## Long-Term Outlook

    ## Investment Recommendation
    Choose one:
    - Buy
    - Hold
    - Sell

    Explain reasoning clearly.
    """

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content