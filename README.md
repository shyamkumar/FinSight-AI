# 📊 FinSight AI

## Multi-Agent Financial Research Assistant using Azure OpenAI

---

# 🚀 Project Overview

FinSight AI is a production-grade AI-powered financial research assistant designed to automate the analysis of large annual reports and financial documents using Agentic AI, Retrieval-Augmented Generation (RAG), and Multi-Agent Systems.

The platform enables users to:

* Upload financial annual reports (PDFs)
* Automatically extract financial insights
* Perform AI-powered financial Q&A
* Analyze risks and strategic opportunities
* Generate downloadable AI reports
* Visualize company stock market performance
* Use multiple AI agents for deep analysis

This project was developed as an End Semester Capstone Project for:

# IIT Bombay – AI/ML in Practice

---

# 🎯 Problem Statement

Financial annual reports are often:

* Extremely lengthy
* Complex to understand
* Time-consuming to analyze
* Difficult for non-financial users

Investors, analysts, and business professionals require faster and smarter ways to:

* Understand company performance
* Identify risks
* Discover growth opportunities
* Generate strategic insights

Traditional manual analysis requires significant domain expertise and many hours of effort.

---

# ✅ Solution

FinSight AI solves this problem using:

* Retrieval-Augmented Generation (RAG)
* Azure OpenAI
* Multi-Agent AI systems
* Real-time financial data visualization
* AI-powered financial report generation

The system automatically:

1. Extracts text from uploaded PDFs
2. Chunks the document
3. Generates embeddings
4. Stores vectors in vector database
5. Uses multiple AI agents for analysis
6. Generates intelligent financial insights
7. Displays live stock market data
8. Produces downloadable AI-generated reports

---

# 🧠 Key Features

## ✅ PDF Financial Report Upload

Upload company annual reports in PDF format.

## ✅ RAG Pipeline

Uses Retrieval-Augmented Generation for context-aware financial analysis.

## ✅ Multi-Agent AI System

Includes multiple specialized agents:

* Financial Analysis Agent
* Risk Analysis Agent
* Strategic Insights Agent
* Summary Agent

## ✅ Azure OpenAI Integration

Uses Azure-hosted OpenAI models for scalable enterprise AI.

## ✅ Dynamic Stock Dashboard

Automatically detects company ticker from uploaded file and fetches:

* Live stock price
* Market cap
* Revenue
* Net income
* Stock trends

## ✅ AI Financial Chat

Users can ask questions such as:

* What are the major risks?
* Summarize the annual report.
* What are growth opportunities?
* Analyze financial performance.

## ✅ Downloadable AI Reports

Generate PDF reports containing AI-generated financial analysis.

## ✅ Production-Grade UI

Modern enterprise dashboard built using Streamlit.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   Upload PDF Report │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  PDF Text Extraction│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Text Chunking       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Embedding Generation│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Vector Database     │
                    │ (FAISS)             │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │      Multi-Agent AI System     │
              ├────────────────────────────────┤
              │ Financial Analysis Agent       │
              │ Risk Analysis Agent            │
              │ Strategic Insight Agent        │
              │ Summary Agent                  │
              └────────────────┬───────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ AI Financial Output │
                    └─────────────────────┘
```

---

# 🛠️ Tech Stack

| Technology   | Purpose               |
| ------------ | --------------------- |
| Python       | Backend Development   |
| Azure OpenAI | LLM and Embeddings    |
| CrewAI       | Multi-Agent AI System |
| Streamlit    | Frontend Dashboard    |
| FAISS        | Vector Database       |
| Plotly       | Data Visualization    |
| LangChain    | RAG Orchestration     |
| PyPDF        | PDF Text Extraction   |
| yFinance     | Live Stock Data       |

---

# 📂 Project Structure

```text
FinSight-AI/
│
├── app/
│   ├── agents/
│   │   ├── financial_agent.py
│   │   ├── risk_agent.py
│   │   ├── strategy_agent.py
│   │   └── crew_manager.py
│   │
│   ├── rag/
│   │   ├── rag_pipeline.py
│   │   ├── embeddings.py
│   │   └── vector_store.py
│   │
│   ├── utils/
│   │   ├── azure_openai.py
│   │   ├── llm_config.py
│   │   └── pdf_generator.py
│
├── streamlit_app.py
├── requirements.txt
├── .env
├── README.md
└── test_rag.py
```

---

# ⚙️ Installation Guide

# Step 1 – Clone Repository

```bash
git clone https://github.com/shyamkumar/FinSight-AI.git

cd FinSight-AI
```

---

# Step 2 – Create Virtual Environment

## Windows

```bash
python -m venv venv
```

---

# Step 3 – Activate Environment

## PowerShell

```bash
venv\Scripts\activate
```

---

# Step 4 – Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ☁️ Azure OpenAI Setup

# Step 1 – Create Azure OpenAI Resource

Go to:

[https://portal.azure.com](https://portal.azure.com)

Create:

* Azure OpenAI Resource
* GPT deployment
* Embedding deployment

---

# Step 2 – Create `.env` File

```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4.1-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
```

---

# ▶️ Run Streamlit Application

```bash
streamlit run streamlit_app.py
```

---

# 📊 How to Use

# 1️⃣ Upload Financial Report

Upload:

* NVIDIA annual report
* Tesla annual report
* Apple annual report
* Reliance annual report

---

# 2️⃣ Ask Questions

Examples:

```text
What are the major risks?
```

```text
Summarize the annual report.
```

```text
Analyze company financial performance.
```

```text
What are future growth opportunities?
```

---

# 3️⃣ Generate AI Analysis

The system will:

* retrieve relevant chunks
* run multi-agent analysis
* generate AI response
* display insights

---

# 4️⃣ Download AI Report

Export AI-generated analysis as PDF.

---

# 🤖 Multi-Agent AI Workflow

## Financial Analysis Agent

Responsible for:

* financial summary
* profitability analysis
* business performance

---

## Risk Analysis Agent

Responsible for:

* cybersecurity risk
* operational risk
* supply chain risk
* market risk

---

## Strategic Insight Agent

Responsible for:

* future growth opportunities
* AI strategy
* market expansion

---

## Summary Agent

Responsible for:

* final consolidated response
* executive summary

---

# 📈 Example Companies Tested

| Company   | Ticker      |
| --------- | ----------- |
| NVIDIA    | NVDA        |
| Tesla     | TSLA        |
| Apple     | AAPL        |
| Microsoft | MSFT        |
| Amazon    | AMZN        |
| Reliance  | RELIANCE.NS |
| TCS       | TCS.NS      |

---

# 📷 Screenshots

## Dashboard UI

(Add screenshot here)

---

## AI Financial Chat

(Add screenshot here)

---

## AI Risk Analysis

(Add screenshot here)

---

# 🔥 Key Innovations

## ✅ Agentic AI System

Uses multiple collaborating AI agents.

## ✅ Production-Grade Financial Copilot

Enterprise-style AI dashboard.

## ✅ Dynamic Company Detection

Automatically detects company from uploaded PDF.

## ✅ Live Market Data Integration

Real-time stock data using yFinance.

## ✅ RAG-based Financial Intelligence

Context-aware financial question answering.

---

# 🚀 Future Scope

Future improvements can include:

* Autonomous financial agents
* Portfolio recommendation engine
* Real-time SEC filing ingestion
* Multilingual AI assistant
* Voice-enabled AI financial advisor
* Advanced forecasting models
* Cloud-native scalable deployment

---

# 📌 Challenges Faced

* Large PDF processing latency
* Embedding generation time
* Streamlit session state management
* Azure OpenAI deployment configuration
* Multi-agent orchestration complexity
* Dynamic UI synchronization

---

# 🎓 Learning Outcomes

This project helped in understanding:

* Production AI architecture
* Agentic AI systems
* RAG pipelines
* Vector databases
* Azure OpenAI integration
* Financial AI applications
* Enterprise dashboard development

---

# 👨‍💻 Author

## Shyam Kumar

Senior Software Engineer | Salesforce Developer | AI/ML Enthusiast

IIT Bombay – AI/ML in Practice

---

# 📜 License

This project is developed for educational and research purposes.

---

# ⭐ Acknowledgements

Special thanks to:

* IIT Bombay
* Azure OpenAI
* Streamlit
* CrewAI
* LangChain
* OpenAI

---

# 🚀 Final Output

FinSight AI successfully demonstrates:

✅ Agentic AI

✅ Multi-Agent Systems

✅ Financial RAG Pipeline

✅ Azure OpenAI Deployment

✅ Enterprise AI Dashboard

✅ AI Financial Research Automation

This project represents a production-grade AI financial research platform suitable for enterprise-scale intelligent financial analysis.
