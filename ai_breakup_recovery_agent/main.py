# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""ai-breakup-recovery-agent - A Bindu Agent for emotional support and breakup recovery.

This agent provides comprehensive breakup recovery support through multiple specialized
agents: emotional support, closure messages, recovery planning, and honest feedback.
"""

import argparse
import asyncio
import json
import os
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from agno.agent import Agent
from agno.media import Image as AgnoImage
from agno.models.google import Gemini
from agno.models.openrouter import OpenRouter
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.mem0 import Mem0Tools
from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global instances
therapist_agent: Optional[Agent] = None
closure_agent: Optional[Agent] = None
routine_planner_agent: Optional[Agent] = None
brutal_honesty_agent: Optional[Agent] = None
recovery_team: Optional[Team] = None

model_name: Optional[str] = None
api_key: Optional[str] = None
mem0_api_key: Optional[str] = None
_initialized = False
_init_lock = asyncio.Lock()


def load_config() -> Dict[str, Any]:
    """Load agent configuration from project root."""
    # Try multiple possible locations for agent_config.json
    possible_paths = [
        Path(__file__).parent / "agent_config.json",  # Same directory as main.py
        Path(__file__).parent.parent / "agent_config.json",  # Project root
        Path.cwd() / "agent_config.json",  # Current working directory
    ]

    for config_path in possible_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except (PermissionError, json.JSONDecodeError) as e:
                print(f"⚠️  Error reading {config_path}: {type(e).__name__}")
                continue
            except Exception as e:
                print(f"⚠️  Unexpected error reading {config_path}: {type(e).__name__}")
                continue

    # If no config found, create a minimal default
    print("⚠️  No agent_config.json found, using default configuration")
    return {
        "name": "ai-breakup-recovery-agent",
        "description": "AI-powered breakup recovery assistant providing emotional support and practical guidance",
        "version": "1.0.0",
        "author": os.getenv("AUTHOR_EMAIL", "user@example.com"),
        "deployment": {
            "url": "http://127.0.0.1:3773",
            "expose": True,
            "protocol_version": "1.0.0",
            "proxy_urls": ["127.0.0.1"],
            "cors_origins": ["*"],
        },
        "environment_variables": [
            {"key": "GEMINI_API_KEY", "description": "Google Gemini API key", "required": False},
            {"key": "OPENROUTER_API_KEY", "description": "OpenRouter API key", "required": False},
            {"key": "MEM0_API_KEY", "description": "Mem0 API key for memory", "required": False},
        ],
    }


async def initialize_agents() -> None:
    """Initialize all specialized agents and the recovery team."""
    global therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent, recovery_team

    if not api_key:
        error_msg = "API key must be set before initializing agents"
        raise ValueError(error_msg)

    try:
        # Determine which model to use
        if api_key.startswith("AIza"):  # Google Gemini API keys start with AIza
            model = Gemini(id="gemini-2.0-flash-exp", api_key=api_key)
            print("✅ Using Google Gemini 2.0 Flash")
        else:
            model = OpenRouter(
                id=model_name or "google/gemini-2.0-flash-exp",
                api_key=api_key,
                cache_response=True,
                supports_native_structured_outputs=True,
            )
            print(f"✅ Using OpenRouter model: {model_name or 'google/gemini-2.0-flash-exp'}")

        # Initialize memory tools if API key is provided
        mem0_tools = None
        if mem0_api_key:
            mem0_tools = Mem0Tools(api_key=mem0_api_key)
            print("✅ Memory features enabled")

        # Initialize Therapist Agent (Emotional Support)
        therapist_agent = Agent(
            name="Therapist Agent",
            model=model,
            tools=[mem0_tools] if mem0_tools else None,
            instructions=[
                "You are an empathetic therapist specializing in breakup recovery.",
                "Your responsibilities:",
                "1. Listen with empathy and validate the user's feelings",
                "2. Use gentle, appropriate humor to lighten the mood when suitable",
                "3. Share relatable experiences to help users feel less alone",
                "4. Offer comforting words and genuine encouragement",
                "5. Analyze both text and any shared images for emotional context",
                "6. Never minimize their pain or rush the healing process",
                "Always respond with warmth, understanding, and genuine care.",
            ],
            markdown=True,
            add_datetime_to_context=True,
        )

        # Initialize Closure Agent (Unsent Messages)
        closure_agent = Agent(
            name="Closure Agent",
            model=model,
            tools=[mem0_tools] if mem0_tools else None,
            instructions=[
                "You are a closure specialist who helps people process unexpressed feelings.",
                "Your responsibilities:",
                "1. Help users craft emotional messages for feelings they never expressed",
                "2. Create templates for unsent letters that capture raw, honest emotions",
                "3. Guide users through emotional release exercises",
                "4. Suggest meaningful closure rituals and ceremonies",
                "5. Format messages clearly with appropriate headers and structure",
                "Ensure the tone is always heartfelt, authentic, and therapeutic.",
            ],
            markdown=True,
            add_datetime_to_context=True,
        )

        # Initialize Routine Planner Agent (Recovery Plan)
        routine_planner_agent = Agent(
            name="Routine Planner Agent",
            model=model,
            tools=[mem0_tools] if mem0_tools else None,
            instructions=[
                "You are a recovery routine planner specializing in post-breakup healing.",
                "Your responsibilities:",
                "1. Design personalized 7-day recovery challenges with daily tasks",
                "2. Include fun, engaging activities and essential self-care practices",
                "3. Suggest practical social media detox strategies and guidelines",
                "4. Create empowering playlists and mood-boosting activity suggestions",
                "5. Incorporate exercise, mindfulness, and social connection activities",
                "Focus on actionable, practical steps that promote healing and growth.",
            ],
            markdown=True,
            add_datetime_to_context=True,
        )

        # Initialize Brutal Honesty Agent (Direct Feedback with Web Search)
        tools = [DuckDuckGoTools()]
        if mem0_tools:
            tools.append(mem0_tools)
            
        brutal_honesty_agent = Agent(
            name="Brutal Honesty Agent",
            model=model,
            tools=tools,
            instructions=[
                "You are a direct feedback specialist who provides honest, constructive insights.",
                "Your responsibilities:",
                "1. Give raw, objective feedback about relationship dynamics and breakups",
                "2. Clearly explain what typically goes wrong in similar situations",
                "3. Use blunt but not cruel language to convey difficult truths",
                "4. Provide evidence-based reasons to move forward and heal",
                "5. Search for relevant articles, studies, or expert opinions when helpful",
                "Focus on helping users gain clarity and learn from their experience.",
            ],
            markdown=True,
            add_datetime_to_context=True,
        )

        # Create a Team that coordinates all agents
        recovery_team = Team(
            name="Breakup Recovery Squad",
            mode="coordinate",  # type: ignore[arg-type]  # String works at runtime despite type hint
            model=model,
            members=[
                therapist_agent,
                closure_agent,
                routine_planner_agent,
                brutal_honesty_agent,
            ],
            instructions=[
                "You are the coordinator of the Breakup Recovery Squad, a team of specialized agents.",
                "Analyze the user's input and determine which agents should respond:",
                "- For emotional support queries: use Therapist Agent",
                "- For closure and unsent messages: use Closure Agent",
                "- For recovery planning: use Routine Planner Agent",
                "- For honest feedback: use Brutal Honesty Agent",
                "For complex situations, coordinate responses from multiple agents.",
                "Ensure responses are cohesive and not repetitive.",
                "Always prioritize the user's emotional well-being.",
            ],
            markdown=True,
            add_datetime_to_context=True,
            show_members_responses=True,
            debug_mode=os.getenv("DEBUG_MODE", "false").lower() == "true",
        )

        print("✅ All recovery agents initialized successfully")

    except Exception as e:
        print(f"❌ Error initializing agents: {e}")
        traceback.print_exc()
        raise


async def process_images(uploaded_files: Optional[List[Dict[str, Any]]] = None) -> List[AgnoImage]:
    """Process uploaded images into AgnoImage format.

    Args:
        uploaded_files: List of uploaded file dictionaries with 'name', 'content', and 'type'

    Returns:
        List of AgnoImage objects
    """
    processed_images = []
    
    if not uploaded_files:
        return processed_images
    
    temp_files = []  # Track temp files for cleanup
    
    try:
        for file in uploaded_files:
            try:
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file['name']).suffix) as tmp_file:
                    tmp_file.write(file['content'])
                    tmp_path = tmp_file.name
                    temp_files.append(tmp_path)
                
                # Create AgnoImage from the temporary file
                agno_image = AgnoImage(filepath=Path(tmp_path))
                processed_images.append(agno_image)
                
            except Exception as e:
                print(f"⚠️  Error processing image {file.get('name', 'unknown')}: {e}")
                # Clean up this temp file if it was created
                if 'tmp_path' in locals():
                    try:
                        Path(tmp_path).unlink(missing_ok=True)
                    except Exception:
                        pass
                continue
        
        return processed_images
        
    except Exception as e:
        # Clean up all temp files on error
        for temp_file in temp_files:
            try:
                Path(temp_file).unlink(missing_ok=True)
            except Exception:
                pass
        raise


async def run_therapist_agent(user_input: str, images: Optional[List[AgnoImage]] = None) -> str:
    """Run the therapist agent for emotional support."""
    global therapist_agent
    
    if not therapist_agent:
        error_msg = "Therapist agent not initialized"
        raise RuntimeError(error_msg)
    
    prompt = f"""Provide emotional support based on:

User's message: {user_input}

Please provide a compassionate response with:
1. Validation of their feelings and experiences
2. Gentle, comforting words of support
3. Relatable insights to help them feel less alone
4. Encouragement and hope for the future
5. Gentle humor if appropriate to lighten the mood

Remember to be warm, empathetic, and genuinely supportive."""
    
    response = therapist_agent.run(prompt, images=images)
    return response.content if response.content else ""


async def run_closure_agent(user_input: str, images: Optional[List[AgnoImage]] = None) -> str:
    """Run the closure agent for unsent messages and emotional release."""
    global closure_agent
    
    if not closure_agent:
        error_msg = "Closure agent not initialized"
        raise RuntimeError(error_msg)
    
    prompt = f"""Help create emotional closure based on:

User's feelings: {user_input}

Please provide:
1. Templates for unsent messages that capture their unexpressed feelings
2. Emotional release exercises to process pain and anger
3. Meaningful closure rituals and ceremonies
4. Strategies for letting go and moving forward
5. Ways to honor the relationship and its lessons

Format messages clearly and ensure the tone is heartfelt and authentic."""
    
    response = closure_agent.run(prompt, images=images)
    return response.content if response.content else ""


async def run_routine_planner_agent(user_input: str, images: Optional[List[AgnoImage]] = None) -> str:
    """Run the routine planner agent for recovery planning."""
    global routine_planner_agent
    
    if not routine_planner_agent:
        error_msg = "Routine planner agent not initialized"
        raise RuntimeError(error_msg)
    
    prompt = f"""Design a personalized 7-day recovery plan based on:

Current emotional state: {user_input}

Include:
1. Daily activities and challenges for each of the 7 days
2. Self-care routines and mindfulness practices
3. Social media detox strategies and screen time guidelines
4. Mood-lifting music, podcast, and activity suggestions
5. Exercise and movement recommendations
6. Social connection ideas (when ready)
7. Journaling prompts for reflection

Make the plan practical, actionable, and tailored to their situation."""
    
    response = routine_planner_agent.run(prompt, images=images)
    return response.content if response.content else ""


async def run_brutal_honesty_agent(user_input: str, images: Optional[List[AgnoImage]] = None) -> str:
    """Run the brutal honesty agent for direct feedback."""
    global brutal_honesty_agent
    
    if not brutal_honesty_agent:
        error_msg = "Brutal honesty agent not initialized"
        raise RuntimeError(error_msg)
    
    prompt = f"""Provide honest, constructive feedback about:

Situation: {user_input}

Include:
1. Objective analysis of relationship dynamics and what typically goes wrong
2. Honest insights about patterns and behaviors to examine
3. Growth opportunities and lessons to learn
4. Realistic future outlook and what to expect
5. Actionable steps for personal development
6. Search for relevant articles or expert perspectives if helpful

Be direct and honest, but maintain compassion. Focus on clarity and growth."""
    
    response = brutal_honesty_agent.run(prompt, images=images)
    return response.content if response.content else ""


async def run_recovery_team(user_input: str, images: Optional[List[AgnoImage]] = None) -> Dict[str, Any]:
    """Run the entire recovery team for comprehensive support."""
    global recovery_team
    
    if not recovery_team:
        error_msg = "Recovery team not initialized"
        raise RuntimeError(error_msg)
    
    prompt = f"""Coordinate the Breakup Recovery Squad to help with:

User's situation: {user_input}

Please analyze their needs and have the appropriate agents respond.
If multiple types of support are needed, coordinate responses from multiple agents.
Ensure the responses are comprehensive, non-repetitive, and truly helpful."""
    
    response = recovery_team.run(prompt, images=images)
    
    return {
        "coordinator_response": response.content if hasattr(response, 'content') else str(response),
        "member_responses": getattr(response, 'member_responses', []),
    }


async def handler(messages: List[Dict[str, str]]) -> str:
    """Handle incoming agent messages with lazy initialization.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
                 Format expected by Bindu: [{"role": "user", "content": "user message"}]
    
    Returns:
        Response string for UI display
    """
    global _initialized
    
    # Extract data from messages
    images_data = []
    mode = "team"
    user_input = ""
    
    if messages and len(messages) > 0:
        last_message = messages[-1]
        if last_message.get("role") == "user":
            content = last_message.get("content", "")
            
            # Check if content is JSON with special parameters
            if content.startswith("{") and content.endswith("}"):
                try:
                    parsed = json.loads(content)
                    if isinstance(parsed, dict):
                        user_input = parsed.get("text", "")
                        images_data = parsed.get("images", [])
                        mode = parsed.get("mode", "team")
                except json.JSONDecodeError:
                    # Not JSON, use content as is
                    user_input = content
            else:
                user_input = content
    
    if not user_input:
        return "No valid user message found"
    
    # Lazy initialization on first call
    async with _init_lock:
        if not _initialized:
            print("🔧 Initializing Breakup Recovery Squad...")
            try:
                await initialize_agents()
                _initialized = True
                print("✅ Breakup Recovery Squad ready!")
            except Exception as e:
                error_msg = f"Failed to initialize agents: {e}"
                print(f"❌ {error_msg}")
                return f"Error: {error_msg}"
    
    try:
        # Process images if any
        images = await process_images(images_data) if images_data else []
        
        # Run the appropriate agent based on mode
        if mode == "therapist":
            return await run_therapist_agent(user_input, images)
        elif mode == "closure":
            return await run_closure_agent(user_input, images)
        elif mode == "routine":
            return await run_routine_planner_agent(user_input, images)
        elif mode == "honest":
            return await run_brutal_honesty_agent(user_input, images)
        else:  # team mode (default)
            team_response = await run_recovery_team(user_input, images)
            return team_response["coordinator_response"]
            
    except Exception as e:
        print(f"❌ Error in handler: {e}")
        traceback.print_exc()
        return f"Error: {e}"


async def cleanup() -> None:
    """Clean up any resources."""
    print("🧹 Cleaning up Breakup Recovery Squad resources...")


def main():
    """Run the main entry point for the Breakup Recovery Agent."""
    global model_name, api_key, mem0_api_key

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="AI Breakup Recovery Agent - Bindu Agent")
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_NAME", "google/gemini-2.0-flash-exp"),
        help="Model ID to use (default: google/gemini-2.0-flash-exp, env: MODEL_NAME)",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key (GEMINI_API_KEY or OPENROUTER_API_KEY env var)",
    )
    parser.add_argument(
        "--mem0-api-key",
        type=str,
        default=os.getenv("MEM0_API_KEY"),
        help="Mem0 API key for memory features (env: MEM0_API_KEY)",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to custom agent_config.json",
    )
    args = parser.parse_args()

    # Set global variables
    model_name = args.model
    api_key = args.api_key or os.getenv("GEMINI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    mem0_api_key = args.mem0_api_key

    # Validate required API key
    if not api_key:
        print("❌ ERROR: API key is required")
        print("\nPlease set your API key in one of these ways:")
        print("  1. Environment variable: export GEMINI_API_KEY='your-key-here'")
        print("  2. Environment variable: export OPENROUTER_API_KEY='your-key-here'")
        print("  3. Command line: --api-key your-key-here")
        print("\nGet your API key:")
        print("  • Google Gemini: https://makersuite.google.com/app/apikey")
        print("  • OpenRouter: https://openrouter.ai/keys")
        sys.exit(1)

    # Load configuration
    if args.config:
        config_path = Path(args.config)
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
        else:
            print(f"❌ Config file not found: {args.config}")
            sys.exit(1)
    else:
        config = load_config()

    print("\n" + "=" * 50)
    print("💔 Breakup Recovery Squad - Starting Up")
    print("=" * 50)
    print(f"📱 Agent: {config.get('name', 'ai-breakup-recovery-agent')}")
    print(f"🤖 Model: {model_name}")
    provider = "Google Gemini" if api_key and api_key.startswith("AIza") else "OpenRouter"
    print(f"🔌 Provider: {provider}")
    print(f"🧠 Memory: {'Enabled' if mem0_api_key else 'Disabled'}")
    print("=" * 50 + "\n")

    try:
        # Start the agent server
        print("🚀 Starting Breakup Recovery Squad server...")
        server_url = config.get('deployment', {}).get('url', 'http://127.0.0.1:3773')
        print(f"🌐 Server will run on: {server_url}")
        print("⏳ Agents will initialize on first request\n")
        
        bindufy(config, handler)
        
    except KeyboardInterrupt:
        print("\n🛑 Breakup Recovery Squad stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        asyncio.run(cleanup())
        print("👋 Goodbye! Take care of yourself.")


if __name__ == "__main__":
    main()