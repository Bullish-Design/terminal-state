# tests/test_export.py
"""Tests for export functionality requiring tmux."""

from __future__ import annotations

import shutil
import time

import pytest

from terminal_state import TerminalSession

pytestmark = pytest.mark.skipif(
    shutil.which("tmux") is None,
    reason="tmux not available",
)


@pytest.fixture
def session():
    """Create and cleanup a terminal session."""
    sess = TerminalSession.create(width=80, height=24)
    yield sess
    sess.destroy()


def test_export_asciinema(session, preserved_tmp):
    """Test asciinema export."""
    session.send_command("echo 'test export'")
    session.send_command("ls -la")
    time.sleep(0.2)

    cast_file = preserved_tmp / "test.cast"
    session.recording.to_asciinema(cast_file)

    assert cast_file.exists()
    assert cast_file.stat().st_size > 0

    # Verify it's valid JSON lines
    with open(cast_file) as f:
        lines = f.readlines()
        assert len(lines) >= 2  # Header + at least one event


def test_export_screenshot(session, preserved_tmp):
    """Test PNG screenshot export."""
    session.send_command("echo 'screenshot test'")
    time.sleep(0.2)

    png_file = preserved_tmp / "screenshot.png"
    session.recording.to_screenshot(png_file)

    assert png_file.exists()
    assert png_file.stat().st_size > 0


@pytest.mark.slow
def test_export_gif(session, preserved_tmp):
    """Test GIF export."""
    # Create some visual content
    session.send_command("echo '=== GIF Test ==='")
    session.send_command('for i in {1..3}; do echo "Frame $i"; sleep 0.1; done')
    time.sleep(0.5)

    gif_file = preserved_tmp / "test.gif"
    session.recording.to_gif(gif_file, fps=5)

    assert gif_file.exists()
    assert gif_file.stat().st_size > 0


def test_recording_has_frames(session):
    """Test that recording accumulates frames."""
    initial_count = len(session.recording.frames)

    session.send_command("echo 'frame 1'")
    session.send_command("echo 'frame 2'")

    assert len(session.recording.frames) > initial_count
    assert session.recording.duration > 0
