"""Tests for the Breakup Recovery Agent."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# We import from the module where main.py resides.
# Assuming standard structure based on previous files.
from ai_breakup_recovery_agent.main import (
    cleanup,
    generate_full_report,
    handler,
    initialize_agents,
    load_config,
)


@pytest.fixture
def mock_agent_response():
    """Fixture for mock agent response."""
    response = MagicMock()
    response.content = "This is a test response."
    return response


# ==================== CONFIG TESTS ====================


def test_load_config_success():
    """Test successful config loading."""
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("builtins.open") as mock_open,
    ):
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = '{"name": "test_config"}'
        mock_open.return_value = mock_file

        config = load_config()
        assert config["name"] == "test_config"


def test_load_config_fallback():
    """Test config loading fallback when file doesn't exist."""
    with patch("pathlib.Path.exists", return_value=False):
        config = load_config()
        assert config["name"] == "ai-breakup-recovery-agent"


# ==================== INITIALIZATION TESTS ====================


@pytest.mark.asyncio
async def test_initialize_agents_success():
    """Test successful agent initialization populates the _agents dict."""
    with (
        patch("ai_breakup_recovery_agent.main.os.getenv", return_value="fake-key"),
        patch("ai_breakup_recovery_agent.main.Gemini") as mock_gemini,
        patch("ai_breakup_recovery_agent.main.DuckDuckGoTools"),
        patch("ai_breakup_recovery_agent.main.Agent") as mock_agent,
    ):
        # Setup mocks
        mock_agent_instance = MagicMock()
        mock_agent.return_value = mock_agent_instance

        # We need to access the global _agents dict from the module
        with patch("ai_breakup_recovery_agent.main._agents", {}) as mock_agents_dict:
            await initialize_agents()

            # Verify all 4 agents were created
            assert "therapist" in mock_agents_dict
            assert "closure" in mock_agents_dict
            assert "planner" in mock_agents_dict
            assert "honesty" in mock_agents_dict

            # Verify Gemini was used (preferred over OpenRouter if key present)
            mock_gemini.assert_called()


@pytest.mark.asyncio
async def test_initialize_agents_no_key():
    """Test initialization fails without API key."""
    with (
        patch("ai_breakup_recovery_agent.main.os.getenv", return_value=None),
        pytest.raises(ValueError, match="No API Key found"),
    ):
        await initialize_agents()


# ==================== REPORT GENERATION TESTS ====================


@pytest.mark.asyncio
async def test_generate_full_report():
    """Test that full report aggregates responses from all agents."""

    # Create mock agents
    mock_therapist = AsyncMock()
    mock_therapist.arun.return_value.content = "Therapist says hang in there."

    mock_closure = AsyncMock()
    mock_closure.arun.return_value.content = "Write a letter."

    mock_planner = AsyncMock()
    mock_planner.arun.return_value.content = "Go for a run."

    mock_honesty = AsyncMock()
    mock_honesty.arun.return_value.content = "It's over."

    mock_agents = {
        "therapist": mock_therapist,
        "closure": mock_closure,
        "planner": mock_planner,
        "honesty": mock_honesty,
    }

    with patch("ai_breakup_recovery_agent.main._agents", mock_agents):
        report = await generate_full_report("I felt sad today", [])

        # Verify all agents were called
        mock_therapist.arun.assert_called_once()
        mock_closure.arun.assert_called_once()
        mock_planner.arun.assert_called_once()
        mock_honesty.arun.assert_called_once()

        # Verify output structure
        assert "# 💔 Breakup Recovery Plan" in report
        assert "Therapist says hang in there" in report
        assert "It's over" in report


# ==================== HANDLER TESTS ====================


@pytest.mark.asyncio
async def test_handler_initialization():
    """Test that handler initializes agents on first run."""
    messages = [{"role": "user", "content": "hello"}]

    with (
        patch("ai_breakup_recovery_agent.main._initialized", False),
        patch("ai_breakup_recovery_agent.main.initialize_agents", new_callable=AsyncMock) as mock_init,
        patch("ai_breakup_recovery_agent.main._init_lock") as mock_lock,
        patch("ai_breakup_recovery_agent.main._agents") as mock_agents,
    ):
        # Mock the lock and agents
        mock_lock.__aenter__ = AsyncMock()
        mock_lock.__aexit__ = AsyncMock()

        mock_therapist = AsyncMock()
        mock_therapist.arun.return_value.content = "Hello there."
        mock_agents.__getitem__.return_value = mock_therapist

        await handler(messages)

        mock_init.assert_called_once()


@pytest.mark.asyncio
async def test_handler_chat_mode():
    """Test that short/generic messages trigger only the Therapist."""
    messages = [{"role": "user", "content": "I am feeling a bit down"}]

    mock_therapist = AsyncMock()
    mock_therapist.arun.return_value.content = "I'm here for you."

    mock_agents = {"therapist": mock_therapist}

    with (
        patch("ai_breakup_recovery_agent.main._initialized", True),
        patch("ai_breakup_recovery_agent.main._agents", mock_agents),
        patch("ai_breakup_recovery_agent.main.generate_full_report", new_callable=AsyncMock) as mock_report,
    ):
        response = await handler(messages)

        # Should call therapist, NOT full report
        mock_therapist.arun.assert_called_once()
        mock_report.assert_not_called()
        assert response == "I'm here for you."


@pytest.mark.asyncio
async def test_handler_full_plan_mode():
    """Test that specific keywords trigger the full recovery plan."""
    # "plan" is a trigger word in main.py
    messages = [{"role": "user", "content": "I need a recovery plan please"}]

    with (
        patch("ai_breakup_recovery_agent.main._initialized", True),
        patch("ai_breakup_recovery_agent.main.generate_full_report", new_callable=AsyncMock) as mock_report,
    ):
        mock_report.return_value = "# Full Plan"

        response = await handler(messages)

        mock_report.assert_called_once()
        assert response == "# Full Plan"


@pytest.mark.asyncio
async def test_handler_empty_messages():
    """Test handler behavior with empty input."""
    with patch("ai_breakup_recovery_agent.main._initialized", True):
        response = await handler([])
        assert response == "Please tell me what happened."


@pytest.mark.asyncio
async def test_cleanup():
    """Test cleanup prints message."""
    with patch("builtins.print") as mock_print:
        await cleanup()
        mock_print.assert_called_with("🧹 Cleaning up resources...")
