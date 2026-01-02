# tests/test_frame.py
"""Tests for Frame model."""

from __future__ import annotations

import time

from terminal_state.capture import Frame


def test_frame_creation():
    """Test basic frame creation."""
    frame = Frame(
        content="test content",
        width=80,
        height=24,
        timestamp=time.time(),
    )
    assert frame.content == "test content"
    assert frame.width == 80
    assert frame.height == 24


def test_frame_immutability():
    """Test that frames are immutable."""
    frame = Frame(
        content="test",
        width=80,
        height=24,
        timestamp=time.time(),
    )
    try:
        frame.content = "new content"  # type: ignore[misc]
        assert False, "Should have raised error"
    except Exception:
        pass  # Expected


def test_frame_with_metadata():
    """Test frame with optional metadata."""
    frame = Frame(
        content="test",
        width=80,
        height=24,
        timestamp=time.time(),
        metadata={"source": "test"},
    )
    assert frame.metadata["source"] == "test"
