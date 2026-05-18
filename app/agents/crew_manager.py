from crewai import Crew
from crewai import Task

from app.agents.financial_agent import (
    financial_agent
)

from app.agents.risk_agent import (
    risk_agent
)

from app.agents.summary_agent import (
    summary_agent
)

from app.agents.insight_agent import (
    insight_agent
)
from app.utils.llm_config import (
    azure_llm
)


class FinancialCrew:

    def run_analysis(
        self,
        context,
        query
    ):

        financial_task = Task(
            description=f"""
            Analyze the following
            financial context:

            {context}

            Query:
            {query}
            """,

            agent=financial_agent,

            expected_output="""
            Detailed financial analysis
            """
        )

        risk_task = Task(
            description=f"""
            Identify risks from:

            {context}
            """,

            agent=risk_agent,

            expected_output="""
            Financial and operational risks
            """
        )

        summary_task = Task(
            description=f"""
            Summarize this financial data:

            {context}
            """,

            agent=summary_agent,

            expected_output="""
            Concise executive summary
            """
        )

        insight_task = Task(
            description=f"""
            Generate strategic insights
            from:

            {context}
            """,

            agent=insight_agent,

            expected_output="""
            Strategic financial insights
            """
        )

        crew = Crew(
            agents=[
                financial_agent,
                risk_agent,
                summary_agent,
                insight_agent
            ],

            tasks=[
                financial_task,
                risk_task,
                summary_task,
                insight_task
            ],

            verbose=True
        )

        result = crew.kickoff()
        llm=azure_llm

        return result