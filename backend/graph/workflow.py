from typing import TypedDict

from langgraph.graph import StateGraph, END

from backend.agents.research_agent import research_stock
from backend.agents.report_agent import generate_report


class StockState(TypedDict):

    ticker: str

    stock_info: dict

    news: list

    financial_ratios: dict

    analysis: dict


def research_node(state):

    data = research_stock(state["ticker"])

    return {
        "stock_info": data["stock_info"],
        "news": data["news"],
        "financial_ratios": data["financial_ratios"]
    }


def report_node(state):

    analysis = generate_report(
        state["stock_info"],
        state["news"],
        state["financial_ratios"]
    )

    return {
        "analysis": analysis
    }


graph = StateGraph(StockState)

graph.add_node("research_agent", research_node)

graph.add_node("report_agent", report_node)

graph.set_entry_point("research_agent")

graph.add_edge("research_agent", "report_agent")

graph.add_edge("report_agent", END)

financial_workflow = graph.compile()