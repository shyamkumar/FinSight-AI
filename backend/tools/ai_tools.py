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

def generate_ai_score(analysis):

    bullish = len(
        analysis.get("bullish_factors", [])
    )

    bearish = len(
        analysis.get("bearish_factors", [])
    )

    score = 50 + (bullish * 10) - (bearish * 5)

    score = max(0, min(score, 100))

    if score >= 75:
        sentiment = "Bullish"

    elif score >= 55:
        sentiment = "Neutral"

    else:
        sentiment = "Bearish"

    if score >= 80:
        risk = "Low"

    elif score >= 60:
        risk = "Medium"

    else:
        risk = "High"

    return {

        "ai_score": score,

        "sentiment": sentiment,

        "risk_level": risk,

        "confidence": min(
            95,
            60 + bullish * 5
        )
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