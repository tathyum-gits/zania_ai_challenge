import pdfplumber
import re
import os
import logging
from typing import Optional

class PDFParser:
    """A class for extracting and cleaning text from PDF files."""

    def __init__(self, file_path: str):
        """
        Initialize the PDFParser with a file path.
        
        Args:
            file_path (str): The path to the PDF file.
        """
        self.file_path = file_path

    def extract_text(self) -> Optional[str]:
        """
        Extracts text from all pages of the PDF file.

        Returns:
            Optional[str]: The extracted text from the PDF, or None if an error occurs.
        """
        if not self._is_valid_pdf():
            logging.error("Invalid PDF file: %s", self.file_path)
            return None

        text_content = []
        
        try:
            with pdfplumber.open(self.file_path) as pdf:
                logging.info("Opened PDF file: %s", self.file_path)
                for page_number, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                    else:
                        logging.warning("No text found on page %d", page_number + 1)
        except Exception as e:
            logging.exception("Error reading PDF file: %s", e)
            return None

        logging.info("Successfully extracted text from PDF")
        return "\n".join(text_content)

    def clean_text(self, text: str) -> str:
        """
        Cleans extracted text by removing excessive whitespace.

        Args:
            text (str): The raw text to be cleaned.

        Returns:
            str: The cleaned text.
        """
        cleaned_text = re.sub(r'\s+', ' ', text)
        return cleaned_text.strip()

    def parse(self) -> Optional[str]:
        """
        Parses the PDF file, extracting and cleaning the text.

        Returns:
            Optional[str]: The cleaned text, or None if extraction fails.
        """
        raw_text = self.extract_text()
        if raw_text is None:
            logging.error("Failed to extract text from PDF: %s", self.file_path)
            return None

        cleaned_text = self.clean_text(raw_text)
        logging.info("Text cleaned and parsing complete")
        return cleaned_text

    def _is_valid_pdf(self) -> bool:
        """
        Validates that the file exists and is a PDF file.

        Returns:
            bool: True if the file exists and is a PDF, otherwise False.
        """
        is_pdf = os.path.isfile(self.file_path) and self.file_path.lower().endswith(".pdf")
        if not is_pdf:
            logging.error("Provided file path is not a valid PDF: %s", self.file_path)
        return is_pdf
