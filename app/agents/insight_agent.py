from crewai import Agent
from app.utils.llm_config import (
    azure_llm
)

insight_agent = Agent(
    role="Financial Insights Expert",

    goal="""
    Generate strategic business insights
    from retrieved financial data.
    """,

    backstory="""
    You provide investment-oriented
    and strategic financial analysis.
    """,
    llm=azure_llm,
    verbose=True
    
)