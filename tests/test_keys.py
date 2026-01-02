# tests/test_keys.py
"""Tests for key sequence handling."""

from __future__ import annotations

import pytest

from terminal_state.input import KeySequence, Keys


def test_keysequence_literal():
    """Test literal key sequence."""
    seq = KeySequence(keys="hello", literal=True)
    assert seq.keys == "hello"
    assert seq.literal is True
    assert not seq.is_special


def test_keysequence_special():
    """Test special key detection."""
    seq = KeySequence(keys="C-c")
    assert seq.is_special


def test_keysequence_validation():
    """Test key sequence validation."""
    with pytest.raises(ValueError):
        KeySequence(keys="")


def test_predefined_keys():
    """Test predefined key constants."""
    assert Keys.ESCAPE.keys == "Escape"
    assert Keys.ENTER.keys == "Enter"
    assert Keys.CTRL_C.keys == "C-c"
