from crewai import Agent

from app.utils.llm_config import (
    azure_llm
)

risk_agent = Agent(
    role="Risk Analysis Expert",

    goal="""
    Identify operational, financial,
    cybersecurity, and market risks
    from financial documents.
    """,

    backstory="""
    You specialize in risk assessment,
    supply chain risks, credit risks,
    and business continuity analysis.
    """,

    llm=azure_llm,

    verbose=True
)