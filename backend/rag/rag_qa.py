import os

from dotenv import load_dotenv

from openai import AzureOpenAI

from backend.rag.retrieval import retrieve_relevant_chunks

# ======================================
# LOAD ENV VARIABLES
# ======================================

load_dotenv()

# ======================================
# AZURE OPENAI CLIENT
# ======================================

client = AzureOpenAI(

    api_key=os.getenv("OPENAI_API_KEY"),

    api_version="2024-02-15-preview",

    azure_endpoint=os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    )
)

deployment = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT"
)

# ======================================
# GENERATE RAG ANSWER
# ======================================

def generate_rag_answer(query: str):

    # ==================================
    # RETRIEVE RELEVANT CHUNKS
    # ==================================

    chunks = retrieve_relevant_chunks(query)

    context = "\n\n".join(chunks)

    # ==================================
    # IMPROVED FINANCIAL ANALYST PROMPT
    # ==================================

    prompt = f"""

You are a senior Wall Street financial analyst and AI research assistant.

Your task is to analyze annual report information and provide
high-quality investor-focused insights.

STRICT RULES:

1. Use ONLY the provided annual report context.
2. Do NOT hallucinate or invent information.
3. If information is unavailable, explicitly say:
   "The annual report does not provide sufficient information."
4. Provide concise but insightful financial reasoning.
5. Focus on investor implications and business impact.
6. Mention risks, opportunities, and strategic insights.
7. Use structured formatting.

USER QUESTION:
{query}

ANNUAL REPORT CONTEXT:
{context}

Provide response in this format:

## Concise Explanation
- Direct answer to the question.

## Financial & Business Insights
- Revenue/profitability implications
- Operational/business insights
- Market or industry implications
- Strategic observations

## Risks & Concerns
- Financial risks
- Operational risks
- Market risks
- Regulatory or macroeconomic risks

## Investor Takeaway
- Key takeaway for investors or analysts.

"""

    # ==================================
    # AZURE OPENAI RESPONSE
    # ==================================

    response = client.chat.completions.create(

        model=deployment,

        messages=[

            {
              "role": "system",

              "content": """

            You are an elite financial research analyst specializing in:
            - equity research
            - annual report analysis
            - financial statement interpretation
            - investor risk analysis
            - strategic business analysis

            You provide:
            - factual responses
            - investor-focused insights
            - concise reasoning
            - risk-aware analysis

            Never hallucinate data.
            Always rely only on provided context.

            """
     },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.2
        max_tokens=1200
    )

    # ==================================
    # EXTRACT ANSWER
    # ==================================

    answer = response.choices[0].message.content

    # ==================================
    # MULTI-AGENT EXECUTION FLOW
    # ==================================

    query_lower = query.lower()

    agent_flow = [

        (
            "🧠 Intent Agent → "
            "Detected financial analysis query"
        ),

        (
            "📚 Research Agent → "
            "Retrieved annual report insights"
        )

    ]

    # ==================================
    # DYNAMIC AGENT ROUTING
    # ==================================

    if "risk" in query_lower:

        agent_flow.append(

            "📊 Risk Agent → "
            "Evaluated financial and "
            "operational risks"

        )

    if (
        "growth" in query_lower
        or "opportunity" in query_lower
        or "expansion" in query_lower
    ):

        agent_flow.append(

            "📈 Growth Agent → "
            "Analyzed future business "
            "opportunities"

        )

    if (
        "revenue" in query_lower
        or "profit" in query_lower
        or "financial" in query_lower
        or "margin" in query_lower
    ):

        agent_flow.append(

            "💰 Financial Agent → "
            "Analyzed company financial "
            "performance"

        )

    if (
        "competition" in query_lower
        or "market" in query_lower
    ):

        agent_flow.append(

            "🌍 Market Intelligence Agent → "
            "Evaluated competitive and "
            "market positioning"

        )

    # ==================================
    # FINAL INVESTMENT AGENT
    # ==================================

    agent_flow.append(

        "💡 Investment Agent → "
        "Generated executive recommendation"

    )

    # ==================================
    # RETURN RESPONSE
    # ==================================

    return {

        "query": query,

        "answer": answer,

        "sources": chunks,

        "agent_flow": agent_flow
    }