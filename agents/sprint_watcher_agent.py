"""
Sprint Watcher Agent — Continuously monitors Plane sprint activity.
Lightweight & Modularized (< 250 lines).
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "agents"))
load_dotenv(ROOT_DIR / ".env")
console = Console(legacy_windows=False)

from plane_agent import get_or_create_project, list_tasks, list_sprints, update_task_status, add_comment
from memory_manager import update_agent_status, log_task_result, load_state, save_state
from sprint_watcher_helpers import render_sprint_table

STATE_TODO    = "unstarted"
STATE_INPROG  = "started"
STATE_DONE    = "done"
STATE_FAILED  = "cancelled"


class SprintWatcherAgent:
    """Watches active Plane sprint and drives task lifecycle: Todo → In Progress → Tests → Done."""

    def __init__(self, poll_interval_seconds: int = 15):
        self.poll_interval = poll_interval_seconds
        self.project_id: Optional[str] = None
        self.state = load_state()

    def _init_project(self) -> bool:
        self.project_id = self.state.get("plane_project_id")
        if not self.project_id:
            try:
                self.project_id = get_or_create_project()
                self.state["plane_project_id"] = self.project_id
                save_state(self.state)
            except Exception as e:
                console.print(f"[red]❌ Could not connect to Plane: {e}[/red]")
                return False
        return True

    def _fetch_sprint_tasks(self) -> list[dict]:
        try:
            return list_tasks(self.project_id)
        except Exception as e:
            console.print(f"[yellow]⚠️  Failed to fetch tasks: {e}[/yellow]")
            return []

    def _run_builder(self, task_id: str, task_title: str, description: str, priority: str) -> bool:
        console.print(f"[cyan]🔨 Invoking Builder Agent for: {task_title}[/cyan]")
        try:
            cmd = [
                sys.executable,
                str(ROOT_DIR / "agents" / "builder_agent.py"),
                "--task-id", task_id,
                "--task-title", task_title,
                "--description", description or task_title,
                "--priority", priority,
            ]
            result = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                console.print(f"[green]✅ Builder completed: {task_title}[/green]")
                return True
            else:
                console.print(f"[red]❌ Builder failed:\n{result.stderr[:300]}[/red]")
                return False
        except Exception as e:
            console.print(f"[red]❌ Builder exception: {e}[/red]")
            return False

    def _run_tests(self) -> tuple[bool, str]:
        console.print("[cyan]🧪 Running Core Unit Tests...[/cyan]")
        try:
            cmd = [sys.executable, "-m", "pytest", "tests/unit/", "-v", "--tb=short", "-q"]
            res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=120)
            passed = (res.returncode == 0)
            output = res.stdout[:500] if passed else res.stderr[:500]
            if passed:
                console.print("[green]✅ Unit Tests PASSED[/green]")
            else:
                console.print(f"[red]❌ Unit Tests FAILED:\n{output}[/red]")
            return passed, output
        except Exception as e:
            return False, f"Test error: {e}"

    def _finalize_task(self, task_id: str, task_title: str, success: bool, output: str, duration: float):
        final_state = STATE_DONE if success else STATE_FAILED
        try:
            update_task_status(self.project_id, task_id, final_state)
            status_text = "PASSED ✅" if success else "FAILED ❌"
            add_comment(self.project_id, task_id, f"🤖 Sprint Watcher Result: Tests {status_text} ({duration}s).\n{output[:300]}")
        except Exception as e:
            console.print(f"[yellow]⚠️ Could not update task status: {e}[/yellow]")

        log_task_result(task_id, task_title, "SprintWatcherAgent", "completed" if success else "failed", output, duration)
        update_agent_status("sprint_watcher", "idle", "Sprint Watcher Agent Active (Monitoring)")

    def _handle_new_task(self, task: dict) -> bool:
        task_id = task["id"]
        task_title = task.get("name", "Unknown Task")
        priority = task.get("priority", "medium")
        desc = task.get("description", "")

        start_time = time.time()
        console.print(Panel(f"🔨 New task detected!\nTitle: {task_title}\nID: {task_id}", border_style="cyan"))

        try:
            update_task_status(self.project_id, task_id, STATE_INPROG)
        except Exception:
            pass

        update_agent_status("sprint_watcher", "running", f"⚡ ACTIVE TASK: [{task_id[:8]}] {task_title}")
        build_success = self._run_builder(task_id, task_title, desc, priority)
        test_success, test_output = self._run_tests() if build_success else (False, "Builder failed")
        duration = round(time.time() - start_time, 2)
        self._finalize_task(task_id, task_title, test_success, test_output, duration)
        return test_success

    def watch(self, max_cycles: Optional[int] = None):
        if not self._init_project():
            return

        console.print(Panel.fit("👁️  Sprint Watcher Agent — Running", border_style="magenta"))
        cycle = 0

        while True:
            cycle += 1
            tasks = self._fetch_sprint_tasks()
            render_sprint_table(tasks, cycle, datetime.now().strftime("%H:%M:%S"))

            actionable = [
                t for t in tasks
                if t.get("state_group", "").lower() in ("unstarted", "backlog", "todo", "started", "in_progress")
            ]

            for task in actionable:
                console.print(f"⚡ Processing task: {task.get('name')}")
                self._handle_new_task(task)

            if max_cycles and cycle >= max_cycles:
                break

            time.sleep(self.poll_interval)


if __name__ == "__main__":
    watcher = SprintWatcherAgent(poll_interval_seconds=15)
    watcher.watch(max_cycles=1)
