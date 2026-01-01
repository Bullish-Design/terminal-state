"""Frame model for terminal state snapshots."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Frame(BaseModel):
    """Immutable terminal state snapshot."""

    model_config = ConfigDict(frozen=True)

    content: str = Field(description="Raw terminal output (may include ANSI)")
    width: int = Field(ge=1, le=1000)
    height: int = Field(ge=1, le=1000)
    timestamp: float = Field(description="Unix timestamp")

    # Optional enrichments
    ansi_data: bytes | None = Field(default=None, description="Preserved ANSI sequences")
    metadata: dict[str, str] = Field(default_factory=dict)
