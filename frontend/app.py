import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Financial Research Assistant",
    layout="wide"
)

st.sidebar.title("📊 FinSight AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Stock Analysis",
        "Annual Report QA"
    ]
)

st.title("📈 AI Financial Research Assistant")


# ==========================================
# STOCK ANALYSIS PAGE
# ==========================================

if page == "Stock Analysis":

    ticker = st.text_input(
        "Enter Stock Ticker",
        placeholder="Example: NVDA"
    )

    if st.button("Analyze Stock"):

        if ticker.strip() == "":

            st.error("Please enter a stock ticker.")

        else:

            with st.spinner("Analyzing stock..."):

                # =========================
                # STOCK ANALYSIS API
                # =========================

                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    json={
                        "ticker": ticker
                    }
                )

                result = response.json()

                analysis = result.get("analysis", {})

                if analysis:

                    st.success("Analysis Complete")

                    st.subheader("🏢 Company Overview")
                    st.write(
                        analysis.get(
                            "company_overview",
                            "N/A"
                        )
                    )

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

                    st.subheader("📉 Risk Analysis")
                    st.write(
                        analysis.get(
                            "risk_analysis",
                            "N/A"
                        )
                    )

                    st.subheader("🚀 Long-Term Outlook")
                    st.write(
                        analysis.get(
                            "long_term_outlook",
                            "N/A"
                        )
                    )

                    st.subheader("💡 Recommendation")
                    st.info(
                        analysis.get(
                            "recommendation",
                            "N/A"
                        )
                    )

                else:

                    st.error("Analysis data not found.")

                # =========================
                # CHART API
                # =========================

                chart_response = requests.get(
                    f"http://127.0.0.1:8000/stock-chart/{ticker}"
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
    # SESSION MEMORY
    # ======================================

    if "messages" not in st.session_state:

        st.session_state.messages = []

    # ======================================
    # PDF UPLOAD SECTION
    # ======================================

    st.subheader("📄 Upload Annual Report")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        files = {
            "file": uploaded_file
        }

        with st.spinner("Uploading and processing PDF..."):

            response = requests.post(
                "http://127.0.0.1:8000/upload-report",
                files=files
            )

            result = response.json()

            st.success("PDF Processed Successfully")

    st.divider()

    # ======================================
    # CHAT HEADER
    # ======================================

    st.subheader("🤖 Financial AI Chat")

    # ======================================
    # DISPLAY CHAT HISTORY
    # ======================================

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # ======================================
    # CHAT INPUT
    # ======================================

    prompt = st.chat_input(
        "Ask questions about annual report"
    )

    # ======================================
    # USER QUESTION
    # ======================================

    if prompt:

        # USER MESSAGE
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        # ==================================
        # AI RESPONSE
        # ==================================

        with st.chat_message("assistant"):

            with st.spinner("Analyzing annual report..."):

                response = requests.get(
                    "http://127.0.0.1:8000/rag-qa",
                    params={
                        "query": prompt
                    }
                )

                result = response.json()

                answer = result["answer"]

                st.markdown(answer)

                # ==========================
                # SOURCES
                # ==========================

                with st.expander("📚 View Retrieved Sources"):

                    for idx, source in enumerate(result["sources"]):

                        st.write(f"Source {idx+1}")

                        st.caption(source[:1000])

        # SAVE AI RESPONSE
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )