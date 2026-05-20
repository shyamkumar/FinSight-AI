from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter


from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter


def generate_pdf_report(
    ticker,
    analysis,
    metrics,
    ai_scores,
    multi_agent
):

    print("PDF REPORT GENERATION STARTED")

    file_name = f"{ticker}_AI_Report.pdf"

    print("File name:", file_name)

    doc = SimpleDocTemplate(
        file_name,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    content = []

    # ======================================
    # TITLE
    # ======================================

    title = Paragraph(
        f"<b>{ticker} AI Investment Report</b>",
        styles["Title"]
    )

    content.append(title)

    content.append(
        Spacer(1, 20)
    )

    # ======================================
    # COMPANY OVERVIEW
    # ======================================

    overview = Paragraph(

        f"<b>Company Overview:</b><br/>{analysis.get('company_overview', '')}",

        styles["BodyText"]
    )

    content.append(overview)

    content.append(
        Spacer(1, 12)
    )

    # ======================================
    # METRICS
    # ======================================

    metrics_text = f'''
    <b>Financial Metrics</b><br/>
    Market Cap: {metrics.get("marketCap")}<br/>
    Trailing PE: {metrics.get("trailingPE")}<br/>
    Profit Margin: {metrics.get("profitMargins")}<br/>
    Revenue Growth: {metrics.get("revenueGrowth")}<br/>
    '''

    content.append(

        Paragraph(
            metrics_text,
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    # ======================================
    # AI SCORES
    # ======================================

    ai_text = f'''
    <b>AI Investment Signals</b><br/>
    AI Score: {ai_scores.get("ai_score")}<br/>
    Sentiment: {ai_scores.get("sentiment")}<br/>
    Risk Level: {ai_scores.get("risk_level")}<br/>
    Confidence: {ai_scores.get("confidence")}%<br/>
    '''

    content.append(

        Paragraph(
            ai_text,
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    # ======================================
    # RECOMMENDATION
    # ======================================

    recommendation = Paragraph(

        f"<b>Recommendation:</b><br/>{analysis.get('recommendation', '')}",

        styles["BodyText"]
    )

    content.append(recommendation)

    content.append(
        Spacer(1, 12)
    )

    # ======================================
    # MULTI AGENT
    # ======================================

    agent_text = f'''
    <b>Bull Agent:</b><br/>
    {multi_agent.get("bull_agent")}<br/><br/>

    <b>Bear Agent:</b><br/>
    {multi_agent.get("bear_agent")}<br/><br/>

    <b>Risk Agent:</b><br/>
    {multi_agent.get("risk_agent")}<br/><br/>

    <b>Research Agent:</b><br/>
    {multi_agent.get("research_agent")}
    '''

    content.append(

        Paragraph(
            agent_text,
            styles["BodyText"]
        )
    )

    # ======================================
    # BUILD PDF
    # ======================================

    doc.build(content)

    print("PDF SAVED SUCCESSFULLY")

    # ======================================
    # RETURN FILE NAME
    # ======================================

    return file_name