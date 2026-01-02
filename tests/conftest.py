# tests/conftest.py
"""Pytest configuration and fixtures."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    )


@pytest.fixture
def output_dir():
    """Create persistent output directory for review."""
    output = Path("tests/test_outputs")
    output.mkdir(exist_ok=True)
    return output


@pytest.fixture
def preserved_tmp(tmp_path, output_dir, request):
    """Temporary path that gets copied to output_dir on test completion."""
    yield tmp_path

    # Copy to preserved location after test
    test_name = request.node.name
    dest = output_dir / test_name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(tmp_path, dest)
