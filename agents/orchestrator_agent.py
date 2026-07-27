"""
Orchestrator Agent — Master coordinator for the AI Analytics Dashboard.
Reads state, assigns tasks to sub-agents, and manages sprint progress.
"""

import os
import json
import time
from pathlib import Path
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


if __name__ == "__main__":
    if not ANTHROPIC_API_KEY:
        console.print("[red]❌ ANTHROPIC_API_KEY not set in .env[/red]")
        console.print("[yellow]Please add your Claude API key to the .env file[/yellow]")
    else:
        agent = OrchestratorAgent()
        agent.run_daily_session()
