import pytest

from utils import clean_text


def test_basic_cleaning():
    assert clean_text(" Hello, World! ") == "hello world"


def test_apostrophe_and_period():
    assert clean_text("It's 2026.") == "its 2026"


def test_unicode_punctuation():
    assert clean_text("Café—moi!") == "café moi"


def test_whitespace_normalization():
    assert clean_text("  multiple   spaces\tand\nnewlines ") == "multiple spaces and newlines"


def test_empty_and_none():
    assert clean_text("") == ""
    assert clean_text(None) == ""
