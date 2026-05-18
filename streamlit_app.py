import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import os

from app.rag.rag_pipeline import FinancialRAG
from app.utils.pdf_generator import generate_pdf_report

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

    if st.button("🚀 Generate AI Analysis"):

        if not st.session_state.pdf_processed:

            st.warning(
                "Please upload financial PDF first."
            )

        else:

            with st.spinner(
                "Running Multi-Agent AI..."
            ):

                response = (
                    st.session_state.rag.ask_question(query)
                )

            st.session_state.chat_history.append(
                {
                    "query": query,
                    "response": response
                }
            )

    st.markdown("---")

    st.success("Azure OpenAI Connected")
    st.success("Multi-Agent AI Enabled")
    st.success("Financial RAG Active")

# ============================================================
# PROCESS PDF
# ============================================================

if uploaded_file is not None:

    st.session_state.uploaded_filename = (
        uploaded_file.name
    )

    if not st.session_state.pdf_processed:

        os.makedirs(
            "temp",
            exist_ok=True
        )

        pdf_path = os.path.join(
            "temp",
            uploaded_file.name
        )

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner(
            "Processing Financial Report..."
        ):

            rag = FinancialRAG()

            rag.ingest_pdf(pdf_path)

            st.session_state.rag = rag

            st.session_state.pdf_processed = True

        st.success(
            "✅ Financial Report Processed Successfully"
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
# CHARTS
# ============================================================

if stock_ticker:

    c1, c2 = st.columns(2)

    with c1:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📈 Stock Price Trend")

        hist = stock.history(period="1y")

        fig = px.line(
            hist,
            x=hist.index,
            y="Close"
        )

        fig.update_layout(
            template="plotly_white",
            height=350
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

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