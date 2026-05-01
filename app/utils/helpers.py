"""
Utility / helper functions.
"""

import os
import re
from typing import List


def ensure_dir(path: str) -> str:
    """Create directory if it doesn't exist; return the path."""
    os.makedirs(path, exist_ok=True)
    return path


def clean_text(text: str) -> str:
    """Basic text cleaning: collapse whitespace, strip edges."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def list_files_in_dir(directory: str, extensions: List[str] = None) -> List[str]:
    """List all files in a directory, optionally filtered by extension."""
    files = []
    for fname in os.listdir(directory):
        fpath = os.path.join(directory, fname)
        if os.path.isfile(fpath):
            if extensions is None or os.path.splitext(fname)[1].lower() in extensions:
                files.append(fpath)
    return files
