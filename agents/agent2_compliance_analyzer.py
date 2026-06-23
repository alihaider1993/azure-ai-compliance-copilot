import json

from services.openai_service import (
    chat_completion,
    generate_embedding,
)
from services.search_service import vector_search
from services.cosmos_service import upsert_item


def clean_json_response(response: str) -> str:
    response = response.strip()

    if response.startswith("```json"):
        response = response.replace("```json", "", 1)

    if response.startswith("```"):
        response = response.replace("```", "", 1)

    if response.endswith("```"):
        response = response[:-3]

    return response.strip()


def infer_document_type(file_name: str, content: str) -> str:
    name = file_name.lower()
    text = content[:7000].lower()

    # Commercial / procurement documents
    if (
        "quotation" in name
        or "quote" in name
        or "quotation" in text[:1500]
        or "quote" in text[:1500]
    ):
        return "Quotation"

    if (
        "proposal" in name
        or "commercial proposal" in text
        or "technical proposal" in text
        or "financial proposal" in text
    ):
        return "Commercial Proposal"

    if (
        "purchase order" in name
        or name.startswith("po")
        or "purchase order" in text[:2000]
        or "po number" in text[:2000]
        or "po no" in text[:2000]
    ):
        return "Purchase Order"

    if (
        "invoice" in name
        or "tax invoice" in text[:2000]
        or "invoice number" in text[:2000]
        or "invoice no" in text[:2000]
    ):
        return "Invoice"

    if (
        "delivery challan" in name
        or "delivery note" in name
        or "delivery challan" in text[:2000]
        or "delivery note" in text[:2000]
    ):
        return "Delivery Note"

    if (
        "receipt" in name
        or "payment receipt" in text[:2000]
        or "receipt number" in text[:2000]
    ):
        return "Receipt"

    if (
        "tender" in name
        or "invitation to tender" in text
        or "request for tender" in text
        or "rfp" in name
        or "request for proposal" in text
        or "expression of interest" in text
        or "eoi" in name
    ):
        return "Tender Document"

    if (
        "procurement notice" in name
        or "contract notice" in text
        or "prior information notice" in text
    ):
        return "Procurement Notice"

    # Contract documents
    if (
        "front sheet" in name
        or "frontsheet" in name
        or "front sheet" in text[:2000]
        or "contract front sheet" in text[:2000]
    ):
        return "Front Sheet"

    if (
        "master service agreement" in name
        or "master services agreement" in name
        or "msa" in name
        or "master service agreement" in text
        or "master services agreement" in text
    ):
        return "Master Service Agreement"

    if (
        "service agreement" in name
        or "supplier agreement" in name
        or "services agreement" in name
        or "service agreement" in text[:3000]
        or "supplier agreement" in text[:3000]
    ):
        return "Supplier Agreement"

    if (
        "statement of work" in name
        or "sow" in name
        or "statement of work" in text[:3000]
    ):
        return "Statement of Work"

    if (
        "appendix" in name
        or "annex" in name
        or "annexure" in name
        or "appendix" in text[:2000]
        or "annex" in text[:2000]
    ):
        return "Appendix"

    if (
        "schedule" in name
        or "schedule" in text[:1500]
    ):
        return "Schedule"

    if (
        "contract" in name
        or "agreement" in name
        or "this agreement" in text[:3000]
        or "terms and conditions" in text[:3000]
    ):
        return "Full Contract"

    # Privacy / data protection
    if (
        "privacy notice" in name
        or "privacy policy" in name
        or "privacy notice" in text[:3000]
        or "privacy policy" in text[:3000]
    ):
        return "Privacy Notice"

    if (
        "data processing agreement" in name
        or "dpa" in name
        or "data processing agreement" in text
        or "controller" in text[:3000]
        and "processor" in text[:3000]
    ):
        return "Data Processing Agreement"

    if (
        "data protection impact assessment" in name
        or "dpia" in name
        or "data protection impact assessment" in text
    ):
        return "DPIA"

    # Policies / governance
    if (
        "code of conduct" in name
        or "supplier code" in name
        or "code of conduct" in text
        or "supplier code" in text
    ):
        return "Policy"

    if (
        "policy" in name
        or "policy" in text[:2000]
    ):
        return "Policy"

    if (
        "standard operating procedure" in name
        or "sop" in name
        or "procedure" in name
        or "standard operating procedure" in text[:3000]
        or "procedure" in text[:2000]
    ):
        return "SOP"

    if (
        "handbook" in name
        or "handbook" in text[:2000]
        or "employee handbook" in text
    ):
        return "Handbook"

    if (
        "risk assessment" in name
        or "risk assessment" in text[:3000]
    ):
        return "Risk Assessment"

    if (
        "audit report" in name
        or "audit report" in text[:3000]
    ):
        return "Audit Report"

    if (
        "minutes" in name
        or "meeting minutes" in text[:2000]
    ):
        return "Meeting Minutes"

    # File-type based fallback
    if name.endswith((".xlsx", ".xls", ".csv")):
        return "Spreadsheet"

    if name.endswith(".pptx"):
        return "Presentation"

    if name.endswith((".png", ".jpg", ".jpeg")):
        return "Image Document"

    return "Other"


SYSTEM_PROMPT = """
You are an expert UK Compliance, Contract Review, Procurement, Data Protection, Information Security, Governance, Risk Management and Policy Review Analyst.

Use three sources of knowledge:

1. Retrieved benchmark documents.
2. General UK legal and regulatory knowledge.
3. Your expert reasoning and industry best practices.

The benchmark documents are guidance and examples. They are NOT the sole source of truth.

Identify only genuine and material:

- compliance gaps
- contractual risks
- governance weaknesses
- information security weaknesses
- privacy risks
- unclear responsibilities
- missing mandatory controls
- operational risks

Avoid speculative findings.

Do not generate findings merely because a clause is commonly seen in contracts.

Do not report drafting preferences as compliance failures.

A document may still be compliant even if it does not contain every clause found in benchmark documents.

Determine the document type first and tailor the review.

Possible types:

- Full Contract
- Master Service Agreement
- Supplier Agreement
- Purchase Order
- Quotation
- Commercial Proposal
- Invoice
- Delivery Note
- Receipt
- Front Sheet
- Schedule
- Appendix
- Statement of Work
- Tender Document
- Procurement Notice
- Policy
- SOP
- Handbook
- Privacy Notice
- Data Processing Agreement
- DPIA
- Spreadsheet
- Presentation
- Form
- Image Document
- Website Notice
- Risk Assessment
- Audit Report
- Meeting Minutes
- Other

Missing =
Clear evidence shows that a mandatory requirement is absent and the omission creates genuine material risk.

Partial =
The requirement exists but is incomplete, ambiguous, weak, or poorly defined.

Requires Verification =
The requirement is not visible in the uploaded document but may reasonably exist elsewhere in the wider agreement or document set.

Purchase Orders, Quotations, Invoices, Delivery Notes and Receipts are short-form transactional or commercial documents.
Do not expect them to contain full contract clauses.
Prefer Requires Verification + Low severity unless immediate material risk exists.

Quotations are commercial offer documents.
Assess pricing clarity, validity period, scope, payment terms, tax treatment, delivery terms, exclusions, acceptance terms, responsibilities, warranties and material commercial risks.
Do not penalise missing full contract clauses unless the quotation claims to be the complete standalone agreement.

Front Sheets are partial documents.
Do not treat them as full contracts.

Tender Documents are procurement instruments.
Do not expect final contract clauses.

Privacy Notices may rely on wider privacy documentation.
Group related transparency findings.

Return ONLY valid JSON.

Required JSON format:

{
  "document_type": "string",
  "findings": [
    {
      "category": "string",
      "issue": "string",
      "evidence": "string",
      "uploaded_reference": "Uploaded document page or section",
      "page_reference": "Uploaded document page or section",
      "benchmark_reference": "Benchmark file/page/article or General UK compliance best practice",
      "status": "Missing | Partial | Requires Verification",
      "severity": "Low | Medium | High | Critical",
      "confidence_score": 0.0,
      "review_status": "Pending"
    }
  ]
}
"""


def build_benchmark_context(benchmark_results: list[dict]) -> str:
    context_blocks = []

    for item in benchmark_results:
        file_name = item.get("file_name", "Unknown")
        page_number = item.get("page_number", "N/A")
        framework = item.get("framework", "General")
        chunk_text = item.get("chunk_text", "")

        context_blocks.append(
            f"Source File: {file_name}\n"
            f"Page: {page_number}\n"
            f"Framework: {framework}\n"
            f"Content:\n{chunk_text}"
        )

    return "\n\n---\n\n".join(context_blocks)


def normalize_findings(result: dict) -> dict:
    findings = result.get("findings", [])

    for finding in findings:
        finding.setdefault("category", "General")
        finding.setdefault("issue", "N/A")
        finding.setdefault("evidence", "N/A")
        finding.setdefault("status", "Requires Verification")
        finding.setdefault("severity", "Low")

        finding.setdefault("uploaded_reference", "Uploaded document")
        finding.setdefault(
            "page_reference",
            finding.get("uploaded_reference", "Uploaded document"),
        )

        finding.setdefault(
            "benchmark_reference",
            "General UK compliance best practice",
        )

        finding.setdefault("confidence_score", 0.75)
        finding.setdefault("review_status", "Pending")

        try:
            confidence = float(finding["confidence_score"])
        except Exception:
            confidence = 0.75

        if confidence > 1:
            confidence = confidence / 100

        confidence = max(0, min(confidence, 1))

        finding["confidence_score"] = round(confidence, 2)
        finding["confidence_percent"] = int(confidence * 100)

    result["findings"] = findings
    return result


def analyze_compliance(
    document_id: str,
    extracted_data: dict,
    framework: str,
) -> dict:

    content = extracted_data.get("content", "")
    file_name = extracted_data.get("file_name", "")

    inferred_document_type = infer_document_type(
        file_name=file_name,
        content=content,
    )

    query_text = f"""
Framework:
{framework}

Document Type:
{inferred_document_type}

Document:
{content[:5000]}
"""

    query_vector = generate_embedding(query_text)

    benchmark_results = vector_search(
        query_vector,
        top=7,
    )

    benchmark_context = build_benchmark_context(
        benchmark_results,
    )

    user_prompt = f"""
Compliance Framework:
{framework}

Detected Document Type:
{inferred_document_type}

Uploaded File Name:
{file_name}

Uploaded Document Text:
{content[:50000]}

Retrieved Benchmark Context:
{benchmark_context}

Task:
Review the uploaded document using the retrieved benchmark context, general UK compliance knowledge, and expert reasoning.

Document classification instruction:
Use the detected document type unless the uploaded document text clearly proves a better type. If you change the type, still keep it within the allowed document types listed in the system prompt.

For every finding:
- cite evidence from the uploaded document
- include uploaded_reference such as "Uploaded document, page 2" if available
- include page_reference with the same or clearer page/section reference
- cite benchmark_reference using retrieved source file/page where relevant
- include confidence_score between 0.00 and 1.00
- set review_status to "Pending"

Only return material, evidence-based findings.

Return JSON only.
"""

    response = chat_completion(
        SYSTEM_PROMPT,
        user_prompt,
    )

    try:
        result = json.loads(
            clean_json_response(response),
        )

    except json.JSONDecodeError:
        result = {
            "document_type": inferred_document_type,
            "findings": [
                {
                    "category": "Parsing",
                    "issue": "Model response could not be parsed as JSON.",
                    "evidence": response,
                    "uploaded_reference": "N/A",
                    "page_reference": "N/A",
                    "benchmark_reference": "N/A",
                    "status": "Partial",
                    "severity": "Medium",
                    "confidence_score": 0.1,
                    "review_status": "Pending",
                }
            ],
        }

    result["document_type"] = result.get(
        "document_type",
        inferred_document_type,
    )

    if result["document_type"] == "Other":
        result["document_type"] = inferred_document_type

    result = normalize_findings(result)

    for index, finding in enumerate(
        result.get("findings", []),
        start=1,
    ):
        finding_record = {
            "id": f"{document_id}_finding_{index}",
            "document_id": document_id,
            **finding,
        }

        upsert_item(
            "findings",
            finding_record,
        )

    return result