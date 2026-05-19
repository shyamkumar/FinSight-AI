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
    Analyze this company for investment purposes.

    Stock Information:
    {stock_data}

    Latest News:
    {news_data}

    Provide:
    1. Company overview
    2. Growth opportunities
    3. Risks
    4. Overall investment insight
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