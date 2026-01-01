"""Configuration models."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class SessionConfig(BaseModel):
    """Configuration for terminal session."""

    width: int = Field(default=120, ge=1, le=1000)
    height: int = Field(default=40, ge=1, le=1000)
    shell: str = Field(default="/bin/bash")
    environment: dict[str, str] = Field(default_factory=dict)
    socket_dir: Path = Field(default=Path("/tmp/terminal-state"))
