
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
BASE_API_URL = "https://finsight-ai-asgje4gjdjfydcfe.southindia-01.azurewebsites.net"

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = {}

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Financial Research Assistant",
    layout="wide"
)

# ==========================================
# LOAD CSS
# ==========================================

with open("frontend/styles.css") as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
    width=120
)

st.sidebar.title("FinSight AI")

st.sidebar.caption(
    "AI Financial Copilot"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Stock Analysis",
        "Annual Report QA"
    ]
)

st.sidebar.divider()

# ==========================================
# HERO SECTION
# ==========================================

st.title("📈 AI Financial Research Assistant")

st.markdown("""
# Upload Financial Report to Begin AI Analysis
### AI-powered Financial Research using Azure OpenAI + RAG
""")

# ==========================================
# FEATURE CARDS SECTION
# ==========================================

st.divider()

st.subheader("🚀 Available AI Features")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    <div style="
        background-color:#FFFFFF;
        padding:20px;
        border-radius:15px;
        box-shadow:0px 2px 8px rgba(0,0,0,0.08);
        margin-bottom:20px;
    ">

    <h3>📈 Financial Intelligence</h3>

    <ul>
        <li>Executive AI Analysis</li>
        <li>Market Sentiment Detection</li>
        <li>Risk Assessment</li>
        <li>Growth Opportunity Detection</li>
        <li>KPI Dashboard</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div style="
        background-color:#FFFFFF;
        padding:20px;
        border-radius:15px;
        box-shadow:0px 2px 8px rgba(0,0,0,0.08);
        margin-bottom:20px;
    ">

    <h3>🤖 Multi-Agent AI</h3>

    <ul>
        <li>Bull vs Bear Debate</li>
        <li>Boardroom Simulation</li>
        <li>What-If Scenario Analysis</li>
        <li>Investor PPT Generator</li>
        <li>Explainable AI Citations</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==========================================
# STOCK ANALYSIS PAGE
# ==========================================

if page == "Stock Analysis":

    ticker = st.text_input(
        "Enter Stock Ticker",
        placeholder="Example: NVDA"
    )

# ==========================================
# ANALYZE BUTTON
# ==========================================

if st.button("Analyze Stock"):

    with st.spinner("Analyzing stock..."):

        response = requests.post(
            f"{BASE_API_URL}/analyze",
            json={
                "ticker": ticker
            }
        )

        result = response.json()

        st.session_state.analysis_result = result

# ==========================================
# LOAD STORED ANALYSIS
# ==========================================

stored_result = st.session_state.get(
    "analysis_result",
    {}
)

if stored_result:

    analysis = stored_result.get(
        "analysis",
        {}
    )

    metrics = stored_result.get(
        "metrics",
        {}
    )

    ai_scores = stored_result.get(
        "ai_scores",
        {}
    )

    multi_agent = stored_result.get(
        "multi_agent",
        {}
    )

    st.success("Analysis Complete")

    # ==========================================
    # KPI DASHBOARD
    # ==========================================

    st.subheader("📊 Financial KPI Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Market Cap",
            f"${round(metrics.get('marketCap', 0)/1e12, 2)}T"
            if metrics.get("marketCap")
            else "N/A"
        )

    with col2:

        st.metric(
            "Trailing P/E",
            round(metrics.get("trailingPE", 0), 2)
            if metrics.get("trailingPE")
            else "N/A"
        )

    with col3:

        st.metric(
            "Profit Margin",
            f"{round(metrics.get('profitMargins', 0)*100, 2)}%"
            if metrics.get("profitMargins")
            else "N/A"
        )

    with col4:

        st.metric(
            "Revenue Growth",
            f"{round(metrics.get('revenueGrowth', 0)*100, 2)}%"
            if metrics.get("revenueGrowth")
            else "N/A"
        )

    st.divider()

    # ==========================================
    # AI SIGNALS
    # ==========================================

    st.subheader("🤖 AI Investment Signals")

    ai_score = ai_scores.get("ai_score", 0)

    fig_gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=ai_score,

            title={
                "text": "AI Investment Score"
            },

            gauge={

                "axis": {
                    "range": [0, 100]
                },

                "bar": {
                    "color": "darkblue"
                },

                "steps": [

                    {
                        "range": [0, 40],
                        "color": "#ffcccc"
                    },

                    {
                        "range": [40, 70],
                        "color": "#fff4cc"
                    },

                    {
                        "range": [70, 100],
                        "color": "#ccffcc"
                    }
                ]
            }
        )
    )

    st.plotly_chart(
        fig_gauge,
        use_container_width=True
    )

    # ==========================================
    # AI SIGNAL METRICS
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "AI Score",
            f"{ai_scores.get('ai_score', 0)}/100"
        )

    with col2:

        st.metric(
            "Market Sentiment",
            ai_scores.get("sentiment", "N/A")
        )

    with col3:

        st.metric(
            "Risk Level",
            ai_scores.get("risk_level", "N/A")
        )

    with col4:

        st.metric(
            "AI Confidence",
            f"{ai_scores.get('confidence', 0)}%"
        )

    st.divider()

    # ==========================================
    # COMPANY OVERVIEW
    # ==========================================

    st.subheader("🏢 Company Overview")

    st.write(
        analysis.get(
            "company_overview",
            "N/A"
        )
    )

    # ==========================================
    # BULLISH VS BEARISH
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📈 Bullish Factors")

        for item in analysis.get(
            "bullish_factors",
            []
        ):

            st.success(item)

    with col2:

        st.subheader("⚠️ Bearish Factors")

        for item in analysis.get(
            "bearish_factors",
            []
        ):

            st.error(item)

    st.divider()

    # ==========================================
    # RISK ANALYSIS
    # ==========================================

    st.subheader("📉 Risk Analysis")

    st.write(
        analysis.get(
            "risk_analysis",
            "N/A"
        )
    )

    # ==========================================
    # LONG TERM OUTLOOK
    # ==========================================

    st.subheader("🚀 Long-Term Outlook")

    st.write(
        analysis.get(
            "long_term_outlook",
            "N/A"
        )
    )

    # ==========================================
    # RECOMMENDATION
    # ==========================================

    st.subheader("💡 Recommendation")

    st.info(
        analysis.get(
            "recommendation",
            "N/A"
        )
    )

    st.divider()

    # ==========================================
    # MULTI AGENT AI WORKSPACE
    # ==========================================

    st.subheader("🤖 Multi-Agent AI Workspace")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🐂 Bull Agent")

        st.success(
            multi_agent.get(
                "bull_agent",
                "N/A"
            )
        )

    with col2:

        st.markdown("### 🐻 Bear Agent")

        st.error(
            multi_agent.get(
                "bear_agent",
                "N/A"
            )
        )

    col3, col4 = st.columns(2)

    with col3:

        st.markdown("### ⚠️ Risk Agent")

        st.warning(
            multi_agent.get(
                "risk_agent",
                "N/A"
            )
        )

    with col4:

        st.markdown("### 📊 Research Agent")

        st.info(
            multi_agent.get(
                "research_agent",
                "N/A"
            )
        )

    st.divider()

    # ==========================================
    # EXECUTIVE REPORT
    # ==========================================

    st.subheader("📄 Executive AI Report")

    if "report_generated" not in st.session_state:

        st.session_state.report_generated = False

    if "report_result" not in st.session_state:

        st.session_state.report_result = {}

    if st.button("Generate Executive AI Report"):

        with st.spinner("Generating AI Report..."):

            report_response = requests.post(
                f"{BASE_API_URL}/generate-report",
                json={
                    "ticker": ticker
                }
            )

            report_result = report_response.json()

            st.session_state.report_generated = True

            st.session_state.report_result = report_result

    if st.session_state.report_generated:

        st.success(
            "Executive AI Report Generated"
        )

        st.json(
            st.session_state.report_result
        )
        pdf_path = st.session_state.report_result.get("pdf_file")

        if pdf_path:

         with open(pdf_path, "rb") as pdf_file:

          st.download_button(
            label="⬇ Download Executive Report",
            data=pdf_file,
            file_name=pdf_path,
            mime="application/pdf"
        )

    st.divider()

    # ==========================================
    # STOCK CHART
    # ==========================================

    chart_response = requests.get(
            f"{BASE_API_URL}/stock-chart/{ticker}"
    )

    chart_data = chart_response.json()

    if isinstance(chart_data, list):

        df = pd.DataFrame(chart_data)

        fig = px.line(
            df,
            x="Date",
            y="Close",
            title=f"{ticker} Stock Price (6 Months)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.error("Chart data invalid")

# ==========================================
# ANNUAL REPORT QA PAGE
# ==========================================

if page == "Annual Report QA":

    # ======================================
    # SESSION STATE
    # ======================================

    if "pdf_uploaded" not in st.session_state:
        st.session_state.pdf_uploaded = False

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ======================================
    # PDF UPLOAD
    # ======================================

    st.subheader("📄 Upload Annual Report")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if (
        uploaded_file is not None
        and not st.session_state.pdf_uploaded
    ):

        files = {
            "file": uploaded_file
        }

        with st.spinner(
            "Uploading and processing PDF..."
        ):

            response = requests.post(
                f"{BASE_API_URL}/upload-report",
                files=files
            )

            result = response.json()

            st.success(
                "PDF Processed Successfully"
            )

            st.session_state.pdf_uploaded = True

    st.divider()

    # ======================================
    # SAMPLE QUESTIONS
    # ======================================

    sample_questions = [

        "What are the major financial risks?",

        "Summarize the company's financial performance.",

        "What are the key revenue drivers?",

        "What are the future growth opportunities?",

        "What are the profitability concerns?",

        "What are the operational challenges?",

        "What are the major business risks mentioned?",

        "Summarize management's future outlook.",

        "What are the company's expansion plans?",

        "What are the key strategic initiatives?",

        "What are the major investment risks?",

        "How is the company performing financially?",

        "What are the long-term market opportunities?",

        "What are the major cost pressures?",

        "What are the key takeaways for investors?"

    ]

    selected_question = st.selectbox(

        "📌 Choose Sample Financial Question",

        sample_questions

    )

    # ======================================
    # AI CHAT
    # ======================================

    st.subheader("🤖 Financial AI Chat")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask questions about annual report"
    )

    # ======================================
    # USE SELECTED SAMPLE QUESTION
    # ======================================

    if not prompt:
        prompt = selected_question

    # ======================================
    # AI RESPONSE
    # ======================================

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing annual report..."
            ):

                response = requests.get(
                    f"{BASE_API_URL}/rag-qa",
                    params={
                        "query": prompt
                    }
                )

                result = response.json()

                answer = result.get(
                    "answer",
                    "No answer generated."
                )

                st.markdown(answer)

                with st.expander(
                    "📚 View Retrieved Sources"
                ):

                    for idx, source in enumerate(
                        result.get("sources", [])
                    ):

                        st.write(
                            f"Source {idx+1}"
                        )

                        st.caption(
                            source[:1000]
                        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )