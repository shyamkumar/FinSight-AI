
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

    # ======================================
    # INPUT
    # ======================================

    ticker = st.text_input(

        "Enter Company Name or Stock Ticker",

        placeholder=(
            "Example: Tesla, NVIDIA, "
            "TCS, Reliance"
        )

    )

    # ======================================
    # ANALYZE BUTTON
    # ======================================

    if st.button("Analyze Stock"):

        with st.spinner(
            "Analyzing stock..."
        ):

            response = requests.post(

                f"{BASE_API_URL}/analyze",

                json={
                    "ticker": ticker
                }

            )

            if response.status_code == 200:

                result = response.json()

                if "error" in result:

                    st.error(
                        result["error"]
                    )

                    st.stop()

                st.session_state.analysis_result = (
                    result
                )

            else:

                st.error(
                    f"Backend Error: "
                    f"{response.text}"
                )

                st.stop()

    # ======================================
    # LOAD ANALYSIS RESULT
    # ======================================

    stored_result = st.session_state.get(

        "analysis_result",

        {}

    )

    # ======================================
    # SHOW RESULTS
    # ======================================

    if stored_result:

        resolved_ticker = stored_result.get(

            "resolved_ticker",

            ticker

        )

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

        st.success(
            f"Detected Ticker: "
            f"{resolved_ticker}"
        )

        st.success(
            "Analysis Complete"
        )

        # ======================================
        # KPI DASHBOARD
        # ======================================

        st.subheader(
            "📊 Financial KPI Dashboard"
        )

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        with col1:

            st.metric(

                "Market Cap",

                f"${round(metrics.get('marketCap', 0)/1e12, 2)}T"

                if metrics.get(
                    "marketCap"
                )

                else "N/A"

            )

        with col2:

            st.metric(

                "Trailing P/E",

                round(
                    metrics.get(
                        "trailingPE",
                        0
                    ),
                    2
                )

                if metrics.get(
                    "trailingPE"
                )

                else "N/A"

            )

        with col3:

            st.metric(

                "Profit Margin",

                f"{round(metrics.get('profitMargins', 0)*100, 2)}%"

                if metrics.get(
                    "profitMargins"
                )

                else "N/A"

            )

        with col4:

            st.metric(

                "Revenue Growth",

                f"{round(metrics.get('revenueGrowth', 0)*100, 2)}%"

                if metrics.get(
                    "revenueGrowth"
                )

                else "N/A"

            )

        st.divider()

        # ======================================
        # STOCK PRICE CHART
        # ======================================

        st.subheader(
            "📈 Stock Price Trend"
        )

        chart_response = requests.get(

            f"{BASE_API_URL}/stock-chart/"
            f"{resolved_ticker}"

        )

        if chart_response.status_code == 200:

            chart_data = (
                chart_response.json()
            )

            if isinstance(
                chart_data,
                list
            ):

                df = pd.DataFrame(
                    chart_data
                )

                if (

                    not df.empty

                    and "Date"
                    in df.columns

                    and "Close"
                    in df.columns

                ):

                    fig = px.line(

                        df,

                        x="Date",

                        y="Close",

                        title=(
                            f"{resolved_ticker} "
                            f"Stock Price "
                            f"(6 Months)"
                        )

                    )

                    st.plotly_chart(

                        fig,

                        use_container_width=True

                    )

                else:

                    st.warning(

                        "Stock chart "
                        "data unavailable."

                    )

            else:

                st.warning(

                    "Invalid stock "
                    "chart data."

                )

        else:

            st.warning(
                "Unable to load stock chart."
            )

        st.divider()

        # ======================================
        # EXECUTIVE AI SUMMARY
        # ======================================

        st.subheader(
            "🧠 Executive AI Summary"
        )

        if isinstance(analysis, dict):

            st.markdown(
                f"""
### 🏢 Company Overview
{analysis.get('company_overview', 'N/A')}

---

### 🚨 Risk Analysis
{analysis.get('risk_analysis', 'N/A')}

---

### 🔮 Long-Term Outlook
{analysis.get('long_term_outlook', 'N/A')}

---

### 💡 Investment Recommendation
{analysis.get('recommendation', 'N/A')}
"""
            )

            st.markdown(
                "### 📈 Bullish Factors"
            )

            bullish = analysis.get(
                "bullish_factors",
                []
            )

            for item in bullish:

                st.markdown(
                    f"- {item}"
                )

            st.markdown(
                "### ⚠️ Bearish Factors"
            )

            bearish = analysis.get(
                "bearish_factors",
                []
            )

            for item in bearish:

                st.markdown(
                    f"- {item}"
                )

        else:

            st.markdown(
                analysis
            )

        st.divider()

        # ======================================
        # AI INVESTMENT SCORES
        # ======================================

        st.subheader(
            "🤖 AI Investment Scores"
        )

        score_col1, score_col2, score_col3 = (
            st.columns(3)
        )

        with score_col1:

            st.metric(

                "Growth Score",

                ai_scores.get(
                    "growth_score",
                    "N/A"
                )

            )

        with score_col2:

            st.metric(

                "Risk Score",

                ai_scores.get(
                    "risk_score",
                    "N/A"
                )

            )

        with score_col3:

            st.metric(

                "Investment Rating",

                ai_scores.get(
                    "investment_rating",
                    "N/A"
                )

            )

        st.divider()

        # ======================================
        # MULTI AGENT ANALYSIS
        # ======================================

        st.subheader(
            "👥 Multi-Agent AI Analysis"
        )

        if isinstance(
            multi_agent,
            dict
        ):

            for role, insight in (
                multi_agent.items()
            ):

                with st.expander(
                    f"{role}"
                ):

                    st.markdown(
                        insight
                    )

        else:

            st.warning(
                "Multi-agent analysis unavailable."
            )

        st.divider()

        # ======================================
        # EXECUTIVE REPORT
        # ======================================

        st.subheader(
            "📄 Executive AI Report"
        )

        if st.button(
            "Generate Executive AI Report"
        ):

            with st.spinner(
                "Generating AI report..."
            ):

                report_response = requests.post(

                    f"{BASE_API_URL}/generate-report",

                    json={

                        "ticker": resolved_ticker

                    }

                )

                if (
                    report_response.status_code
                    == 200
                ):

                    report_result = (

                        report_response.json()

                    )

                    st.success(

                        "Executive AI Report Generated"

                    )

                    download_url = (

                        f"{BASE_API_URL}"
                        f"/download-report/"
                        f"{resolved_ticker}"

                    )

                    st.markdown(

                        f"[📥 Download Executive Report]"
                        f"({download_url})"

                    )

                else:

                    st.error(
                        "Report generation failed."
                    )
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

    use_sample_question = st.button(
        "🚀 Ask Sample Question"
    )

    # ======================================
    # AI CHAT
    # ======================================

    st.subheader("🤖 Financial AI Chat")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    user_prompt = st.chat_input(
        "Ask questions about annual report",
        key="annual_report_chat_input"
    )

    prompt = None

    # ======================================
    # HANDLE QUESTIONS
    # ======================================

    if use_sample_question:

        prompt = selected_question

    elif user_prompt:

        prompt = user_prompt

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
                     "🧠 Multi-Agent Execution Flow"
                ):

                    for step in result.get(
                        "agent_flow",
                     []
                   ):

                     st.success(step)

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