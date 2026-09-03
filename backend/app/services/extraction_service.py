import json
from typing import Any

from app.services.llm_service import LLMService


class ExtractionService:
    """
    Extracts structured information from documents using an LLM.
    """

    def __init__(self):
        self.llm_service = LLMService()

    def extract(
        self,
        document_text: str,
        document_type: str,
    ) -> dict[str, Any]:

        if not document_text.strip():
            return {
                "success": False,
                "error": "Document contains no text.",
                "data": {},
            }

        system_prompt = """
You are an intelligent document information extraction system.

Your job is to extract useful structured information from
documents.

Rules:

1. Return ONLY valid JSON.
2. Do not return Markdown.
3. Do not invent information.
4. If information is missing, use null.
5. Preserve important values exactly when possible.
6. Use appropriate field names.
7. Extract only information actually present in the document.
"""

        user_prompt = f"""
Document type:
{document_type}

Extract structured information from the following document.

Return a JSON object.

For common document types, prefer useful fields such as:

Invoice:
- invoice_number
- invoice_date
- due_date
- seller
- buyer
- subtotal
- tax
- total
- currency
- items

Resume:
- name
- email
- phone
- location
- summary
- education
- experience
- skills
- certifications

Contract:
- parties
- effective_date
- expiration_date
- contract_value
- obligations
- termination_conditions

Receipt:
- merchant
- date
- items
- subtotal
- tax
- total
- payment_method

Research paper:
- title
- authors
- abstract
- keywords
- methodology
- findings
- conclusion

For other document types, determine appropriate fields yourself.

DOCUMENT:

{document_text}
"""

        try:
            response = self.llm_service.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )

            data = self._parse_json(response)

            return {
                "success": True,
                "data": data,
            }

        except Exception as error:
            return {
                "success": False,
                "error": str(error),
                "data": {},
            }

    def _parse_json(self, response: str) -> dict:
        """
        Convert the LLM response into a Python dictionary.
        """

        cleaned_response = response.strip()

        if cleaned_response.startswith("```"):
            cleaned_response = (
                cleaned_response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        parsed = json.loads(cleaned_response)

        if not isinstance(parsed, dict):
            raise ValueError(
                "LLM response must be a JSON object."
            )

        return parsed