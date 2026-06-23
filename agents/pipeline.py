from agents.agent1_document_processor import process_document
from agents.agent2_compliance_analyzer import analyze_compliance
from agents.agent3_risk_assessor import assess_risk
from agents.agent4_recommendation_generator import (
    generate_recommendations,
)
from agents.agent5_report_generator import generate_report


def run_compliance_review(
    local_file_path: str,
    file_name: str,
    framework: str,
) -> dict:

    # Agent 1 - Extract document
    doc_result = process_document(
        local_file_path,
        file_name,
    )

    # Agent 2 - Compliance analysis
    analysis = analyze_compliance(
        document_id=doc_result["document_id"],
        extracted_data=doc_result["extracted_data"],
        framework=framework,
    )

    document_type = analysis.get(
        "document_type",
        "Unknown",
    )

    findings = analysis.get(
        "findings",
        [],
    )

    # Agent 3 - Risk assessment
    risk_result = assess_risk(
        document_id=doc_result["document_id"],
        findings=findings,
    )

    # Agent 4 - Recommendations
    recommendations_result = generate_recommendations(
        findings
    )

    recommendations = recommendations_result.get(
        "recommendations",
        [],
    )

    # Agent 5 - Final report
    report = generate_report(
        document_id=doc_result["document_id"],
        file_name=file_name,
        framework=framework,
        document_type=document_type,
        findings=findings,
        risk_result=risk_result,
        recommendations=recommendations,
    )

    return report