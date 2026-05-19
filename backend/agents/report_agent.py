from backend.tools.ai_tools import generate_stock_analysis


def generate_report(
    stock_info,
    news,
    financial_ratios
):

    analysis = generate_stock_analysis(
        stock_info,
        news,
        financial_ratios
    )

    return analysis