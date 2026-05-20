# 📈 FinSight AI — Cloud-Deployed AI Financial Research Assistant

FinSight AI is an enterprise-grade AI-powered Financial Research Assistant built using Azure OpenAI, Azure AI Search, FastAPI, and Streamlit.

The platform enables intelligent stock analysis, annual report question-answering (RAG), executive AI-generated investment reports, multi-agent financial reasoning, and cloud-native financial research workflows.

---

# 🚀 Features

## 📊 AI Stock Analysis
- Real-time stock analysis
- Company overview generation
- Bullish vs bearish analysis
- Risk assessment
- Long-term outlook prediction
- AI-powered investment recommendation

---

## 📈 Financial KPI Dashboard
- Market capitalization
- P/E ratio
- Profit margins
- Revenue growth
- AI investment score
- Risk level indicators
- Confidence metrics

---

## 🤖 Multi-Agent AI Workspace
Specialized AI agents collaborate to simulate institutional financial analysis.

### Agents:
- 🐂 Bull Agent
- 🐻 Bear Agent
- ⚠️ Risk Agent
- 📊 Research Agent

---

## 📄 Executive AI Report Generator
Generate downloadable executive-level financial PDF reports containing:
- AI stock analysis
- Financial KPIs
- Multi-agent insights
- Investment recommendations
- Strategic outlook

---

## 🔍 Annual Report QA (RAG)
Upload annual reports and ask natural language questions.

### Capabilities:
- PDF upload
- Semantic chunking
- Vector embeddings
- Azure AI Search retrieval
- AI-generated answers with source citations

---

## ☁️ Azure Cloud Architecture
- Azure OpenAI
- Azure AI Search
- Azure Blob Storage
- FastAPI backend
- Streamlit frontend
- Vector search architecture

---

# 🏗️ System Architecture

```text
User
   ↓
Streamlit Frontend
   ↓
FastAPI Backend
   ↓
Azure OpenAI
   ↓
Azure AI Search (Vector Search)
   ↓
Azure Blob Storage
```

---

# 🧠 AI Capabilities

- Retrieval-Augmented Generation (RAG)
- Multi-Agent AI reasoning
- Financial risk analysis
- AI investment scoring
- Semantic document retrieval
- Executive report generation

---

# 🛠️ Tech Stack

## Frontend
- Streamlit
- Plotly
- Pandas

## Backend
- FastAPI
- Python

## AI/ML
- Azure OpenAI
- Embeddings
- RAG Pipeline
- Vector Search

## Cloud
- Azure AI Search
- Azure Blob Storage
- Azure App Service

## Financial APIs
- Yahoo Finance (yfinance)

## Reporting
- ReportLab PDF Generation

---

# 📂 Project Structure

```text
FinSight-AI/
│
├── backend/
│   ├── main.py
│   ├── rag/
│   ├── tools/
│   └── services/
│
├── frontend/
│   ├── app.py
│   └── styles.css
│
├── reports/
│
├── requirements.txt
├── startup.sh
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone <your-github-repo-url>
cd FinSight-AI
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\\Scripts\\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint

AZURE_SEARCH_ENDPOINT=your_search_endpoint
AZURE_SEARCH_KEY=your_search_key
AZURE_SEARCH_INDEX=financial-reports

AZURE_STORAGE_CONNECTION_STRING=your_blob_connection
```

---

# ▶️ Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

# ▶️ Run Frontend

```bash
streamlit run frontend/app.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

# 📄 API Endpoints

## Analyze Stock

```http
POST /analyze
```

---

## Upload Annual Report

```http
POST /upload-report
```

---

## RAG QA

```http
GET /rag-qa
```

---

## Generate Executive Report

```http
POST /generate-report
```

---

# 📸 Screenshots

## 📊 AI Dashboard
- KPI dashboard
- AI score gauges
- Financial charts

## 🤖 Multi-Agent Workspace
- Bull vs Bear analysis
- Risk insights
- Research agent outputs

## 📄 Executive Reports
- AI-generated investment PDF reports

---

# 🔮 Future Enhancements

- Real-time financial news AI agent
- SEC filing monitoring
- Earnings call summarization
- Portfolio optimization AI
- Live stock sentiment tracking
- Azure Front Door deployment
- Authentication system
- User dashboard & history

---

# ☁️ Deployment

Planned production deployment stack:

- Azure App Service
- Azure Front Door
- Azure Blob Storage
- Azure AI Search
- Azure OpenAI

---

# 👨‍💻 Author

Shyam Kumar

Senior Software Engineer | Salesforce Developer | AI Engineer

---

# ⭐ Key Highlights

✅ Enterprise AI Architecture  
✅ Cloud-Native Design  
✅ Retrieval-Augmented Generation (RAG)  
✅ Multi-Agent AI System  
✅ Financial AI Copilot  
✅ Executive Report Automation  
✅ Azure AI Ecosystem Integration  

---

# 📜 License

This project is for educational and portfolio purposes.