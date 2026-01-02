# tests/test_session.py
"""Tests for TerminalSession requiring tmux."""

from __future__ import annotations

import shutil
import time

import pytest

from terminal_state import TerminalSession
from terminal_state.input import Keys

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


def test_session_creation(session):
    """Test basic session creation."""
    assert session._started is True
    assert session.config.width == 80
    assert session.config.height == 24


def test_send_command(session):
    """Test sending a command."""
    session.send_command("echo 'hello world'")
    time.sleep(0.2)

    frame = session.capture()
    assert "hello world" in frame.content


def test_capture_frame(session):
    """Test frame capture."""
    session.send_command("pwd")
    time.sleep(0.1)

    frame = session.capture()
    assert frame.width == 80
    assert frame.height == 24
    assert len(frame.content) > 0


def test_expect_text(session):
    """Test waiting for text to appear."""
    session.send_command("echo 'specific marker text'")
    found = session.expect_text("specific marker text", timeout=2.0)
    assert found is True


def test_expect_text_timeout(session):
    """Test expect_text timeout."""
    found = session.expect_text("text that will never appear", timeout=0.5)
    assert found is False


def test_recording_captures_frames(session):
    """Test that recording captures frames."""
    session.send_command("echo 'frame 1'")
    session.send_command("echo 'frame 2'")

    assert len(session.recording.frames) >= 2


def test_send_keys_literal(session):
    """Test sending literal text."""
    session.send_keys("literal text", record=False)
    session.send_keys(Keys.ENTER, record=True)
    time.sleep(0.1)

    frame = session.capture()
    assert "literal text" in frame.content


def test_send_keys_special(session):
    """Test sending special keys."""
    session.send_command("cat > /tmp/test_file.txt")
    session.send_keys("test content")
    session.send_keys(Keys.ENTER)
    session.send_keys(Keys.CTRL_D, record=False)  # EOF
    time.sleep(0.2)

    session.send_command("cat /tmp/test_file.txt")
    assert session.expect_text("test content", timeout=2.0)


def test_context_manager():
    """Test context manager interface."""
    with TerminalSession.create(width=80, height=24) as sess:
        sess.send_command("echo 'context test'")
        assert sess._started is True

    # Should be destroyed after context exit
    assert sess._started is False


def test_multiple_commands(session):
    """Test executing multiple commands."""
    commands = [
        "echo 'command 1'",
        "echo 'command 2'",
        "echo 'command 3'",
    ]

    for cmd in commands:
        session.send_command(cmd)

    time.sleep(0.2)
    frame = session.capture()

    assert "command 1" in frame.content
    assert "command 2" in frame.content
    assert "command 3" in frame.content
