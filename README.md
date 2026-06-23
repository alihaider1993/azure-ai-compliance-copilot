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

# 🎯 Project Overview

The application performs end-to-end document review and compliance analysis using a multi-agent architecture powered by:

- Azure OpenAI GPT-4o
- Azure AI Document Intelligence
- Azure AI Search
- Azure Blob Storage
- Azure Cosmos DB (Serverless)
- Streamlit
- Managed Identity Authentication

The system provides:

✅ Compliance Findings

✅ Risk Assessment

✅ Recommendations

✅ Executive Summary

✅ Document Classification

✅ Confidence Scoring

✅ Document References

✅ Benchmark References

✅ Dashboard Analytics

✅ PDF/DOCX/Excel Report Export

---

# 📸 Application Features

## Executive Summary Dashboard

Displays:

- Compliance Score
- Risk Level
- Risk Score
- Document Type
- Findings Count

---

## Compliance Findings

Each finding contains:

- Category
- Severity
- Status
- Confidence Score
- Issue Description
- Evidence
- Uploaded Document Reference
- Benchmark Reference
- Review Status

---

## Recommendations

Automatically generates remediation recommendations with:

- Related Issue
- Recommendation
- Priority Level

---

## Dashboard Analytics

Interactive visualisations:

- Findings by Severity
- Findings by Status
- Findings by Category

---

## Export Reports

Generate reports in:

- PDF
- Microsoft Word (DOCX)
- Microsoft Excel (XLSX)

---

# 📄 Supported Documents

| Type | Supported |
|------|------------|
| PDF | ✅ |
| DOCX | ✅ |
| TXT | ✅ |
| XLSX | ✅ |
| XLS | ✅ |
| CSV | ✅ |
| PPTX | ✅ |
| PNG | ✅ |
| JPG | ✅ |
| JPEG | ✅ |

---

# 🏗️ Solution Architecture

```text
                     User Upload
                           │
                           ▼
                Streamlit Frontend
                           │
                           ▼
       ┌─────────────────────────────┐
       │ Agent 1                     │
       │ Document Processor          │
       └─────────────────────────────┘
                           │
                           ├── Upload File
                           │
                           ├── Azure Blob Storage
                           │
                           ├── Azure Document Intelligence
                           │
                           └── Cosmos DB Metadata Storage
                           │
                           ▼
       ┌─────────────────────────────┐
       │ Agent 2                     │
       │ Compliance Analyzer         │
       └─────────────────────────────┘
                           │
                           ├── Document Classification
                           ├── Generate Embeddings
                           ├── Azure AI Search Retrieval
                           ├── Benchmark Retrieval
                           └── GPT-4o Compliance Analysis
                           │
                           ▼
       ┌─────────────────────────────┐
       │ Agent 3                     │
       │ Risk Assessor               │
       └─────────────────────────────┘
                           │
                           ├── Risk Score
                           ├── Risk Level
                           ├── Compliance Score
                           ├── Severity Distribution
                           └── Dashboard Metrics
                           │
                           ▼
       ┌─────────────────────────────┐
       │ Agent 4                     │
       │ Recommendation Generator    │
       └─────────────────────────────┘
                           │
                           └── Remediation Recommendations
                           │
                           ▼
       ┌─────────────────────────────┐
       │ Agent 5                     │
       │ Report Generator            │
       └─────────────────────────────┘
                           │
                           ├── Cosmos DB Persistence
                           ├── Executive Summary
                           ├── Findings
                           ├── Recommendations
                           └── Export Reports
                           │
                           ▼
                  Streamlit Dashboard
```

---

# 🤖 Multi-Agent Architecture

## Agent 1 – Document Processor

Responsibilities:

- Generate document UUID
- Upload document to Blob Storage
- Extract text using Azure Document Intelligence
- Store metadata in Cosmos DB
- Return extracted data

Stores:

- document_id
- file_name
- blob_name
- blob_url
- page_count
- extraction_status
- created_at

---

## Agent 2 – Compliance Analyzer

Responsibilities:

- Infer document type
- Generate embeddings
- Retrieve benchmark content
- Perform evidence-based compliance analysis
- Generate findings

Outputs:

- category
- issue
- evidence
- uploaded_reference
- benchmark_reference
- status
- severity
- confidence_score
- review_status

Supported document types:

- Full Contract
- Master Service Agreement
- Supplier Agreement
- Purchase Order
- Quotation
- Commercial Proposal
- Invoice
- Delivery Note
- Receipt
- Tender Document
- Procurement Notice
- Policy
- SOP
- Handbook
- Privacy Notice
- Data Processing Agreement
- Spreadsheet
- Presentation
- Risk Assessment
- Audit Report
- Other

---

## Agent 3 – Risk Assessor

Calculates:

- Risk Score
- Risk Level
- Compliance Score
- Severity Distribution
- Category Distribution
- Status Distribution
- Red Flag Count

Risk Levels:

- Low
- Medium
- High
- Critical

Compliance Score:

```text
100 − (Risk Score × 10)
```

---

## Agent 4 – Recommendation Generator

Generates remediation actions:

```json
{
  "issue": "...",
  "recommendation": "...",
  "priority": "Low | Medium | High"
}
```

---

## Agent 5 – Report Generator

Creates final report:

```json
{
  "id": "...",
  "document_id": "...",
  "file_name": "...",
  "framework": "...",
  "document_type": "...",
  "created_at": "...",
  "executive_summary": {},
  "findings": [],
  "recommendations": []
}
```

Persists reports inside Cosmos DB.

---

# ☁️ Azure Architecture

## Azure OpenAI

Purpose:

- Compliance analysis
- Risk analysis
- Recommendations generation
- Document classification

Model:

- GPT-4o

Authentication:

- Managed Identity
- DefaultAzureCredential

---

## Azure AI Document Intelligence

Purpose:

- OCR
- Layout extraction
- Table extraction
- Page extraction

Model:

- prebuilt-layout

Authentication:

- Managed Identity

---

## Azure AI Search

Purpose:

- Vector search
- Benchmark retrieval
- RAG grounding
- Semantic search

Authentication:

- Managed Identity

---

## Azure Blob Storage

Purpose:

- Store uploaded documents
- Maintain document URLs
- Archive document reviews

Blob Naming Convention:

```text
reviews/{document_id}_{filename}
```

---

## Azure Cosmos DB (Serverless)

Database:

```text
compliance-db
```

Containers:

### documents

Stores:

- document_id
- file_name
- blob_url
- page_count
- upload_date
- extraction_status

### findings

Stores:

- finding_id
- document_id
- finding details
- confidence score
- references

### reviews

Stores:

- risk score
- risk level
- compliance score
- dashboard metrics

### reports

Stores:

- executive summary
- findings
- recommendations
- framework
- document type

---

# 🔒 Security

This solution uses:

- Managed Identity
- DefaultAzureCredential
- No hardcoded API keys
- Environment variable configuration
- Principle of least privilege

---

# 📊 Compliance Frameworks Supported

1. General Policy Review
2. UK GDPR
3. Information Security Policy
4. Supplier Contract Review
5. Health & Safety SOP

---

# 📂 Project Structure

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
└── data/
    ├── reports/
    └── sample_documents/
```

---

# 🚀 Local Setup

Clone repository:

```bash
git clone https://github.com/YOUR_USERNAME/azure-ai-compliance-copilot.git
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

# 🎬 Demo Workflow

Upload Document

↓

Run Compliance Review

↓

Executive Summary

↓

Red Flag Summary

↓

Compliance Findings

↓

Recommendations

↓

Dashboard Analytics

↓

PDF / DOCX / Excel Export

---

# 🧠 Skills Demonstrated

- Azure AI Engineering
- Generative AI Applications
- Retrieval-Augmented Generation (RAG)
- Document Intelligence
- Multi-Agent Architecture
- Vector Search
- Responsible AI Prompt Engineering
- Cloud Architecture
- Managed Identity Authentication
- Cosmos DB Design
- Streamlit Application Development
- Production-style Reporting Systems

---

# 👤 Author

