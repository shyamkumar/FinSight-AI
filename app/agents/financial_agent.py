from crewai import Agent

from app.utils.llm_config import (
    azure_llm
)

financial_agent = Agent(
    role="Senior Financial Analyst",

    goal="""
    Analyze financial reports and
    provide detailed financial insights.
    """,

    backstory="""
    You are an experienced financial
    analyst with expertise in annual
    reports, balance sheets,
    revenue analysis, and market trends.
    """,

    llm=azure_llm,

    verbose=True
)