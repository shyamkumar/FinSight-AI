from crewai import Agent

from app.utils.llm_config import (
    azure_llm
)
summary_agent = Agent(
    role="Financial Summary Specialist",

    goal="""
    Generate concise and professional
    financial summaries.
    """,

    backstory="""
    You are skilled at summarizing
    long financial reports into
    executive-level insights.
    """,
    llm=azure_llm,
    verbose=True
    
)