# tests/test_config.py
"""Tests for configuration models."""

from __future__ import annotations

from pathlib import Path

from terminal_state.models import SessionConfig


def test_config_defaults():
    """Test default configuration values."""
    config = SessionConfig()
    assert config.width == 120
    assert config.height == 40
    assert config.shell == "/bin/bash"


def test_config_custom():
    """Test custom configuration."""
    config = SessionConfig(
        width=100,
        height=30,
        shell="/bin/zsh",
        socket_dir=Path("/tmp/custom"),
    )
    assert config.width == 100
    assert config.height == 30
    assert config.shell == "/bin/zsh"
    assert config.socket_dir == Path("/tmp/custom")
