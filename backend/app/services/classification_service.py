from typing import Dict


class ClassificationService:
    """
    Classifies documents based on their extracted text.

    This first version uses lightweight rule-based classification.
    Later, we can replace or enhance it with an LLM/Transformer model.
    """

    DOCUMENT_KEYWORDS: Dict[str, list[str]] = {
        "invoice": [
            "invoice",
            "invoice number",
            "invoice no",
            "total amount",
            "subtotal",
            "tax",
            "billing",
            "bill to",
        ],
        "resume": [
            "resume",
            "curriculum vitae",
            "cv",
            "work experience",
            "education",
            "skills",
            "professional experience",
        ],
        "contract": [
            "agreement",
            "contract",
            "party",
            "terms and conditions",
            "hereby",
            "effective date",
            "termination",
        ],
        "report": [
            "report",
            "executive summary",
            "introduction",
            "findings",
            "conclusion",
            "recommendations",
        ],
        "receipt": [
            "receipt",
            "cashier",
            "subtotal",
            "change",
            "payment method",
            "amount paid",
        ],
        "research_paper": [
            "abstract",
            "methodology",
            "literature review",
            "references",
            "results",
            "discussion",
        ],
    }

    def classify(self, text: str) -> dict:
        """
        Classify a document using keyword matching.
        """

        if not text or not text.strip():
            return {
                "document_type": "unknown",
                "confidence": 0.0,
            }

        normalized_text = text.lower()

        scores = {}

        for document_type, keywords in self.DOCUMENT_KEYWORDS.items():

            score = 0

            for keyword in keywords:
                if keyword in normalized_text:
                    score += 1

            scores[document_type] = score

        best_type = max(
            scores,
            key=scores.get
        )

        best_score = scores[best_type]

        if best_score == 0:
            return {
                "document_type": "unknown",
                "confidence": 0.0,
            }

        total_keywords = len(
            self.DOCUMENT_KEYWORDS[best_type]
        )

        confidence = min(
            best_score / total_keywords,
            1.0
        )

        return {
            "document_type": best_type,
            "confidence": round(confidence, 2),
        }