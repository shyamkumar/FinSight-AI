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
        temperature=0.2,
        max_tokens=1200
    )

    content = response.choices[0].message.content

    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    return json.loads(content)

def generate_ai_score(analysis):

    try:

        growth_score = 80
        risk_score = 65

        recommendation = "Moderate Buy"

        return {

            "growth_score": f"{growth_score}/100",

            "risk_score": f"{risk_score}/100",

            "investment_rating": recommendation
        }

    except Exception as e:

        print(e)

        return {

            "growth_score": "N/A",

            "risk_score": "N/A",

            "investment_rating": "N/A"
        }

def generate_multi_agent_analysis(analysis):

    bullish_points = analysis.get(
        "bullish_factors",
        []
    )

    bearish_points = analysis.get(
        "bearish_factors",
        []
    )

    bull_agent = f"""
Bullish Investment Thesis:

- {' - '.join(bullish_points)}

Overall outlook remains optimistic based on growth and profitability trends.
"""

    bear_agent = f"""
Bearish Investment Thesis:

- {' - '.join(bearish_points)}

Valuation and market risks require caution.
"""

    risk_agent = """
Key Risks:

- Macroeconomic slowdown
- Regulatory pressure
- AI competition
- Supply chain exposure
"""

    research_agent = """
Strategic Research Insights:

- AI demand remains strong
- Cloud infrastructure growth accelerating
- Long-term semiconductor demand expanding
"""

    return {

        "bull_agent": bull_agent,

        "bear_agent": bear_agent,

        "risk_agent": risk_agent,

        "research_agent": research_agent
    }