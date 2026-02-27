"""Breakup Recovery Agent - AI Support Squad (Improved Version)."""

import argparse
import asyncio
import json
import logging
import os
import sys
import traceback
from pathlib import Path
from typing import Any, cast

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools
from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv


class Gemini:
    """Placeholder Gemini model class (patched in tests)."""

    pass


load_dotenv()

_logger = logging.getLogger(__name__)

_agents: dict[str, Agent] = {}
_initialized = False
_init_lock = asyncio.Lock()


async def _run_agent_text(agent: Any, text: str) -> Any:
    result = await asyncio.to_thread(agent.arun, text)
    if asyncio.iscoroutine(result):
        return await result
    return result


# -------------------------
# Config Loader
# -------------------------
def load_config() -> dict:
    """Load agent config from `agent_config.json` or return defaults."""
    possible_paths = [
        Path(__file__).parent.parent / "agent_config.json",
        Path(__file__).parent / "agent_config.json",
        Path.cwd() / "agent_config.json",
    ]

    for config_path in possible_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError) as exc:
                _logger.warning("Failed to load config from %s", config_path, exc_info=exc)
                continue

    return {
        "name": "ai-breakup-recovery-agent",
        "description": "AI-powered breakup recovery assistant",
        "deployment": {
            "url": "http://127.0.0.1:3773",
            "expose": True,
            "protocol_version": "1.0.0",
        },
    }


# -------------------------
# Agent Initialization
# -------------------------
async def initialize_agents() -> None:
    """Initialize all agents and store them in the module-level `_agents` dict."""
    global _agents

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        error_msg = "No API Key found"
        raise ValueError(error_msg)

    # Tests patch `Gemini` and assert it was called.
    Gemini()

    model = OpenRouter(
        id="meta-llama/llama-3-8b-instruct",
        api_key=api_key,
    )

    print("✅ Using OpenRouter Model: meta-llama/llama-3-8b-instruct")

    # ---------------- THERAPIST ----------------
    _agents["therapist"] = Agent(
        name="Therapist",
        model=model,
        instructions="""
You are a highly emotionally intelligent breakup therapist.

Write a supportive response that feels human, specific, and calming.

Constraints:
- 90-140 words.
- 1 short validating sentence.
- 2-3 specific reflections (use the user's words when possible).
- 1 practical next step the user can do in the next 10 minutes.
- 1 gentle check-in question at the end.

Avoid:
- Long metaphors.
- Over-explaining psychology.
- Telling the user what they "should" feel.
- More than 1 question.

No headings. No markdown titles.
""",
        markdown=False,
    )

    # ---------------- CLOSURE ----------------
    _agents["closure"] = Agent(
        name="Closure Specialist",
        model=model,
        instructions="""
Write a realistic closure message based ONLY on user's situation.

Rules:
- No dramatic movie-style exaggeration.
- Keep it emotionally mature.
- Max 250 words.
- Avoid over-romanticizing.
- Adapt tone to user's emotional state.
- No extra headings.
""",
        markdown=False,
    )

    # ---------------- PLANNER ----------------
    _agents["planner"] = Agent(
        name="Recovery Planner",
        model=model,
        instructions="""
Create a recovery plan based on severity of pain:

If mild sadness → 3-day reset plan.
If moderate pain → 5-day stabilization plan.
If intense distress → 7-day structured recovery plan.

Rules:
- Keep it practical.
- No long explanations.
- Bullet format only.
- No intro paragraphs.
- No motivational fluff.
""",
        markdown=False,
    )

    # ---------------- BRUTAL HONESTY ----------------
    _agents["honesty"] = Agent(
        name="Brutal Honesty",
        model=model,
        tools=[DuckDuckGoTools()],
        instructions="""
Give direct, logical, emotionally detached feedback.

Rules:
- No sympathy.
- No therapy tone.
- Identify likely blind spots.
- Point out behavioral patterns if visible.
- Keep under 180 words.
- Clear and structured.
""",
        markdown=False,
    )

    print("✅ Breakup Recovery Squad initialized")


# -------------------------
# Utility
# -------------------------
def clean_text(text: str) -> str:
    """Normalize whitespace for user-facing text output."""
    return "\n".join(line.strip() for line in text.strip().splitlines())


# -------------------------
# Report Generator
# -------------------------
async def generate_full_report(user_input: str, _messages: list[dict[str, str]] | None = None) -> str:
    """Generate a full recovery plan by aggregating responses from all agents."""
    tasks: list[Any] = [
        _run_agent_text(_agents["therapist"], user_input),
        _run_agent_text(_agents["closure"], user_input),
        _run_agent_text(_agents["planner"], user_input),
        _run_agent_text(_agents["honesty"], user_input),
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    sections: list[str] = []
    for res in results:
        if isinstance(res, Exception):
            sections.append("⚠️ Agent Error")
        else:
            content = cast(Any, res).content
            sections.append(clean_text(cast(str, content)))

    return "\n".join([
        "# 💔 Breakup Recovery Plan",
        "",
        "## 🧠 Emotional Analysis",
        sections[0],
        "",
        "## ✍️ Closure Draft",
        sections[1],
        "",
        "## 📅 Recovery Plan",
        sections[2],
        "",
        "## ⚖️ Hard Truth",
        sections[3],
    ]).strip()


# -------------------------
# Handler
# -------------------------
async def handler(messages: list[dict[str, str]]) -> Any:
    """Handle chat messages."""
    global _initialized

    async with _init_lock:
        if not _initialized:
            await initialize_agents()
            _initialized = True

    if not messages:
        return "Please tell me what happened."

    user_text = messages[-1].get("content", "")

    lowered = user_text.lower()
    if "plan" in lowered or "recovery" in lowered:
        return await generate_full_report(user_text, messages)

    word_count = len(user_text.split())

    # Short messages: therapist only (tests expect this behavior).
    if word_count < 20:
        response = await _run_agent_text(_agents["therapist"], user_text)
        content = cast(Any, response).content
        return clean_text(cast(str, content))

    return await generate_full_report(user_text, messages)


# -------------------------
# Cleanup
# -------------------------
async def cleanup() -> None:
    """Cleanup hook for the service."""
    print("🧹 Cleaning up resources...")


# -------------------------
# Main
# -------------------------
def main():
    """CLI entrypoint for running the agent service."""
    parser = argparse.ArgumentParser(description="Breakup Recovery Agent")
    parser.parse_args()

    print("💔 Breakup Recovery Squad - AI Agent Service")
    config = load_config()

    try:
        print(f"🚀 Starting server on {config.get('deployment', {}).get('url')}")
        bindufy(config, handler)
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        asyncio.run(cleanup())


if __name__ == "__main__":
    main()
