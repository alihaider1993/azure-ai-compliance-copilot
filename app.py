import os
import tempfile

import pandas as pd
import plotly.express as px
import streamlit as st

from agents.pipeline import run_compliance_review
from utils.export_reports import (
    generate_pdf_report,
    generate_docx_report,
    generate_excel_report,
)


st.set_page_config(
    page_title="AI Compliance & Document Review Copilot",
    page_icon="📋",
    layout="wide",
)

st.title("📋 AI Compliance & Document Review Copilot")

st.markdown(
    """
Upload a policy, contract, SOP, handbook, spreadsheet, presentation, or image and receive:

✅ Compliance Findings  
✅ Risk Assessment  
✅ Recommendations  
✅ Executive Summary
"""
)

framework = st.selectbox(
    "Select Compliance Framework",
    [
        "General Policy Review",
        "UK GDPR",
        "Information Security Policy",
        "Supplier Contract Review",
        "Health & Safety SOP",
    ],
)

uploaded_file = st.file_uploader(
    "Upload Document",
    type=[
        "pdf",
        "docx",
        "txt",
        "xlsx",
        "xls",
        "csv",
        "pptx",
        "png",
        "jpg",
        "jpeg",
    ],
)

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

    file_size_mb = uploaded_file.size / (1024 * 1024)

    st.info(
        f"File Type: {uploaded_file.type or 'Unknown'} | "
        f"Size: {file_size_mb:.2f} MB"
    )

    if file_size_mb > 5:
        st.error("Please upload a document smaller than 5 MB.")
        st.stop()

    if st.button("Run Compliance Review", type="primary"):
        with st.spinner("Running multi-agent analysis..."):
            file_extension = os.path.splitext(uploaded_file.name)[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension,
            ) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name

            try:
                report = run_compliance_review(
                    local_file_path=temp_path,
                    file_name=uploaded_file.name,
                    framework=framework,
                )
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        st.success("Analysis Complete")

        summary = report.get("executive_summary", {})
        findings = report.get("findings", [])
        recommendations = report.get("recommendations", [])
        document_type = report.get(
            "document_type",
            summary.get("document_type", "Unknown"),
        )

        # -----------------------------
        # Export Report
        # -----------------------------
        st.markdown("## 📤 Export Report")

        try:
            pdf_bytes = generate_pdf_report(report)
            docx_bytes = generate_docx_report(report)
            excel_bytes = generate_excel_report(report)

            safe_file_name = os.path.splitext(uploaded_file.name)[0].replace(
                " ",
                "_",
            )

            col_pdf, col_docx, col_excel = st.columns(3)

            with col_pdf:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_bytes,
                    file_name=f"compliance_report_{safe_file_name}.pdf",
                    mime="application/pdf",
                )

            with col_docx:
                st.download_button(
                    label="⬇️ Download DOCX",
                    data=docx_bytes,
                    file_name=f"compliance_report_{safe_file_name}.docx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "wordprocessingml.document"
                    ),
                )

            with col_excel:
                st.download_button(
                    label="⬇️ Download Excel",
                    data=excel_bytes,
                    file_name=f"compliance_report_{safe_file_name}.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                )

        except Exception as export_error:
            st.warning(f"Report export failed: {export_error}")

        st.divider()

        # -----------------------------
        # Executive Summary
        # -----------------------------
        st.markdown("## Executive Summary")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                "Compliance Score",
                f'{summary.get("compliance_score", 0)}%',
            )

        with col2:
            st.metric(
                "Risk Level",
                summary.get("risk_level", "Unknown"),
            )

        with col3:
            st.metric(
                "Risk Score",
                summary.get("risk_score", 0),
            )

        with col4:
            st.metric(
                "Document Type",
                document_type,
            )

        with col5:
            st.metric(
                "Findings",
                summary.get("total_findings", len(findings)),
            )

        st.divider()

        # -----------------------------
        # Red Flag Summary
        # -----------------------------
        red_flags = [
            finding
            for finding in findings
            if finding.get("severity") in ["Critical", "High"]
        ]

        st.markdown("## 🚩 Red Flag Summary")

        if not red_flags:
            st.success("No Critical or High severity red flags identified.")
        else:
            st.error(f"{len(red_flags)} Critical/High red flag(s) identified.")

            for index, finding in enumerate(red_flags, start=1):
                st.markdown(
                    f"""
**{index}. {finding.get("category", "General")} — {finding.get("severity", "High")}**

{finding.get("issue", "N/A")}

**Reference:** {finding.get("page_reference", finding.get("uploaded_reference", "Uploaded document"))}
"""
                )

        st.divider()

        severity_icon = {
            "Critical": "🔴",
            "High": "🟠",
            "Medium": "🟡",
            "Low": "🟢",
        }

        status_icon = {
            "Missing": "🔴 Missing",
            "Partial": "🟡 Partial",
            "Requires Verification": "🔵 Requires Verification",
        }

        # -----------------------------
        # Findings First
        # -----------------------------
        st.markdown("## 🔍 Findings")
        st.caption(
            f"{len(findings)} finding(s) identified. Expand each item for details."
        )

        if not findings:
            st.success("No material findings identified.")
        else:
            for index, finding in enumerate(findings, start=1):
                category = finding.get("category", "General")
                severity = finding.get("severity", "Low")
                status = finding.get("status", "Requires Verification")

                try:
                    confidence = finding.get(
                        "confidence_percent",
                        int(float(finding.get("confidence_score", 0.75)) * 100),
                    )
                except Exception:
                    confidence = 75

                page_reference = finding.get(
                    "page_reference",
                    finding.get("uploaded_reference", "Uploaded document"),
                )

                expander_title = (
                    f"{severity_icon.get(severity, '⚪')} "
                    f"Finding {index}: {category} — {severity} "
                    f"({confidence}% confidence)"
                )

                with st.expander(expander_title, expanded=index == 1):
                    col_a, col_b, col_c = st.columns(3)

                    with col_a:
                        st.markdown("**Status**")
                        st.info(status_icon.get(status, status))

                    with col_b:
                        st.markdown("**Severity**")

                        if severity in ["Critical", "High"]:
                            st.error(severity)
                        elif severity == "Medium":
                            st.warning(severity)
                        else:
                            st.success(severity)

                    with col_c:
                        st.markdown("**Confidence**")
                        st.progress(confidence / 100)
                        st.caption(f"{confidence}%")

                    st.markdown("#### Issue")
                    st.write(finding.get("issue", "N/A"))

                    st.markdown("#### Evidence")
                    st.write(finding.get("evidence", "N/A"))

                    st.markdown("#### Uploaded Document Reference")
                    st.info(page_reference)

                    st.markdown("#### Benchmark / Reference")
                    st.caption(
                        finding.get(
                            "benchmark_reference",
                            "N/A",
                        )
                    )

                    st.markdown("#### Review Status")
                    st.write(finding.get("review_status", "Pending"))

        st.divider()

        # -----------------------------
        # Recommendations Second
        # -----------------------------
        st.markdown("## 💡 Recommendations")
        st.caption(
            f"{len(recommendations)} recommendation(s) generated."
        )

        if not recommendations:
            st.info("No recommendations were returned.")
        else:
            for index, recommendation in enumerate(
                recommendations,
                start=1,
            ):
                priority = recommendation.get("priority", "Medium")

                expander_title = (
                    f"💡 Recommendation {index}: "
                    f"{priority} Priority"
                )

                with st.expander(expander_title, expanded=index == 1):
                    st.markdown("#### Related Issue")
                    st.write(recommendation.get("issue", "N/A"))

                    st.markdown("#### Recommendation")
                    st.success(
                        recommendation.get(
                            "recommendation",
                            "N/A",
                        )
                    )

                    st.markdown("#### Priority")

                    if priority in ["Critical", "High", "Urgent"]:
                        st.error(priority)
                    elif priority == "Medium":
                        st.warning(priority)
                    else:
                        st.info(priority)

        st.divider()

        # -----------------------------
        # Dashboard After Findings/Recommendations
        # -----------------------------
        st.markdown("## 📊 Review Dashboard")

        if findings:
            findings_df = pd.DataFrame(findings)

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                if "severity" in findings_df.columns:
                    severity_counts = (
                        findings_df["severity"]
                        .value_counts()
                        .reset_index()
                    )
                    severity_counts.columns = ["Severity", "Count"]

                    fig = px.bar(
                        severity_counts,
                        x="Severity",
                        y="Count",
                        title="Findings by Severity",
                    )
                    st.plotly_chart(fig, use_container_width=True)

            with chart_col2:
                if "status" in findings_df.columns:
                    status_counts = (
                        findings_df["status"]
                        .value_counts()
                        .reset_index()
                    )
                    status_counts.columns = ["Status", "Count"]

                    fig = px.pie(
                        status_counts,
                        names="Status",
                        values="Count",
                        title="Findings by Status",
                    )
                    st.plotly_chart(fig, use_container_width=True)

            if "category" in findings_df.columns:
                category_counts = (
                    findings_df["category"]
                    .value_counts()
                    .reset_index()
                )
                category_counts.columns = ["Category", "Count"]

                fig = px.bar(
                    category_counts,
                    x="Category",
                    y="Count",
                    title="Findings by Category",
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No findings available for dashboard charts.")

        st.divider()

        with st.expander("🧾 View Raw JSON", expanded=False):
            st.json(report)

        st.caption(
            "⚠️ This review is AI-generated and intended to assist "
            "document analysis. It does not constitute legal or regulatory advice."
        )