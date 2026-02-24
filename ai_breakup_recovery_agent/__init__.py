# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""ai-breakup-recovery-agent - A Bindu Agent for emotional support and breakup recovery.

This package provides a multi-agent system for breakup recovery support, featuring:
- Therapist Agent for emotional support
- Closure Agent for unsent messages and emotional release
- Routine Planner Agent for recovery planning
- Brutal Honesty Agent for direct feedback
"""

from ai_breakup_recovery_agent.__version__ import __version__
from ai_breakup_recovery_agent.main import (
    cleanup,
    handler,
    initialize_agents,
    main,
    process_images,
    run_brutal_honesty_agent,
    run_closure_agent,
    run_recovery_team,
    run_routine_planner_agent,
    run_therapist_agent,
)

__all__ = [
    "__version__",
    "cleanup",
    "handler",
    "initialize_agents",
    "main",
    "process_images",
    "run_brutal_honesty_agent",
    "run_closure_agent",
    "run_recovery_team",
    "run_routine_planner_agent",
    "run_therapist_agent",
]
