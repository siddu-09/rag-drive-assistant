"""
Document parser – extracts text from PDF, DOCX, and TXT files.
"""

import os
from typing import Optional

import fitz  # PyMuPDF
from docx import Document


def extract_text(file_path: str) -> Optional[str]:
    """Extract text content from a file based on its extension."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _extract_pdf(file_path)
    elif ext in (".doc", ".docx"):
        return _extract_docx(file_path)
    elif ext == ".txt":
        return _extract_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def _extract_pdf(file_path: str) -> str:
    """Extract text from a PDF file using PyMuPDF."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def _extract_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def _extract_txt(file_path: str) -> str:
    """Extract text from a plain text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    
import fitz  # PyMuPDF

def parse_pdf(file_path):
    text = ""

    doc = fitz.open(file_path)

    for page in doc:
        text += page.get_text()

    return text
