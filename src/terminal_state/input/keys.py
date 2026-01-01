"""Key sequence handling and validation."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class KeySequence(BaseModel):
    """Type-safe key sequence with tmux notation support."""

    keys: str = Field(description="Key sequence (supports tmux notation)")
    literal: bool = Field(default=False, description="Send as literal text")

    @field_validator("keys")
    @classmethod
    def validate_keys(cls, v: str) -> str:
        """Validate key sequence format."""
        if not v:
            raise ValueError("Key sequence cannot be empty")
        return v

    @property
    def is_special(self) -> bool:
        """Check if contains special key notation."""
        return not self.literal and ("<" in self.keys or "C-" in self.keys or "M-" in self.keys)


class Keys:
    """Predefined key sequences."""

    ESCAPE = KeySequence(keys="Escape")
    ENTER = KeySequence(keys="Enter")
    TAB = KeySequence(keys="Tab")
    CTRL_C = KeySequence(keys="C-c")
    CTRL_D = KeySequence(keys="C-d")
    UP = KeySequence(keys="Up")
    DOWN = KeySequence(keys="Down")
    LEFT = KeySequence(keys="Left")
    RIGHT = KeySequence(keys="Right")
