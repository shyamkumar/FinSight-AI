from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import (
    letter
)

from datetime import datetime


def generate_pdf_report(
    query,
    ai_response,
    output_path="financial_report.pdf"
):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(
        "AI Financial Analysis Report",
        styles['Title']
    )

    story.append(title)

    story.append(
        Spacer(1, 20)
    )

    timestamp = Paragraph(
        f"Generated on: {datetime.now()}",
        styles['Normal']
    )

    story.append(timestamp)

    story.append(
        Spacer(1, 20)
    )

    query_heading = Paragraph(
        "User Query",
        styles['Heading2']
    )

    story.append(query_heading)

    query_text = Paragraph(
        query,
        styles['BodyText']
    )

    story.append(query_text)

    story.append(
        Spacer(1, 20)
    )

    response_heading = Paragraph(
        "Multi-Agent AI Analysis",
        styles['Heading2']
    )

    story.append(response_heading)

    response_text = Paragraph(
        str(ai_response).replace(
            "\n",
            "<br/>"
        ),
        styles['BodyText']
    )

    story.append(response_text)

    doc.build(story)

    print(
        f"PDF report saved: {output_path}"
    )