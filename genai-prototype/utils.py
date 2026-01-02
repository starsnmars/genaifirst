"""Utility helpers for the project."""
from __future__ import annotations

import unicodedata


def clean_text(text: str | None) -> str:
    """Clean `text` by removing punctuation, lowercasing, and normalizing whitespace.

    - Returns an empty string for `None`.
    - Removes characters whose Unicode category starts with "P" (punctuation).
    - Converts to lowercase and collapses multiple whitespace characters to a single space.

    Examples
    --------
    >>> clean_text(" Hello, World! ")
    'hello world'
    """
    if text is None:
        return ""

    s = str(text)

    # Remove Unicode punctuation (any character in the "P*" categories).
    s = "".join(ch for ch in s if not unicodedata.category(ch).startswith("P"))

    # Lowercase and normalize whitespace
    s = s.lower()
    s = " ".join(s.split()).strip()

    return s


__all__ = ["clean_text"]
