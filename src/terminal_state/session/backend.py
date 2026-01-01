"""Tmux backend for terminal session management."""

from __future__ import annotations

import time
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

from libtmux import Server
from libtmux.session import Session as TmuxSession

from terminal_state.capture.frame import Frame
from terminal_state.input.keys import KeySequence

if TYPE_CHECKING:
    from terminal_state.models.config import SessionConfig


class TmuxBackend:
    """Tmux-based terminal backend."""

    def __init__(self, config: SessionConfig) -> None:
        self.config = config
        self.session_id = f"terminal-state-{uuid.uuid4().hex[:8]}"
        self.socket_path = config.socket_dir / f"{self.session_id}.sock"
        self.server: Server | None = None
        self.session: TmuxSession | None = None

    def create(self) -> None:
        """Create new tmux session."""
        self.config.socket_dir.mkdir(parents=True, exist_ok=True)

        self.server = Server(socket_path=str(self.socket_path))
        self.session = self.server.new_session(
            session_name=self.session_id,
            x=self.config.width,
            y=self.config.height,
            attach=False,
        )

    def send_keys(self, keys: KeySequence) -> None:
        """Send keys to terminal."""
        if not self.session:
            raise RuntimeError("Session not created")

        pane = self.session.active_pane
        if pane is None:
            raise RuntimeError("No active pane in session")

        pane.send_keys(keys.keys, literal=keys.literal, suppress_history=False)

    def capture(self) -> Frame:
        """Capture current pane content."""
        if not self.session:
            raise RuntimeError("Session not created")

        pane = self.session.active_pane
        if pane is None:
            raise RuntimeError("No active pane in session")

        content = pane.capture_pane()

        return Frame(
            content="\n".join(content) if isinstance(content, list) else content,
            width=self.config.width,
            height=self.config.height,
            timestamp=time.time(),
        )

    def destroy(self) -> None:
        """Destroy tmux session."""
        if self.session:
            self.session.kill()

        if self.socket_path.exists():
            self.socket_path.unlink()
