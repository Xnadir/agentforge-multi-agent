"""Tests for the orchestrator module."""

import pytest


def test_placeholder():
    """Placeholder — will add real tests once fixtures are set up."""
    assert True


def test_agent_roles_defined():
    """Verify the expected agent roles exist."""
    from agents import AGENTS
    expected_roles = {"researcher", "analyst", "writer"}
    assert expected_roles.issubset(set(AGENTS.keys()))
