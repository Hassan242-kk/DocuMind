from pathlib import Path

from paddleocr import PaddleOCR


class OCRService:
    """
    Handles OCR operations for images and scanned documents.
    """

    def __init__(self):
        self.ocr = PaddleOCR(
            lang="en",
        )

    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from an image using PaddleOCR.
        """

        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        result = self.ocr.predict(
            str(path)
        )

        text_parts = []

        for page_result in result:

            if not hasattr(page_result, "json"):
                continue

            result_json = page_result.json

            if callable(result_json):
                result_json = result_json()

            if isinstance(result_json, dict):
                result_data = result_json.get("res", result_json)

                texts = result_data.get(
                    "rec_texts",
                    []
                )

                for text in texts:

                    if text and text.strip():
                        text_parts.append(
                            text.strip()
                        )

        return "\n".join(text_parts)
