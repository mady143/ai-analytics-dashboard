"""
Agent & Server Health Watchdog Supervisor.
Monitors all background agents (sprint_watcher, builder, tester, memory, git) and servers (FastAPI backend, Vite frontend).
If any agent or server goes down, crashed, or unexpectedly idle, auto-restarts them immediately!
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
AGENTS_DIR = ROOT_DIR / "agents"

if str(AGENTS_DIR) not in sys.path:
    sys.path.insert(0, str(AGENTS_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from orchestrator_agent import OrchestratorAgent

if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print("🛡️ Starting AI Analytics Dashboard — Agent & Server Watchdog Supervisor...")
    agent = OrchestratorAgent()
    agent.watchdog_health_loop(poll_interval=15)
