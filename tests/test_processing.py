"""Tests for text processing (parsing and chunking)."""

from app.processing.chunking import chunk_text


def test_chunk_text_basic():
    text = "a" * 1000
    chunks = chunk_text(text, chunk_size=500, chunk_overlap=50)
    assert len(chunks) > 1
    assert len(chunks[0]) == 500


def test_chunk_text_empty():
    assert chunk_text("") == []


def test_chunk_text_short():
    text = "short text"
    chunks = chunk_text(text, chunk_size=500, chunk_overlap=50)
    assert len(chunks) == 1
    assert chunks[0] == text
