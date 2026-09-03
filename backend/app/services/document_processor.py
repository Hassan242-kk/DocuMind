from pathlib import Path

import fitz
from docx import Document

from app.services.ocr_service import OCRService


class DocumentProcessor:
    """
    Handles extraction and preprocessing of documents.
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
        ".jpg",
        ".jpeg",
        ".png",
    }

    OCR_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
    }

    def __init__(self):
        self.ocr_service = OCRService()

    # --------------------------------------------------
    # Main extraction function
    # --------------------------------------------------

    def extract_text(self, file_path: str) -> str:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        extension = path.suffix.lower()

        if extension == ".pdf":
            return self._extract_from_pdf(path)

        if extension == ".docx":
            return self._extract_from_docx(path)

        if extension == ".txt":
            return self._extract_from_txt(path)

        if extension in self.OCR_EXTENSIONS:
            return self._extract_from_image(path)

        raise ValueError(
            f"Unsupported document type: {extension}"
        )

    # --------------------------------------------------
    # PDF extraction
    # --------------------------------------------------

    def _extract_from_pdf(self, path: Path) -> str:

        text_parts = []

        document = fitz.open(path)

        try:

            for page_number, page in enumerate(
                document,
                start=1
            ):

                page_text = page.get_text().strip()

                if page_text:

                    text_parts.append(
                        f"[Page {page_number}]\n"
                        f"{page_text}"
                    )

        finally:

            document.close()

        extracted_text = "\n\n".join(text_parts)

        # If almost no text was extracted,
        # the PDF may be scanned.
        if len(extracted_text.strip()) < 20:

            return self._extract_from_scanned_pdf(
                path
            )

        return extracted_text

    # --------------------------------------------------
    # Scanned PDF OCR
    # --------------------------------------------------

    def _extract_from_scanned_pdf(
        self,
        path: Path
    ) -> str:

        text_parts = []

        document = fitz.open(path)

        try:

            for page_number, page in enumerate(
                document,
                start=1
            ):

                # Render PDF page as image
                pixmap = page.get_pixmap(
                    matrix=fitz.Matrix(2, 2)
                )

                image_path = (
                    path.parent
                    / f"{path.stem}_page_{page_number}.png"
                )

                pixmap.save(
                    str(image_path)
                )

                try:

                    page_text = (
                        self.ocr_service
                        .extract_text_from_image(
                            str(image_path)
                        )
                    )

                    if page_text.strip():

                        text_parts.append(
                            f"[Page {page_number}]\n"
                            f"{page_text.strip()}"
                        )

                finally:

                    # Delete temporary image
                    if image_path.exists():
                        image_path.unlink()

        finally:

            document.close()

        return "\n\n".join(text_parts)

    # --------------------------------------------------
    # DOCX extraction
    # --------------------------------------------------

    def _extract_from_docx(
        self,
        path: Path
    ) -> str:

        document = Document(path)

        paragraphs = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n\n".join(paragraphs)

    # --------------------------------------------------
    # TXT extraction
    # --------------------------------------------------

    def _extract_from_txt(
        self,
        path: Path
    ) -> str:

        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    # --------------------------------------------------
    # Image OCR
    # --------------------------------------------------

    def _extract_from_image(
        self,
        path: Path
    ) -> str:

        return self.ocr_service.extract_text_from_image(
            str(path)
        )

    # --------------------------------------------------
    # Text cleaning
    # --------------------------------------------------

    def clean_text(
        self,
        text: str
    ) -> str:

        if not text:
            return ""

        text = text.replace(
            "\r\n",
            "\n"
        )

        text = text.replace(
            "\r",
            "\n"
        )

        lines = []

        for line in text.split("\n"):

            cleaned_line = " ".join(
                line.split()
            )

            if cleaned_line:
                lines.append(
                    cleaned_line
                )

        return "\n".join(lines)