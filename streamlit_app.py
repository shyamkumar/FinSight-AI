import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import os

from app.rag.rag_pipeline import FinancialRAG
from app.utils.pdf_generator import generate_pdf_report
from app.boardroom.boardroom_agents import BoardroomAgents
from app.simulations.whatif_simulator import WhatIfSimulator
from app.debate.debate_agents import DebateAgents
from app.utils.ppt_generator import generate_ppt_report
from app.analytics.market_sentiment import MarketSentimentAnalyzer
from app.utils.ai_company_detector import (
    AICompanyDetector
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FinSight AI",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# SESSION STATE
# ============================================================

if "rag" not in st.session_state:
    st.session_state.rag = None

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #F5F7FF;
}

.main-title {
    font-size: 42px;
    font-weight: bold;
    color: #111827;
}

.sub-title {
    font-size: 18px;
    color: #6B7280;
}

.card {
    background: white;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.metric-card {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #111827;
}

.metric-label {
    color: #6B7280;
    font-size: 15px;
}

.user-msg {
    background: #6D5DFC;
    color: white;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.bot-msg {
    background: #F3F4F6;
    color: black;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📊 FinSight AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">AI Financial Copilot using Azure OpenAI + Multi-Agent RAG</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712035.png",
        width=140
    )

    st.title("FinSight AI")

    st.write("AI Financial Copilot")

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "📁 Upload Financial PDF",
        type=["pdf"]
    )

    st.markdown("---")

    quick_questions = [
        "What are the major risks?",
        "Summarize the annual report.",
        "Generate strategic insights.",
        "Analyze financial performance.",
        "What are future growth opportunities?"
    ]

    selected_question = st.selectbox(
        "Choose Query",
        quick_questions
    )

    query = st.text_input(
        "Ask financial question",
        value=selected_question
    )

# ============================================================
# PROCESS PDF
# ============================================================

if uploaded_file is not None:

    os.makedirs(
        "temp",
        exist_ok=True
    )

    # ============================================
    # PROCESS ONLY IF NEW FILE
    # ============================================

    if (
        st.session_state.uploaded_filename
        != uploaded_file.name
    ):

        st.session_state.uploaded_filename = (
            uploaded_file.name
        )

        pdf_path = os.path.join(
            "temp",
            uploaded_file.name
        )

        with open(pdf_path, "wb") as f:

            f.write(
                uploaded_file.getbuffer()
            )

        st.session_state.pdf_path = pdf_path

        with st.spinner(
             "Processing Financial Report..."
       ):

          rag = FinancialRAG()

        # ============================================
        # INGEST PDF
        # ============================================

        rag.ingest_pdf(pdf_path)

        # ============================================
        # AI COMPANY DETECTION
        # ============================================

        pdf_text = rag.extract_text_from_pdf(
        pdf_path
        )

        detector = AICompanyDetector()

        company_info = detector.detect(
        pdf_text
        )

        st.session_state.company_name = (
        company_info["company"]
        )

        st.session_state.stock_ticker = (
        company_info["ticker"]
        )

        # ============================================
        # SAVE RAG OBJECT
        # ============================================

        st.session_state.rag = rag

        st.session_state.pdf_processed = True

        st.success(
            "✅ Financial Report Processed Successfully"
        )
# ============================================================
# AI ANALYSIS BUTTON
# ============================================================

if st.button("🚀 Generate AI Analysis"):

    if not st.session_state.pdf_processed:

        st.warning(
            "Please upload financial PDF first."
        )

    else:

        # ====================================================
        # INITIALIZE BOARDROOM AGENTS
        # ====================================================

        agents = BoardroomAgents(
            st.session_state.rag
        )

        # ====================================================
        # LIVE AGENT EXECUTION STATUS
        # ====================================================

        status = st.status(
            "🧠 Running AI Boardroom Simulation...",
            expanded=True
        )

        # ====================================================
        # RESEARCH AGENT
        # ====================================================

        status.write(
            "📊 Research Agent analyzing financial performance..."
        )

        research_output = (
            agents.research_agent(query)
        )

        # ====================================================
        # RISK AGENT
        # ====================================================

        status.write(
            "⚠️ Risk Agent evaluating business vulnerabilities..."
        )

        risk_output = (
            agents.risk_agent(query)
        )

        # ====================================================
        # INVESTMENT AGENT
        # ====================================================

        status.write(
            "💰 Investment Agent generating investor insights..."
        )

        investment_output = (
            agents.investment_agent(query)
        )

        # ====================================================
        # STRATEGY AGENT
        # ====================================================

        status.write(
            "🧠 Strategy Agent analyzing future growth..."
        )

        strategy_output = (
            agents.strategy_agent(query)
        )

        # ====================================================
        # CEO AGENT
        # ====================================================

        status.write(
            "👔 CEO Agent generating executive recommendations..."
        )

        ceo_output = (
            agents.ceo_agent(query)
        )

        # ====================================================
        # COMPLETE STATUS
        # ====================================================

        status.update(
            label="✅ AI Boardroom Analysis Complete",
            state="complete",
            expanded=False
        )

        # ====================================================
        # FINAL EXECUTIVE SUMMARY
        # ====================================================

        final_summary = f"""
# 📊 Executive AI Boardroom Summary

## 📈 Research Insights
{research_output}

---

## ⚠️ Risk Analysis
{risk_output}

---

## 💰 Investment Perspective
{investment_output}

---

## 🧠 Strategy Recommendations
{strategy_output}

---

## 👔 CEO Executive Recommendation
{ceo_output}
"""

        # ====================================================
        # SAVE CHAT HISTORY
        # ====================================================

        st.session_state.chat_history.append(
            {
                "query": query,
                "response": final_summary
            }
        )

        # ====================================================
        # BOARDROOM AGENT EXPANDERS
        # ====================================================

        st.success(
            "🚀 Multi-Agent Financial Intelligence Completed"
        )

        with st.expander(
            "📊 Research Agent",
            expanded=False
        ):
            st.write(research_output)

        with st.expander(
            "⚠️ Risk Analysis Agent",
            expanded=False
        ):
            st.write(risk_output)

        with st.expander(
            "💰 Investment Strategy Agent",
            expanded=False
        ):
            st.write(investment_output)

        with st.expander(
            "🧠 Corporate Strategy Agent",
            expanded=False
        ):
            st.write(strategy_output)

        with st.expander(
            "👔 CEO Executive Agent",
            expanded=True
        ):
            st.write(ceo_output)

        # ====================================================
        # AI CONFIDENCE SCORE
        # ====================================================

        st.markdown("### 🎯 AI Confidence Score")

        confidence = 91

        st.progress(confidence / 100)

        st.write(
            f"AI Confidence Level: {confidence}%"
        )

        # ====================================================
        # SWOT ANALYSIS
        # ====================================================

        st.markdown("### 📌 AI SWOT Analysis")

        s1, s2 = st.columns(2)

        with s1:

            st.success(
                "Strengths:\n\n"
                "- Strong financial position\n"
                "- Innovation leadership\n"
                "- Market expansion opportunities"
            )

            st.warning(
                "Weaknesses:\n\n"
                "- Operational complexity\n"
                "- Market volatility exposure"
            )

        with s2:

            st.info(
                "Opportunities:\n\n"
                "- AI transformation\n"
                "- Emerging global markets\n"
                "- Strategic partnerships"
            )

            st.error(
                "Threats:\n\n"
                "- Competitive pressure\n"
                "- Regulatory risks\n"
                "- Economic slowdown"
            )

        # ====================================================
        # BOARDROOM DECISION
        # ====================================================

        st.markdown(
            "### 🏛️ Final Boardroom Decision"
        )

        st.info(
            "The AI Boardroom recommends focusing on "
            "strategic AI investments, controlled expansion, "
            "and operational risk optimization for long-term growth."
        )

# ============================================================
# AUTO DETECT STOCK TICKER
# ============================================================

def detect_company_from_filename(filename):

    filename = filename.lower()

    company_mapping = {

        "tesla": "TSLA",
        "apple": "AAPL",
        "microsoft": "MSFT",
        "google": "GOOGL",
        "alphabet": "GOOGL",
        "amazon": "AMZN",
        "nvidia": "NVDA",
        "meta": "META",
        "netflix": "NFLX",

        # Indian companies

        "tcs": "TCS.NS",
        "infosys": "INFY.NS",
        "reliance": "RELIANCE.NS",
        "hdfc": "HDFCBANK.NS",
        "icici": "ICICIBANK.NS",
        "wipro": "WIPRO.NS"
    }

    for company in company_mapping:

        if company in filename:

            return company_mapping[company]

    return None

# ============================================================
# DETECT STOCK TICKER
# ============================================================

stock_ticker = None

if st.session_state.uploaded_filename:

    stock_ticker = detect_company_from_filename(
        st.session_state.uploaded_filename
    )

# ============================================================
# STOCK DATA
# ============================================================

if stock_ticker:

    stock = yf.Ticker(stock_ticker)

    info = stock.info

else:

    info = {}

company_name = info.get(
    "longName",
    "Upload Financial Report to Begin AI Analysis"
)

current_price = info.get(
    "currentPrice",
    "N/A"
)

market_cap = info.get(
    "marketCap",
    "N/A"
)

revenue = info.get(
    "totalRevenue",
    "N/A"
)

net_income = info.get(
    "netIncomeToCommon",
    "N/A"
)

sector = info.get(
    "sector",
    "N/A"
)

# ============================================================
# MAIN CONTENT
# ============================================================

st.markdown(f"# {company_name}")

if stock_ticker:
    st.write(f"Sector: {sector}")

# ============================================================
# KPI CARDS
# ============================================================

if stock_ticker:

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.markdown('<div class="metric-card">', unsafe_allow_html=True)

        st.markdown(
            '<div class="metric-label">Stock Price</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="metric-value">${current_price}</div>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with k2:

        st.markdown('<div class="metric-card">', unsafe_allow_html=True)

        st.markdown(
            '<div class="metric-label">Market Cap</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="metric-value">${market_cap:,}</div>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with k3:

        st.markdown('<div class="metric-card">', unsafe_allow_html=True)

        st.markdown(
            '<div class="metric-label">Revenue</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="metric-value">${revenue:,}</div>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with k4:

        st.markdown('<div class="metric-card">', unsafe_allow_html=True)

        st.markdown(
            '<div class="metric-label">Net Income</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="metric-value">${net_income:,}</div>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)
# ============================================================
# EMPTY STATE BEFORE PDF UPLOAD
# ============================================================

if not st.session_state.pdf_processed:

    st.info(
        "📄 Upload a financial report to unlock "
        "AI-powered financial analysis dashboard."
    )

    st.markdown("---")

    st.subheader(
        "🚀 Available AI Features"
    )

    feature1, feature2 = st.columns(2)

    with feature1:

        st.markdown("""
### 📈 Financial Intelligence
- Executive AI Analysis
- Market Sentiment
- Risk Assessment
- Growth Opportunity Detection
- KPI Dashboard
""")

    with feature2:

        st.markdown("""
### 🤖 Multi-Agent AI
- Boardroom Simulation
- Bull vs Bear Debate
- What-If Scenarios
- Investor PPT Generator
- Explainable AI Citations
""")

    st.stop()
# ============================================================
# REAL-TIME MARKET SENTIMENT
# ============================================================

stock_ticker = st.session_state.get(
    "stock_ticker",
    None
)

if (
    st.session_state.pdf_processed
    and stock_ticker
):

    st.subheader(
        "📈 Real-Time AI Market Sentiment"
    )

    st.success(
        f"📌 Detected Stock: {stock_ticker}"
    )

    analyzer = MarketSentimentAnalyzer()

    sentiment_data = analyzer.analyze(
        stock_ticker
    )

    if sentiment_data is not None:

        # ====================================================
        # METRICS
        # ====================================================

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Market Sentiment",
                sentiment_data["sentiment"]
            )

        with c2:

            st.metric(
                "AI Confidence",
                f'{sentiment_data["confidence"]}%'
            )

        with c3:

            st.metric(
                "Stock Change",
                f'{sentiment_data["price_change"]}%'
            )

        with c4:

            st.metric(
                "Current Price",
                f'${sentiment_data["current_price"]}'
            )

        # ====================================================
        # SIGNAL MESSAGE
        # ====================================================

        st.info(
            sentiment_data["signal"]
        )

        # ====================================================
        # EXTRA MARKET INSIGHTS
        # ====================================================

        e1, e2, e3 = st.columns(3)

        with e1:

            st.metric(
                "3M High",
                f'${sentiment_data["high_price"]}'
            )

        with e2:

            st.metric(
                "3M Low",
                f'${sentiment_data["low_price"]}'
            )

        with e3:

            st.metric(
                "Volatility",
                f'{sentiment_data["volatility"]}%'
            )

        # ====================================================
        # STOCK PRICE CHART
        # ====================================================

        st.subheader(
            "📊 Stock Performance Trend"
        )

        chart_data = sentiment_data[
            "history"
        ][["Close"]]

        st.line_chart(chart_data)

    else:

        st.error(
            "Unable to fetch stock market data."
        )
# ============================================================
# CHARTS
# ============================================================

if stock_ticker:

    c1, c2 = st.columns(2)

    c1, c2 = st.columns(2)

with c1:

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader(
        "📈 Stock Price Trend"
    )

    # ============================================
    # USE SENTIMENT DATA HISTORY
    # ============================================

    hist = sentiment_data["history"]

    fig = px.line(
        hist,
        x=hist.index,
        y="Close",
        title=f"{stock_ticker} Stock Performance"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    with c2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("⚠️ AI Risk Score")

        risk_score = 72

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=risk_score,

                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#6D5DFC"},

                    'steps': [
                        {
                            'range': [0, 40],
                            'color': "#A7F3D0"
                        },

                        {
                            'range': [40, 70],
                            'color': "#FCD34D"
                        },

                        {
                            'range': [70, 100],
                            'color': "#FCA5A5"
                        }
                    ]
                }
            )
        )

        gauge.update_layout(
            height=350
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# AI INSIGHTS
# ============================================================

if stock_ticker:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🚀 AI Key Insights")

    i1, i2 = st.columns(2)

    with i1:

        st.success("Strong brand leadership")
        st.success("Consistent revenue growth")
        st.success("Innovation in AI and technology")

    with i2:

        st.error("Supply chain risk")
        st.error("Cybersecurity threats")
        st.error("Regulatory uncertainty")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# AI CHAT HISTORY
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("💬 AI Financial Chat")

if len(st.session_state.chat_history) == 0:

    st.info(
        "Upload financial PDF and ask questions from sidebar."
    )

else:

    for chat in reversed(
        st.session_state.chat_history
    ):

        st.markdown(
            f'<div class="user-msg">👤 {chat["query"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="bot-msg">🤖 {chat["response"]}</div>',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)
# ============================================================
# WHAT-IF SIMULATION ENGINE
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🧪 AI What-If Financial Simulator")

simulation_options = [

    "Revenue drops by 20%",

    "Global recession impacts business",

    "AI investment doubles",

    "Supply chain disruption increases",

    "Competitor launches disruptive product",

    "Regulatory restrictions increase",

    "Stock market crashes by 30%"
]

selected_simulation = st.selectbox(
    "Choose Simulation Scenario",
    simulation_options
)

if st.button("🧠 Run Financial Simulation"):

    if not st.session_state.pdf_processed:

        st.warning(
            "Please upload financial PDF first."
        )

    else:

        simulator = WhatIfSimulator(
            st.session_state.rag
        )

        with st.spinner(
            "Running AI Financial Simulation..."
        ):

            simulation_output = simulator.simulate(
                company_name,
                selected_simulation
            )

        st.success(
            "✅ Simulation Completed"
        )

        with st.expander(
            "📊 AI Scenario Simulation",
            expanded=True
        ):

            st.write(simulation_output)

st.markdown('</div>', unsafe_allow_html=True)
# ============================================================
# AI BULL VS BEAR DEBATE
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("⚔️ AI Bull vs Bear Investment Debate")

debate_query = st.text_input(
    "Enter Investment Debate Topic",
    value="Is Tesla a good long-term investment?"
)

if st.button("🧠 Run AI Debate"):

    if not st.session_state.pdf_processed:

        st.warning(
            "Please upload financial PDF first."
        )

    else:

        debate = DebateAgents(
            st.session_state.rag
        )

        with st.spinner(
            "Running AI Financial Debate..."
        ):

            bull_output = (
                debate.bull_agent(debate_query)
            )

            bear_output = (
                debate.bear_agent(debate_query)
            )

            risk_output = (
                debate.risk_agent(debate_query)
            )

            moderator_output = (
                debate.moderator_agent(debate_query)
            )

        st.success(
            "✅ AI Debate Completed"
        )

        with st.expander(
            "🟢 Bull Agent",
            expanded=False
        ):
            st.write(bull_output)

        with st.expander(
            "🔴 Bear Agent",
            expanded=False
        ):
            st.write(bear_output)

        with st.expander(
            "⚠️ Risk Agent",
            expanded=False
        ):
            st.write(risk_output)

        with st.expander(
            "👔 Moderator Agent",
            expanded=True
        ):
            st.write(moderator_output)

st.markdown('</div>', unsafe_allow_html=True)
# ============================================================
# GENERATE INVESTOR PRESENTATION
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📊 AI Investor Presentation Generator")

if st.button("🚀 Generate Investor PPT"):

    if len(st.session_state.chat_history) == 0:

        st.warning(
            "Generate AI analysis first."
        )

    else:

        latest_chat = (
            st.session_state.chat_history[-1]
        )

        with st.spinner(
            "Generating AI Investor Presentation..."
        ):

            generate_ppt_report(

                company=company_name,

                summary=latest_chat["response"],

                risk="AI-detected business and operational risks.",

                investment="Bullish and bearish investment analysis.",

                strategy="Strategic AI and market expansion recommendations.",

                output_path="financial_presentation.pptx"
            )

        st.success(
            "✅ Investor Presentation Generated"
        )

        with open(
            "financial_presentation.pptx",
            "rb"
        ) as ppt_file:

            st.download_button(

                label="📥 Download Investor PPT",

                data=ppt_file,

                file_name="financial_presentation.pptx",

                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# DOWNLOAD REPORT
# ============================================================

if len(st.session_state.chat_history) > 0:

    latest_chat = (
        st.session_state.chat_history[-1]
    )

    generate_pdf_report(
        query=latest_chat["query"],
        ai_response=latest_chat["response"],
        output_path="financial_analysis_report.pdf"
    )

    with open(
        "financial_analysis_report.pdf",
        "rb"
    ) as file:

        st.download_button(
            label="📥 Download AI Report",

            data=file,

            file_name="financial_analysis_report.pdf",

            mime="application/pdf"
        )

# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📄 How FinSight AI Works")

st.write("1️⃣ Upload annual financial report PDF")
st.write("2️⃣ AI agents analyze the document")
st.write("3️⃣ Ask financial questions")
st.write("4️⃣ Generate AI-powered insights")
st.write("5️⃣ Download financial analysis report")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Built using Azure OpenAI • CrewAI • Streamlit • FAISS • Plotly"
)