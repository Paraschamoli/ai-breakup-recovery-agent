"""Tests for the Breakup Recovery Agent."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from ai_breakup_recovery_agent.main import handler


@pytest.mark.asyncio
async def test_handler_returns_response():
    """Test that handler accepts messages and returns a response."""
    messages = [{"role": "user", "content": "I'm feeling really sad after my breakup"}]

    # Mock the run_recovery_team function to return a mock response
    mock_response = "This is a test response from the agent."

    # Mock _initialized to skip initialization and run_recovery_team to return our mock
    with (
        patch("ai_breakup_recovery_agent.main._initialized", True),
        patch(
            "ai_breakup_recovery_agent.main.run_recovery_team",
            new_callable=AsyncMock,
            return_value={"coordinator_response": mock_response},
        ),
    ):
        result = await handler(messages)

    # Verify we get a result back
    assert result is not None
    assert isinstance(result, str)
    assert result == mock_response


@pytest.mark.asyncio
async def test_handler_with_multiple_messages():
    """Test that handler processes multiple messages correctly."""
    messages = [
        {"role": "system", "content": "You are a helpful recovery assistant."},
        {"role": "user", "content": "I need help moving on"},
    ]

    mock_response = "Here's some advice to help you move on."

    with (
        patch("ai_breakup_recovery_agent.main._initialized", True),
        patch(
            "ai_breakup_recovery_agent.main.run_recovery_team",
            new_callable=AsyncMock,
            return_value={"coordinator_response": mock_response},
        ) as mock_run,
    ):
        result = await handler(messages)

    # Verify run_recovery_team was called
    mock_run.assert_called_once_with("I need help moving on", [])
    assert result is not None
    assert result == mock_response


@pytest.mark.asyncio
async def test_handler_initialization():
    """Test that handler initializes on first call."""
    messages = [{"role": "user", "content": "Test"}]

    mock_response = "Test response"

    # Start with _initialized as False to test initialization path
    with (
        patch("ai_breakup_recovery_agent.main._initialized", False),
        patch("ai_breakup_recovery_agent.main.initialize_agents", new_callable=AsyncMock) as mock_init,
        patch(
            "ai_breakup_recovery_agent.main.run_recovery_team",
            new_callable=AsyncMock,
            return_value={"coordinator_response": mock_response},
        ) as mock_run,
        patch("ai_breakup_recovery_agent.main._init_lock", new_callable=MagicMock) as mock_lock,
    ):
        # Configure the lock to work as an async context manager
        mock_lock_instance = MagicMock()
        mock_lock_instance.__aenter__ = AsyncMock(return_value=None)
        mock_lock_instance.__aexit__ = AsyncMock(return_value=None)
        mock_lock.return_value = mock_lock_instance

        result = await handler(messages)

        # Verify initialization was called
        mock_init.assert_called_once()
        # Verify run_recovery_team was called
        mock_run.assert_called_once_with("Test", [])
        # Verify we got a result
        assert result == mock_response


@pytest.mark.asyncio
async def test_handler_race_condition_prevention():
    """Test that handler prevents race conditions with initialization lock."""
    messages = [{"role": "user", "content": "Test"}]

    mock_response = "Test response"

    # Test with multiple concurrent calls
    with (
        patch("ai_breakup_recovery_agent.main._initialized", False),
        patch("ai_breakup_recovery_agent.main.initialize_agents", new_callable=AsyncMock) as mock_init,
        patch(
            "ai_breakup_recovery_agent.main.run_recovery_team",
            new_callable=AsyncMock,
            return_value={"coordinator_response": mock_response},
        ),
        patch("ai_breakup_recovery_agent.main._init_lock", new_callable=MagicMock) as mock_lock,
    ):
        # Configure the lock to work as an async context manager
        mock_lock_instance = MagicMock()
        mock_lock_instance.__aenter__ = AsyncMock(return_value=None)
        mock_lock_instance.__aexit__ = AsyncMock(return_value=None)
        mock_lock.return_value = mock_lock_instance

        # Call handler twice to ensure lock is used
        await handler(messages)
        await handler(messages)

        # Verify initialize_agents was called only once (due to lock)
        mock_init.assert_called_once()


@pytest.mark.asyncio
async def test_handler_with_different_modes():
    """Test that handler works with different agent modes."""
    modes = ["therapist", "closure", "routine", "honest", "team"]
    agent_functions = {
        "therapist": "run_therapist_agent",
        "closure": "run_closure_agent",
        "routine": "run_routine_planner_agent",
        "honest": "run_brutal_honesty_agent",
        "team": "run_recovery_team",
    }

    for mode in modes:
        # Create JSON message with mode
        import json

        content = json.dumps({"text": "I need help", "mode": mode})
        messages = [{"role": "user", "content": content}]

        mock_response = f"Response from {mode} agent"

        with (
            patch("ai_breakup_recovery_agent.main._initialized", True),
            patch(f"ai_breakup_recovery_agent.main.{agent_functions[mode]}", new_callable=AsyncMock) as mock_run,
        ):
            if mode == "team":
                mock_run.return_value = {"coordinator_response": mock_response}
            else:
                mock_run.return_value = mock_response

            result = await handler(messages)

            assert result == mock_response


@pytest.mark.asyncio
async def test_handler_simple_format():
    """Test handler with simple (non-JSON) format."""
    messages = [{"role": "user", "content": "I need help"}]

    mock_response = "Simple response"

    with (
        patch("ai_breakup_recovery_agent.main._initialized", True),
        patch(
            "ai_breakup_recovery_agent.main.run_recovery_team",
            new_callable=AsyncMock,
            return_value={"coordinator_response": mock_response},
        ),
    ):
        result = await handler(messages)

        assert result == mock_response


@pytest.mark.asyncio
async def test_handler_with_no_messages():
    """Test that handler handles empty messages gracefully."""
    with patch("ai_breakup_recovery_agent.main._initialized", True):
        result = await handler([])
        assert result == "No valid user message found"


@pytest.mark.asyncio
async def test_handler_with_no_user_message():
    """Test that handler handles missing user message."""
    messages = [{"role": "system", "content": "System message"}]

    with patch("ai_breakup_recovery_agent.main._initialized", True):
        result = await handler(messages)
        assert result == "No valid user message found"


@pytest.mark.asyncio
async def test_handler_initialization_failure():
    """Test that handler handles initialization failure gracefully."""
    messages = [{"role": "user", "content": "Test"}]

    with (
        patch("ai_breakup_recovery_agent.main._initialized", False),
        patch("ai_breakup_recovery_agent.main.initialize_agents", new_callable=AsyncMock) as mock_init,
        patch("ai_breakup_recovery_agent.main._init_lock") as mock_lock,
    ):
        mock_init.side_effect = Exception("API key invalid")
        mock_lock.__aenter__ = AsyncMock()
        mock_lock.__aexit__ = AsyncMock()

        result = await handler(messages)

        assert "Failed to initialize agents" in result
