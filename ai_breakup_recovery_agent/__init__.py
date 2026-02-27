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
    generate_full_report,
    handler,
    initialize_agents,
    main,
)

__all__ = [
    "__version__",
    "cleanup",
    "generate_full_report",
    "handler",
    "initialize_agents",
    "main",
]
