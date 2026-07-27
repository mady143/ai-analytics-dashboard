"""
Sprint Watcher Agent — Continuously monitors Plane sprint activity.

RESPONSIBILITIES:
  1. Poll Plane every N minutes for the current sprint's task list
  2. NEW TASK detected    → trigger Builder Agent to implement it
                           → update Plane: "In Progress"
  3. IMPLEMENTATION done  → trigger Tester Agent to run tests
  4. TESTS PASS           → update Plane: "Done" + add result comment
  5. TESTS FAIL           → update Plane: "Failed" + add error comment
                           → re-queue task for Builder to fix

FLOW:
  Plane (sprint tasks)
       │
       ▼
  sprint_watcher_agent.py  ──► builder_agent.py  (writes code)
       │                              │
       │                             ▼
       │                    tester_agent.py  (pytest + playwright)
       │                              │
       └──────────────────────────────┤
                                      ▼
                              plane_agent.py  (mark Done / Failed)
                              memory_manager.py (log result)
"""

import os
import sys
import json
import time
import subprocess
import importlib
from pathlib import Path
from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "agents"))
load_dotenv(ROOT_DIR / ".env")
console = Console()

# ── Imports from sibling agents ──────────────────────────────────────────────
from plane_agent import (
    get_or_create_project,
    list_tasks,
    list_sprints,
    get_states,
    update_task_status,
    add_comment,
    create_task,
)
from memory_manager import (
    update_agent_status,
    log_task_result,
    load_state,
    save_state,
)


# ── State machine for task lifecycle ─────────────────────────────────────────
# Plane state names we care about (case-insensitive matching)
STATE_TODO      = "unstarted"     # Newly added task
STATE_INPROG    = "started"       # Being worked on by Builder
STATE_DONE      = "completed"     # Tested and merged
STATE_FAILED    = "cancelled"     # Tests failed — needs review
STATE_BACKLOG   = "backlog"       # Not yet in sprint


class SprintWatcherAgent:
    """
    Watches the active Plane sprint and drives the full task lifecycle:
    Todo → In Progress (Builder writes code) → Tests → Done / Failed
    """

    def __init__(self, poll_interval_seconds: int = 120):
        """
        Args:
            poll_interval_seconds: How often to poll Plane for task changes.
                                   Default = 2 minutes.
        """
        self.poll_interval = poll_interval_seconds
        self.project_id: Optional[str] = None
        self.current_sprint_id: Optional[str] = None
        self.state = load_state()
        # Track which tasks we've already acted on this session
        self._processed_task_ids: set[str] = set()

    # ── Initialisation ────────────────────────────────────────────────────────

    def _init_project(self) -> bool:
        """Resolve Plane project ID from state or API."""
        self.project_id = self.state.get("plane_project_id")
        if not self.project_id:
            token = os.getenv("PLANE_API_TOKEN", "")
            if not token or token == "your_plane_api_token_here":
                console.print("[red]❌ PLANE_API_TOKEN not set — Sprint Watcher cannot run.[/red]")
                console.print("[dim]Set it in .env and re-run.[/dim]")
                return False
            try:
                self.project_id = get_or_create_project()
                self.state["plane_project_id"] = self.project_id
                save_state(self.state)
            except Exception as e:
                console.print(f"[red]❌ Could not connect to Plane: {e}[/red]")
                return False
        return True

    def _resolve_active_sprint(self) -> Optional[dict]:
        """
        Find the earliest non-completed sprint cycle.
        Returns the sprint dict or None.
        """
        try:
            sprints = list_sprints(self.project_id)
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not fetch sprints: {e}[/yellow]")
            return None

        if not sprints:
            console.print("[yellow]⚠️  No sprints found in Plane. Run setup first.[/yellow]")
            return None

        # Return first sprint that is not ended
        today = datetime.now().date().isoformat()
        for sprint in sprints:
            end = sprint.get("end_date") or ""
            if end >= today:
                return sprint

        # Fallback: return last sprint
        return sprints[-1]

    # ── Task Fetching ─────────────────────────────────────────────────────────

    def _fetch_sprint_tasks(self) -> list[dict]:
        """Fetch all tasks in the current sprint with their states."""
        try:
            return list_tasks(self.project_id)
        except Exception as e:
            console.print(f"[yellow]⚠️  Failed to fetch tasks: {e}[/yellow]")
            return []

    def _get_task_state(self, task: dict) -> str:
        """Normalise the task state to one of our STATE_* constants."""
        if task.get("state_group"):
            return task.get("state_group").lower()
        state_detail = task.get("state_detail")
        if isinstance(state_detail, dict) and state_detail.get("name"):
            return state_detail.get("name").lower()
        return str(task.get("state", "")).lower()

    def _print_sprint_table(self, tasks: list[dict]):
        """Render a Rich table of current sprint tasks."""
        table = Table(
            title=f"📋 Sprint Status — {datetime.now().strftime('%H:%M:%S')}",
            expand=False,
        )
        table.add_column("Priority", style="bold", width=10)
        table.add_column("Task", style="cyan", min_width=40)
        table.add_column("State", width=14)
        table.add_column("Points", width=6, justify="right")

        priority_colors = {
            "urgent": "red",
            "high": "orange3",
            "medium": "yellow",
            "low": "dim",
            "none": "dim",
        }
        state_colors = {
            "completed": "green",
            "started": "cyan",
            "unstarted": "white",
            "backlog": "dim",
            "cancelled": "red",
        }

        for task in tasks:
            priority = task.get("priority", "none").lower()
            state    = self._get_task_state(task)
            name     = task.get("name", "Unnamed")[:55]
            pts      = str(task.get("estimate_point") or "—")

            p_color = priority_colors.get(priority, "white")
            s_color = state_colors.get(state, "white")

            table.add_row(
                f"[{p_color}]{priority.upper()}[/{p_color}]",
                name,
                f"[{s_color}]{state}[/{s_color}]",
                pts,
            )

        console.print(table)

    # ── Task Lifecycle ────────────────────────────────────────────────────────

    def _handle_new_task(self, task: dict) -> bool:
        """
        Called when a task in TODO / UNSTARTED state is detected.
        Triggers the Builder agent subprocess, then hands off to tester.
        Returns True if the task was successfully completed.
        """
        task_id    = task["id"]
        task_title = task.get("name", "Unknown Task")
        priority   = task.get("priority", "medium")
        desc       = task.get("description_html", "") or task.get("description", "")

        start_time = time.time()
        console.print(Panel(
            f"[bold cyan]🔨 New task detected![/bold cyan]\n\n"
            f"  Title:    {task_title}\n"
            f"  Priority: {priority.upper()}\n"
            f"  ID:       {task_id}\n"
            f"  Start:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            border_style="cyan",
        ))

        # ── Step 1: Mark as In Progress ──────────────────────────────────────
        try:
            update_task_status(self.project_id, task_id, STATE_INPROG)
            add_comment(
                self.project_id, task_id,
                f"🤖 Sprint Watcher picked up this task at "
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Builder Agent is working on it."
            )
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not update Plane status: {e}[/yellow]")

        update_agent_status("sprint_watcher", "running", task_title)

        # ── Step 2: Invoke Builder Agent ──────────────────────────────────────
        build_success = self._run_builder(task_id, task_title, desc, priority)

        # ── Step 3: Run Tests ─────────────────────────────────────────────────
        if build_success:
            test_success, test_output = self._run_tests()
        else:
            test_success = False
            test_output  = "Builder agent failed to implement the task."

        duration_seconds = round(time.time() - start_time, 2)

        # ── Step 4: Update Plane based on result ──────────────────────────────
        self._finalize_task(task_id, task_title, test_success, test_output, duration_seconds)
        return test_success

    def _run_builder(
        self,
        task_id: str,
        task_title: str,
        description: str,
        priority: str,
    ) -> bool:
        """
        Invoke the Builder Agent as a subprocess.
        The builder writes/updates code based on the task description.
        Returns True if it exited successfully.
        """
        builder_script = ROOT_DIR / "agents" / "builder_agent.py"

        console.print(f"[cyan]🔨 Invoking Builder Agent for: {task_title}[/cyan]")

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(builder_script),
                    "--task-id",    task_id,
                    "--task-title", task_title,
                    "--description", description or "",
                    "--priority",   priority,
                ],
                cwd=str(ROOT_DIR),
                timeout=300,          # 5-minute timeout per task
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            stdout = result.stdout or ""
            stderr = result.stderr or ""

            if result.returncode == 0:
                console.print(f"[green]✅ Builder completed: {task_title}[/green]")
                log_task_result(
                    task_id, task_title, "builder", "completed",
                    stdout[-2000:],
                )
                return True
            else:
                console.print(f"[red]❌ Builder failed: {task_title}[/red]")
                console.print(stderr[-1000:])
                log_task_result(
                    task_id, task_title, "builder", "failed",
                    stderr[-2000:],
                )
                return False

        except subprocess.TimeoutExpired:
            console.print(f"[red]⏱️  Builder timed out for: {task_title}[/red]")
            log_task_result(task_id, task_title, "builder", "failed", "Timeout after 300s")
            return False
        except FileNotFoundError:
            # builder_agent.py may not exist yet; log and skip gracefully
            console.print(
                f"[yellow]⚠️  builder_agent.py not found — "
                f"task '{task_title}' will be logged but not auto-implemented.[/yellow]"
            )
            log_task_result(task_id, task_title, "builder", "skipped",
                            "builder_agent.py not yet created")
            return False

    def _run_tests(self) -> tuple[bool, str]:
        """
        Run unit tests via pytest.
        Returns (passed: bool, output: str).
        """
        console.print("[cyan]🧪 Running tests after implementation...[/cyan]")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/unit/", "-q", "--tb=short"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        output = stdout + stderr
        passed = result.returncode == 0
        if passed:
            console.print("[green]✅ Tests PASSED[/green]")
        else:
            console.print("[red]❌ Tests FAILED[/red]")
        return passed, output[-3000:]

    def _finalize_task(
        self,
        task_id: str,
        task_title: str,
        success: bool,
        test_output: str,
        duration_seconds: float = 0.0,
    ):
        """Mark task Done or Failed in Plane and log the result with execution duration."""
        new_state = STATE_DONE if success else STATE_FAILED
        status_label = "completed" if success else "failed"
        icon = "✅" if success else "❌"

        comment = (
            f"{icon} Task **{status_label.upper()}** by Sprint Watcher Agent\n\n"
            f"📅 **Date & Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"⏱️ **End-to-End Execution Time:** {duration_seconds}s\n\n"
            f"**Test Output (last 500 chars):**\n```\n{test_output[-500:]}\n```"
        )

        try:
            update_task_status(self.project_id, task_id, new_state)
            add_comment(self.project_id, task_id, comment)
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not update Plane: {e}[/yellow]")

        log_task_result(
            task_id, task_title, "sprint_watcher", status_label,
            f"Duration: {duration_seconds}s | {test_output}", test_results={"passed": success, "duration_seconds": duration_seconds},
        )

        self._processed_task_ids.add(task_id)

        # ── Step 5: Automatically commit and push code if task passed ──────────
        if success:
            try:
                from git_agent import eod_push
                console.print(f"[bold cyan]🔀 Auto-committing and pushing code for completed task: {task_title}[/bold cyan]")
                eod_push(
                    tasks_completed=[task_title],
                    custom_summary=f"Automated completion of sprint task: {task_title}"
                )
            except Exception as e:
                console.print(f"[yellow]⚠️  Git push skipped/failed: {e}[/yellow]")

        console.print(Panel(
            f"[bold {'green' if success else 'red'}]{icon} Task {status_label.upper()}[/bold {'green' if success else 'red'}]\n"
            f"  {task_title}\n"
            f"  Plane status → {new_state}",
            border_style="green" if success else "red",
        ))

    # ── Completed Task Sync ───────────────────────────────────────────────────

    def _sync_completed_tasks(self, tasks: list[dict]):
        """
        For tasks already marked "completed" on Plane but not logged locally,
        ensure memory is up to date.
        """
        for task in tasks:
            task_id = task["id"]
            state   = self._get_task_state(task)

            if "complet" in state and task_id not in self._processed_task_ids:
                log_task_result(
                    task_id,
                    task.get("name", "Unknown"),
                    "sprint_watcher",
                    "completed",
                    "Synced from Plane — already marked completed.",
                )
                self._processed_task_ids.add(task_id)
                console.print(
                    f"[dim]🔄 Synced completed task: {task.get('name', task_id)[:50]}[/dim]"
                )

    # ── Main Loop ─────────────────────────────────────────────────────────────

    def watch(self, max_cycles: int = 0):
        """
        Start the sprint watch loop.

        Args:
            max_cycles: If > 0, stop after this many poll cycles (useful for testing).
                        If 0 (default), run indefinitely.
        """
        console.print(Panel.fit(
            "[bold magenta]👁️  Sprint Watcher Agent — Starting[/bold magenta]\n"
            f"[dim]Poll interval: every {self.poll_interval}s | "
            f"Press Ctrl+C to stop[/dim]",
            border_style="magenta",
        ))

        if not self._init_project():
            return

        update_agent_status("sprint_watcher", "running", "Watching sprint")

        sprint = self._resolve_active_sprint()
        if sprint:
            self.current_sprint_id = sprint.get("id")
            console.print(
                f"[green]✅ Active sprint: [bold]{sprint.get('name')}[/bold][/green]"
            )
        else:
            console.print("[yellow]⚠️  No active sprint found — watching all tasks[/yellow]")

        cycle = 0
        try:
            while True:
                cycle += 1
                console.rule(
                    f"[dim]Poll #{cycle} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]"
                )

                tasks = self._fetch_sprint_tasks()

                if tasks:
                    self._print_sprint_table(tasks)
                    self._sync_completed_tasks(tasks)

                    # Identify NEW tasks (unstarted / todo, not yet processed)
                    new_tasks = [
                        t for t in tasks
                        if self._get_task_state(t) in (STATE_TODO, STATE_BACKLOG, "")
                        and t["id"] not in self._processed_task_ids
                    ]

                    # Sort by priority: urgent → high → medium → low
                    priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3, "none": 4}
                    new_tasks.sort(
                        key=lambda t: priority_order.get(t.get("priority", "none"), 4)
                    )

                    if new_tasks:
                        console.print(
                            f"[bold yellow]⚡ {len(new_tasks)} new task(s) detected![/bold yellow]"
                        )
                        for task in new_tasks:
                            self._handle_new_task(task)
                    else:
                        console.print("[dim]✓ No new tasks — all up to date.[/dim]")
                else:
                    console.print("[dim]No tasks found in this sprint.[/dim]")

                if max_cycles and cycle >= max_cycles:
                    console.print(
                        f"[dim]Reached max_cycles={max_cycles}. Stopping.[/dim]"
                    )
                    break

                console.print(
                    f"[dim]💤 Next poll in {self.poll_interval}s...[/dim]\n"
                )
                time.sleep(self.poll_interval)

        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️  Sprint Watcher stopped by user.[/yellow]")
        finally:
            update_agent_status("sprint_watcher", "idle")


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Sprint Watcher Agent — monitors Plane sprint and drives task lifecycle"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=120,
        help="Poll interval in seconds (default: 120)",
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=0,
        help="Max poll cycles before stopping (0 = run forever)",
    )
    args = parser.parse_args()

    watcher = SprintWatcherAgent(poll_interval_seconds=args.interval)
    watcher.watch(max_cycles=args.cycles)
