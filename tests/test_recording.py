# tests/test_recording.py
"""Tests for Recording model."""

from __future__ import annotations

import time

from terminal_state.capture import Frame, Recording


def test_recording_creation():
    """Test basic recording creation."""
    recording = Recording(width=80, height=24)
    assert recording.width == 80
    assert recording.height == 24
    assert len(recording.frames) == 0


def test_add_frame():
    """Test adding frames to recording."""
    recording = Recording()
    frame = Frame(
        content="test",
        width=80,
        height=24,
        timestamp=time.time(),
    )
    recording.add_frame(frame)
    assert len(recording.frames) == 1
    assert recording.width == 80
    assert recording.height == 24


def test_recording_duration():
    """Test duration calculation."""
    recording = Recording()
    start = time.time()

    frame1 = Frame(content="1", width=80, height=24, timestamp=start)
    frame2 = Frame(content="2", width=80, height=24, timestamp=start + 1.0)

    recording.add_frame(frame1)
    recording.add_frame(frame2)

    assert recording.duration >= 1.0


def test_export_methods_exist():
    """Test that export methods are available."""
    recording = Recording(width=80, height=24)
    frame = Frame(content="test", width=80, height=24, timestamp=time.time())
    recording.add_frame(frame)

    # Just verify methods exist - don't actually export
    assert hasattr(recording, "to_asciinema")
    assert hasattr(recording, "to_gif")
    assert hasattr(recording, "to_screenshot")
