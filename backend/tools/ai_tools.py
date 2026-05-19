import os
import json

from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def generate_stock_analysis(
    stock_data,
    news_data,
    financial_ratios
):

    prompt = f"""
    You are a senior financial analyst.

    Analyze the following stock information.

    Stock Information:
    {stock_data}
    
    Financial Ratios:
    {financial_ratios}

    Latest News:
    {news_data}

    Return ONLY valid JSON.

   Format:

   {{
     "company_overview": "",
     "bullish_factors": [],
     "bearish_factors": [],
     "risk_analysis": "",
     "long_term_outlook": "",
     "recommendation": ""
  }}
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

    content = response.choices[0].message.content

    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    return json.loads(content)