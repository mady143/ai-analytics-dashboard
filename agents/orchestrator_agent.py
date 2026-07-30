"""
Orchestrator Agent — Master coordinator for the AI Analytics Dashboard.
Reads state, assigns tasks to sub-agents, and manages sprint progress.
"""

import os
import json
import time
from pathlib import Path
import sys
ROOT_DIR = Path(__file__).parent.parent
AGENTS_DIR = Path(__file__).parent
if str(AGENTS_DIR) not in sys.path:
    sys.path.insert(0, str(AGENTS_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from typing import Optional
from datetime import datetime
import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv
from memory_manager import (
    load_state, save_state, update_agent_status,
    load_last_conversation, save_conversation,
    log_task_result, get_todays_summary
)
from plane_agent import (
    get_or_create_project, list_tasks,
    update_task_status, add_comment, list_sprints
)
from git_agent import init_repo, setup_git_config, eod_push

load_dotenv()
console = Console()

ROOT_DIR = Path(__file__).parent.parent
AGENT_CONFIG_FILE = ROOT_DIR / "config" / "agent_config.json"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")


def load_agent_config() -> dict:
    with open(AGENT_CONFIG_FILE) as f:
        return json.load(f)


class OrchestratorAgent:
    """
    The master agent that:
    1. Reads current state + Plane sprint tasks
    2. Decides what needs to be done
    3. Delegates to Builder, Tester, or Git agents
    4. Updates Plane on completion
    5. Saves memory after each session
    """

    def __init__(self):
        self.config = load_agent_config()["orchestrator"]
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.state = load_state()
        self.messages = []
        self.project_id: Optional[str] = None
        self._load_memory()

    def _load_memory(self):
        """Restore last conversation context."""
        past_messages = load_last_conversation("orchestrator", max_messages=20)
        if past_messages:
            # Filter to valid message format for Claude API
            self.messages = [
                {"role": m["role"], "content": m["content"]}
                for m in past_messages
                if m.get("role") in ("user", "assistant") and m.get("content")
            ]
            console.print(f"[blue]📂 Restored {len(self.messages)} messages from memory[/blue]")

    def _save_memory(self):
        """Save conversation to memory."""
        save_conversation("orchestrator", self.messages)

    def _call_claude(self, user_message: str) -> str:
        """Send a message to Claude and get a response."""
        self.messages.append({"role": "user", "content": user_message})

        response = self.client.messages.create(
            model=self.config["model"],
            max_tokens=self.config["max_tokens"],
            system=self.config["system_prompt"],
            messages=self.messages
        )

        assistant_msg = response.content[0].text
        self.messages.append({"role": "assistant", "content": assistant_msg})
        return assistant_msg

    def _print_status(self):
        """Print current project status to console."""
        table = Table(title="🚀 AI Analytics Dashboard — Agent Status", style="bold")
        table.add_column("Agent", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Last Run", style="dim")

        agents = self.state.get("agents", {})
        for name, info in agents.items():
            status = info.get("status", "idle")
            last_run = info.get("last_run", "never")
            if last_run and last_run != "never":
                last_run = last_run[:19].replace("T", " ")
            color = {"idle": "dim", "running": "yellow", "completed": "green", "error": "red"}.get(status, "dim")
            table.add_row(name.title(), f"[{color}]{status}[/{color}]", last_run)

        console.print(table)

    def run_daily_session(self):
        """
        Main entry point for the daily agent session.
        Runs through:
        1. Status check
        2. Pull Plane tasks
        3. Work on top priority tasks
        4. Test completion
        5. EOD push
        """
        console.print(Panel.fit(
            "[bold magenta]🤖 Orchestrator Agent Starting...[/bold magenta]\n"
            f"[dim]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]",
            border_style="magenta"
        ))

        update_agent_status("orchestrator", "running", "Daily session")
        self._print_status()

        # Step 1: Initialize project if needed
        if not self.state.get("plane_project_id") and os.getenv("PLANE_API_TOKEN"):
            console.print("[yellow]🔧 Setting up Plane project...[/yellow]")
            try:
                self.project_id = get_or_create_project()
                self.state["plane_project_id"] = self.project_id
                save_state(self.state)
            except Exception as e:
                console.print(f"[yellow]⚠️  Plane setup skipped: {e}[/yellow]")
        else:
            self.project_id = self.state.get("plane_project_id")

        # Step 2: Initialize git
        init_repo()
        setup_git_config()

        # Step 3: Ask Claude what to do today
        context = self._build_context()
        plan = self._call_claude(context)
        console.print(Panel(plan, title="[cyan]Today's Plan[/cyan]", border_style="cyan"))

        # Step 4: Save memory
        self._save_memory()

        # Step 5: Update state
        update_agent_status("orchestrator", "idle")
        console.print("[bold green]✅ Orchestrator session complete![/bold green]")
        return plan

    def _build_context(self) -> str:
        """Build context message for Claude with current project state."""
        summary = get_todays_summary()
        plane_tasks_str = "Plane not configured" if not self.project_id else self._get_open_tasks()

        return f"""
You are managing the AI Analytics Dashboard project.

## Current Date & Time
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Today's Progress
- Tasks completed: {summary['tasks_completed']}
- Files changed: {len(summary['files_changed'])}
- Files: {', '.join(summary['files_changed'][:5]) or 'none'}

## Open Tasks in Plane
{plane_tasks_str}

## Project State
- Backend: FastAPI running at http://localhost:8000
- Frontend: React + Vite at http://localhost:5173
- Memory: Persistent conversation history enabled
- Git: Initialized with EOD auto-push

Based on this context, please:
1. Summarize what's been done
2. Identify the highest priority remaining tasks
3. Suggest which agent (Builder/Tester/Git) should act next
4. Estimate completion for Sprint 1

Keep your response concise and actionable.
"""

    def _get_open_tasks(self) -> str:
        """Get open tasks from Plane as a formatted string."""
        try:
            tasks = list_tasks(self.project_id)
            open_tasks = [t for t in tasks if "complet" not in t.get("state_detail", {}).get("name", "").lower()]
            if not open_tasks:
                return "✅ No open tasks!"
            return "\n".join([f"- [{t.get('priority', 'medium').upper()}] {t.get('name', '')}" for t in open_tasks[:10]])
        except Exception:
            return "Unable to fetch tasks"

    def mark_task_done(self, task_id: str, task_title: str):
        """Mark a task as done in Plane and log it."""
        if self.project_id:
            try:
                update_task_status(self.project_id, task_id, "completed")
                add_comment(self.project_id, task_id, f"✅ Completed by AI Agent at {datetime.now().strftime('%H:%M')}")
            except Exception as e:
                console.print(f"[yellow]⚠️  Could not update Plane: {e}[/yellow]")

        log_task_result(task_id, task_title, "orchestrator", "completed",
                        f"Task completed successfully at {datetime.now().isoformat()}")


    def watchdog_health_loop(self, poll_interval: int = 30):
        """
        Continuous Watchdog Monitor: Keeps an eye on all agents & servers.
        If any agent or server (FastAPI Backend / Vite Frontend) is stopped, crashed, or idle,
        Watchdog automatically restarts them and transitions everything back to RUNNING state!
        """
        import subprocess, sys, httpx
        console.print(Panel.fit(
            "[bold green]🛡️ Orchestrator Watchdog Active — Monitoring Server & Agent Fleet Health...[/bold green]",
            border_style="green"
        ))

        agent_scripts = {
            "sprint_watcher": ROOT_DIR / "scripts" / "run_sprint_watcher.py",
            "builder": ROOT_DIR / "agents" / "builder_agent.py",
            "tester": ROOT_DIR / "agents" / "tester_agent.py",
            "memory": ROOT_DIR / "agents" / "memory_manager.py",
            "git_agent": ROOT_DIR / "agents" / "git_agent.py"
        }

        try:
            while True:
                # ── 1. Check Server Endpoints ─────────────────────────────────────
                backend_healthy = False
                frontend_healthy = False
                try:
                    res = httpx.get("http://127.0.0.1:8000/docs", timeout=3.0)
                    backend_healthy = res.status_code == 200
                except Exception:
                    backend_healthy = False

                try:
                    res = httpx.get("http://127.0.0.1:5173", timeout=3.0)
                    frontend_healthy = res.status_code == 200
                except Exception:
                    frontend_healthy = False

                if not backend_healthy:
                    console.print("[bold red]🚨 Watchdog Alert: Backend FastAPI Server on :8000 is down! Auto-restarting server...[/bold red]")
                    try:
                        subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"], cwd=str(ROOT_DIR / "backend"))
                        console.print("[bold green]✅ FastAPI Backend Server auto-restarted on port 8000![/bold green]")
                    except Exception as ex:
                        console.print(f"[red]Failed to auto-restart backend server: {ex}[/red]")

                if not frontend_healthy:
                    console.print("[bold red]🚨 Watchdog Alert: Frontend Vite Server on :5173 is down! Auto-restarting server...[/bold red]")
                    try:
                        subprocess.Popen(["npm", "run", "dev", "--", "--host", "127.0.0.1"], cwd=str(ROOT_DIR / "frontend"), shell=True)
                        console.print("[bold green]✅ Vite Frontend Server auto-restarted on port 5173![/bold green]")
                    except Exception as ex:
                        console.print(f"[red]Failed to auto-restart frontend server: {ex}[/red]")

                # ── 2. Check Agent Fleet Status ──────────────────────────────────
                from memory_manager import get_dynamic_agent_statuses
                statuses = get_dynamic_agent_statuses()

                for agent_name, script_path in agent_scripts.items():
                    info = statuses.get(agent_name, {})
                    status = info.get("status", "idle")

                    # If an essential background agent is idle or stopped, auto-trigger/restart it!
                    if status != "running" and agent_name in ("sprint_watcher", "memory"):
                        console.print(f"[bold yellow]⚠️ Watchdog Alert: Agent '{agent_name}' is {status}. Auto-restarting...[/bold yellow]")
                        update_agent_status(agent_name, "running", f"Auto-restarted by Orchestrator Watchdog at {datetime.now().strftime('%H:%M:%S')}")
                        try:
                            if script_path.exists():
                                subprocess.Popen([sys.executable, str(script_path)])
                                console.print(f"[bold green]✅ Agent '{agent_name}' successfully restarted and transitioned to RUNNING state![/bold green]")
                        except Exception as ex:
                            console.print(f"[red]❌ Watchdog failed to restart {agent_name}: {ex}[/red]")

                time.sleep(poll_interval)
        except KeyboardInterrupt:
            console.print("[yellow]Watchdog stopped by user.[/yellow]")


if __name__ == "__main__":
    agent = OrchestratorAgent()
    if len(sys.argv) > 1 and sys.argv[1] == "--watchdog":
        agent.watchdog_health_loop(poll_interval=30)
    elif not ANTHROPIC_API_KEY:
        console.print("[yellow]⚠️ ANTHROPIC_API_KEY not set — starting Watchdog mode autonomously...[/yellow]")
        agent.watchdog_health_loop(poll_interval=30)
    else:
        agent.run_daily_session()
