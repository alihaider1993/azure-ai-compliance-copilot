from services.cosmos_service import upsert_item


SEVERITY_SCORES = {
    "Low": 2,
    "Medium": 5,
    "High": 8,
    "Critical": 10,
}


def calculate_distribution(findings: list[dict], field_name: str) -> dict:
    distribution = {}

    for finding in findings:
        value = finding.get(field_name, "Unknown")
        distribution[value] = distribution.get(value, 0) + 1

    return distribution


def assess_risk(document_id: str, findings: list[dict]) -> dict:
    if not findings:
        risk_score = 0
    else:
        scores = [
            SEVERITY_SCORES.get(
                finding.get("severity", "Medium"),
                5,
            )
            for finding in findings
        ]

        risk_score = round(
            sum(scores) / len(scores),
            2,
        )

    if risk_score >= 9:
        risk_level = "Critical"
    elif risk_score >= 7:
        risk_level = "High"
    elif risk_score >= 4:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    compliance_score = max(
        0,
        round(
            100 - (risk_score * 10),
            2,
        ),
    )

    severity_distribution = calculate_distribution(
        findings,
        "severity",
    )

    status_distribution = calculate_distribution(
        findings,
        "status",
    )

    category_distribution = calculate_distribution(
        findings,
        "category",
    )

    critical_findings = [
        finding
        for finding in findings
        if finding.get("severity") == "Critical"
    ]

    high_findings = [
        finding
        for finding in findings
        if finding.get("severity") == "High"
    ]

    red_flags = critical_findings + high_findings

    risk_record = {
        "id": f"{document_id}_risk_review",
        "review_id": f"{document_id}_risk_review",
        "document_id": document_id,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "compliance_score": compliance_score,
        "finding_count": len(findings),
        "severity_distribution": severity_distribution,
        "status_distribution": status_distribution,
        "category_distribution": category_distribution,
        "red_flag_count": len(red_flags),
    }

    upsert_item(
        "reviews",
        risk_record,
    )

    return risk_record