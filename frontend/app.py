import streamlit as st
import requests

st.set_page_config(
    page_title="AI Financial Research Assistant",
    layout="wide"
)

st.title("📈 AI Financial Research Assistant")

ticker = st.text_input(
    "Enter Stock Ticker",
    placeholder="Example: NVDA"
)

if st.button("Analyze Stock"):

    with st.spinner("Analyzing stock..."):

        response = requests.post(
            "http://127.0.0.1:8000/analyze",
            json={
                "ticker": ticker
            }
        )

        result = response.json()

        st.success("Analysis Complete")

        st.subheader("AI Financial Analysis")

        st.json(result)
        st.divider()

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

        st.json(result)
        st.divider()

st.subheader("🤖 Ask Questions About Annual Report")

rag_query = st.text_input(
    "Ask financial questions"
)

if st.button("Ask AI"):

    with st.spinner("Generating answer..."):

        response = requests.get(
            "http://127.0.0.1:8000/rag-qa",
            params={
                "query": rag_query
            }
        )

        result = response.json()

        st.success("Answer Generated")

        st.subheader("AI Answer")

        st.write(result["answer"])