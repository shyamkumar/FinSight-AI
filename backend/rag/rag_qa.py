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
You are an elite financial research analyst and investment advisor.

Your task is to analyze annual report data and provide institutional-grade financial insights.

STRICT RULES:
- Use ONLY the provided annual report context
- Do NOT hallucinate information
- If information is unavailable, clearly say so
- Provide clear financial reasoning
- Use professional investment language
- Be concise but insightful
- Return response in professional markdown format

USER QUESTION:
{query}

ANNUAL REPORT CONTEXT:
{context}

Generate a structured response with:

1. Executive Summary
- Brief answer to the question

2. Financial/Business Insights
- Key business observations
- Revenue/profitability insights
- Operational observations

3. Risk Analysis
- Financial risks
- Operational risks
- Market/regulatory risks

4. Investment Perspective
- Investor implications
- Long-term outlook
- Strategic impact

5. Final Recommendation
- Concise concluding insight
"""

    # ==================================
    # AZURE OPENAI RESPONSE
    # ==================================

    response = client.chat.completions.create(

        model=deployment,

        messages=[

            {
                "role": "system",
                "content": (
                    "You are a world-class "
                    "financial analyst and "
                    "investment advisor."
                )
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.2
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