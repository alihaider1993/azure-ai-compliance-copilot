# 📋 AI Compliance & Document Review Copilot

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4o-0078D4?logo=microsoft-azure)
![Azure Document Intelligence](https://img.shields.io/badge/Document%20Intelligence-Azure-0078D4?logo=microsoft-azure)
![Azure Cosmos DB](https://img.shields.io/badge/Cosmos%20DB-Serverless-0078D4?logo=microsoft-azure)
![Azure AI Search](https://img.shields.io/badge/Azure%20AI%20Search-RAG-0078D4?logo=microsoft-azure)
![Blob Storage](https://img.shields.io/badge/Azure%20Blob%20Storage-0078D4?logo=microsoft-azure)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit)
![Managed Identity](https://img.shields.io/badge/Auth-Managed%20Identity-0078D4?logo=microsoft-azure)
![License](https://img.shields.io/badge/License-MIT-green)

Enterprise-style multi-agent AI Compliance & Document Review Copilot built using Azure AI services. The platform enables users to upload policies, contracts, quotations, SOPs, handbooks, spreadsheets, presentations, and images and receive evidence-based compliance findings, risk assessments, recommendations, and downloadable reports.

---

## 🎯 Project Overview

Many organisations still rely on manual reviews of contracts, policies, procurement documents, and privacy notices. These reviews can be time-consuming, inconsistent, and heavily dependent on individual expertise.

This project demonstrates how Azure AI and Generative AI can accelerate document reviews by combining:

* Multi-Agent Architecture
* Retrieval-Augmented Generation (RAG)
* Document Intelligence and OCR
* Vector Search
* Evidence-Based Compliance Analysis
* Risk Assessment and Recommendations
* Enterprise Security using Managed Identity

The objective is not to replace legal, procurement, or compliance professionals but to build an AI copilot that assists subject matter experts by surfacing potential risks and supporting faster, more consistent decision-making.

---

## ✨ Key Features

✅ Compliance Findings

✅ Risk Assessment

✅ Recommendations

✅ Executive Summary

✅ Document Classification

✅ Confidence Scoring

✅ Uploaded Document References

✅ Benchmark References

✅ Interactive Dashboard Analytics

✅ PDF / DOCX / Excel Export

✅ Managed Identity Authentication

---


## 📸 Application Screenshots

➡️ [View Screenshot Gallery](./docs/screenshots/README.md)

🎥 Loom Demo:

(Add your Loom link here)

---

## 📄 Supported Documents

| Type | Supported |
| ---- | --------- |
| PDF  | ✅         |
| DOCX | ✅         |
| TXT  | ✅         |
| XLSX | ✅         |
| XLS  | ✅         |
| CSV  | ✅         |
| PPTX | ✅         |
| PNG  | ✅         |
| JPG  | ✅         |
| JPEG | ✅         |

---

## 🏗️ Solution Architecture

![Architecture](https://github.com/alihaider1993/azure-ai-compliance-copilot/blob/main/docs/screenshots/architecture.png)

---

## 🤖 Multi-Agent Workflow

| Agent   | Responsibility                                                                           |
| ------- | ---------------------------------------------------------------------------------------- |
| Agent 1 | Document ingestion, Blob upload, OCR extraction, metadata persistence                    |
| Agent 2 | Document classification, embeddings generation, benchmark retrieval, compliance analysis |
| Agent 3 | Risk scoring, compliance scoring, dashboard metrics                                      |
| Agent 4 | Remediation recommendation generation                                                    |
| Agent 5 | Executive summary creation, report generation, Cosmos DB persistence                     |

---

## ☁️ Azure Services Used

### Azure OpenAI (GPT-4o)

Purpose:

* Compliance analysis
* Risk assessment
* Recommendation generation
* Document classification

---

### Azure AI Document Intelligence

Purpose:

* OCR extraction
* Layout extraction
* Table extraction
* Page extraction

Model:

* prebuilt-layout

---

### Azure AI Search

Purpose:

* Vector search
* Benchmark retrieval
* Retrieval-Augmented Generation (RAG)
* Semantic search

---

### Azure Blob Storage

Purpose:

* Store uploaded documents
* Archive reviews
* Maintain document URLs

---

### Azure Cosmos DB (Serverless)

Database:

```text
compliance-db
```

Containers:

* documents
* findings
* reviews
* reports

---

### Authentication

* Managed Identity
* DefaultAzureCredential
* No hardcoded secrets
* Principle of Least Privilege

---

## 📊 Compliance Frameworks Supported

1. General Policy Review
2. UK GDPR
3. Information Security Policy
4. Supplier Contract Review
5. Health & Safety SOP

---

## 📂 Project Structure

```text
azure-ai-compliance-copilot/
│
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── agents/
│   ├── agent1_document_processor.py
│   ├── agent2_compliance_analyzer.py
│   ├── agent3_risk_assessor.py
│   ├── agent4_recommendation_generator.py
│   ├── agent5_report_generator.py
│   └── pipeline.py
│
├── services/
│   ├── blob_service.py
│   ├── cosmos_service.py
│   ├── document_intelligence_service.py
│   ├── openai_service.py
│   ├── search_service.py
│   └── storage_service.py
│
├── utils/
│   ├── export_reports.py
│   ├── chunking.py
│   └── config.py
│
├── benchmark/
│
├── scripts/
│   ├── create_search_index.py
│   └── ingest_benchmark_documents.py
│
├── docs/
│   ├── architecture.png
│   └── screenshots/
│
└── data/
    ├── reports/
    └── sample_documents/
```

---

## 🚀 Local Setup

Clone repository:

```bash
git clone https://github.com/alihaider1993/azure-ai-compliance-copilot.git
cd azure-ai-compliance-copilot
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate environment:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment file:

```bash
copy .env.example .env
```

Populate Azure resource values.

Run application:

```bash
streamlit run app.py
```

---

## 🎬 Demo Workflow

```text
Upload Document
        ↓
Run Compliance Review
        ↓
Executive Summary
        ↓
Compliance Findings
        ↓
Recommendations
        ↓
Dashboard Analytics
        ↓
PDF / DOCX / Excel Export
```

---

## 🧠 Skills Demonstrated

* Azure AI Engineering
* Generative AI Applications
* Retrieval-Augmented Generation (RAG)
* Document Intelligence
* Multi-Agent Architecture
* Vector Search
* Responsible AI Prompt Engineering
* Cloud Architecture
* Managed Identity Authentication
* Cosmos DB Design
* Streamlit Application Development
* Production-Style Reporting Systems

---

## 👨‍💻 About Me

**Syed Ali Haider**

I am transitioning into AI roles and built this project to demonstrate real-world AI engineering capabilities, including cloud architecture, prompt engineering, RAG, document intelligence, multi-agent orchestration, and enterprise security practices.

[LinkedIn](https://www.linkedin.com/in/syed-ali-haider-43777821) · 
[GitHub](https://github.com/alihaider1993) · 


---

## ⚠️ Disclaimer

This project is a portfolio demonstration of an AI-powered compliance copilot. Findings generated by the system are intended to assist document reviews and should be validated by legal, procurement, or compliance professionals before any decisions are made.


---

