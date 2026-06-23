from datetime import datetime, UTC
from services.cosmos_service import upsert_item


def generate_report(
    document_id: str,
    file_name: str,
    framework: str,
    document_type: str,
    findings: list[dict],
    risk_result: dict,
    recommendations: list[dict],
) -> dict:

    report = {
        "id": f"{document_id}_report",
        "document_id": document_id,
        "file_name": file_name,
        "framework": framework,
        "document_type": document_type,
        "created_at": datetime.now(
            UTC
        ).isoformat(),
        "executive_summary": {
            "risk_level": risk_result.get(
                "risk_level"
            ),
            "risk_score": risk_result.get(
                "risk_score"
            ),
            "compliance_score": risk_result.get(
                "compliance_score"
            ),
            "total_findings": len(
                findings
            ),
            "document_type": document_type,
        },
        "findings": findings,
        "recommendations": recommendations,
    }

    upsert_item(
        "reports",
        report,
    )

    return report