import json
from urllib import response
from services.openai_service import chat_completion


SYSTEM_PROMPT = """
You are an expert Compliance Remediation Advisor.
Generate practical recommendations for each compliance finding.

Return ONLY valid JSON:
{
  "recommendations": [
    {
      "issue": "string",
      "recommendation": "string",
      "priority": "Low | Medium | High | Urgent"
    }
  ]
}
"""

def clean_json_response(response: str) -> str:
    response = response.strip()

    if response.startswith("```json"):
        response = response.replace("```json", "", 1)

    if response.startswith("```"):
        response = response.replace("```", "", 1)

    if response.endswith("```"):
        response = response[:-3]

    return response.strip()


def generate_recommendations(findings: list[dict]) -> dict:
    user_prompt = f"""
Findings:
{json.dumps(findings, indent=2)}

Generate clear, business-friendly remediation actions.
"""

    response = chat_completion(SYSTEM_PROMPT, user_prompt)

    try:
        return json.loads(clean_json_response(response))
    except json.JSONDecodeError:
        return {
            "recommendations": [
                {
                    "issue": "Parsing issue",
                    "recommendation": response,
                    "priority": "Medium",
                }
            ]
        }