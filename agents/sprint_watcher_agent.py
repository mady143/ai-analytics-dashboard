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

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "agents"))
load_dotenv(ROOT_DIR / ".env")
console = Console(legacy_windows=False)

# ── Imports from sibling agents ──────────────────────────────────────────────
from plane_agent import (
    get_or_create_project,
    list_tasks,
    list_sprints,
    get_states,
    update_task_status,
    add_comment,
    create_task,
    list_comments,
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
STATE_DONE      = "done"          # Tested and merged
STATE_FAILED    = "cancelled"     # Tests failed — needs review
STATE_BACKLOG   = "backlog"       # Not yet in sprint


def trigger_automated_git_push():
    """Disabled continuous pushes. Pushes only run at daily EOD cycle when changes exist."""
    console.print("[dim]Continuous Git push disabled (Pushes occur on daily EOD cycle only when code changes exist).[/dim]")


class SprintWatcherAgent:
    """
    Watches the active Plane sprint and drives the full task lifecycle:
    Todo → In Progress (Builder writes code) → Tests → Done / Failed
    """

    def __init__(self, poll_interval_seconds: int = 15):
        """
        Args:
            poll_interval_seconds: How often to poll Plane for task changes.
                                   Default = 15 seconds.
        """
        self.poll_interval = poll_interval_seconds
        self.project_id: Optional[str] = None
        self.current_sprint_id: Optional[str] = None
        self.state = load_state()
        # Track last-seen state per task ID (not just IDs)
        # This allows re-picking tasks when they are reset/updated in Plane
        self._last_seen_state: dict[str, str] = {}   # task_id -> last state string
        self._last_seen_updated: dict[str, str] = {} # task_id -> last updated_at
        self._last_seen_comment_ids: dict[str, set] = {}  # task_id -> set of seen comment IDs
        self._completed_task_ids: set[str] = set()
        # Dynamic Test Timeout (None = unlimited dynamic timeout until all tests finish, or int from env)
        env_timeout = os.getenv("TEST_TIMEOUT_SECONDS", "0").strip()
        self.test_timeout: Optional[int] = int(env_timeout) if env_timeout and env_timeout.isdigit() and int(env_timeout) > 0 else None

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

        update_agent_status(
            "sprint_watcher",
            "running",
            f"⚡ ACTIVE TASK: [{task_id[:8]}] {task_title}"
        )

        # Write picked-up task to agent_state active_tasks for live UI display
        try:
            state = load_state()
            active_entry = {
                "task_id": task_id,
                "title": task_title,
                "priority": priority,
                "picked_up_at": datetime.now().isoformat(),
                "phase": "Building"
            }
            active_tasks = state.get("active_tasks", [])
            # Remove any previous entry for this task ID
            active_tasks = [t for t in active_tasks if t.get("task_id") != task_id]
            active_tasks.insert(0, active_entry)
            state["active_tasks"] = active_tasks[:5]  # Keep last 5
            save_state(state)
        except Exception as e:
            console.print(f"[dim]State update error: {e}[/dim]")

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
        priority: str
    ) -> bool:
        """
        Invoke the Builder Agent as a subprocess.
        Dynamically updates builder status to running during execution, and idle on completion.
        """
        builder_script = ROOT_DIR / "agents" / "builder_agent.py"
        console.print(f"[cyan]🔨 Invoking Builder Agent for: {task_title}[/cyan]")
        update_agent_status(
            "builder",
            "running",
            f"🔨 Implementing [{task_id[:8]}]: {task_title}"
        )

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
                timeout=300,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            stdout = result.stdout or ""
            stderr = result.stderr or ""

            if result.returncode == 0:
                console.print(f"[green]✅ Builder completed: {task_title}[/green]")
                log_task_result(task_id, task_title, "builder", "completed", stdout[-2000:])
                update_agent_status("builder", "idle")
                return True
            else:
                console.print(f"[red]❌ Builder failed: {task_title}[/red]")
                console.print(stderr[-1000:])
                log_task_result(task_id, task_title, "builder", "failed", stderr[-2000:])
                update_agent_status("builder", "idle")
                return False

        except subprocess.TimeoutExpired:
            console.print(f"[red]⏱️  Builder timed out for: {task_title}[/red]")
            log_task_result(task_id, task_title, "builder", "failed", "Timeout after 300s")
            update_agent_status("builder", "idle")
            return False
        except FileNotFoundError:
            console.print(f"[yellow]⚠️  builder_agent.py not found[/yellow]")
            log_task_result(task_id, task_title, "builder", "skipped", "builder_agent.py not yet created")
            update_agent_status("builder", "idle")
            return False

    def _run_tests(self) -> tuple[bool, str]:
        """
        Run unit tests and Playwright browser tests via pytest.
        Dynamically updates tester status to running during test execution, and idle on completion.
        Executes BOTH unit tests and Playwright browser tests.
        """
        timeout_msg = f"{self.test_timeout}s" if self.test_timeout else "unlimited (dynamic)"
        console.print(f"[cyan]🧪 Running Unit Tests & Playwright Browser Tests (Timeout: {timeout_msg})...[/cyan]")
        update_agent_status("tester", "running", "Executing Pytest Unit & Playwright Browser tests")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "tests/unit/", "tests/browser/", "-v", "--tb=short"],
                cwd=str(ROOT_DIR),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.test_timeout,
            )
            stdout = result.stdout or ""
            stderr = result.stderr or ""
            output = stdout + stderr
            passed = result.returncode == 0
            if passed:
                console.print("[green]✅ Unit & Playwright Browser Tests PASSED[/green]")
            else:
                console.print("[red]❌ Test Execution FAILED[/red]")
            update_agent_status("tester", "idle")
            return passed, output[-3000:]
        except subprocess.TimeoutExpired:
            console.print(f"[yellow]⚠️ Tests TIMED OUT after {timeout_msg}[/yellow]")
            update_agent_status("tester", "idle")
            return False, f"Tests timed out after {timeout_msg}"
        except Exception as e:
            console.print(f"[red]❌ Test execution error: {e}[/red]")
            update_agent_status("tester", "idle")
            return False, str(e)

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

        # Update state tracking so this task isn't re-triggered until Plane changes it again
        self._last_seen_state[task_id] = STATE_DONE if success else STATE_FAILED
        self._last_seen_updated[task_id] = datetime.now().isoformat()
        if success:
            self._completed_task_ids.add(task_id)

        # Clear active_tasks entry for this task — it's done
        try:
            state = load_state()
            active_tasks = state.get("active_tasks", [])
            active_tasks = [t for t in active_tasks if t.get("task_id") != task_id]
            state["active_tasks"] = active_tasks
            save_state(state)
        except Exception:
            pass

        # Update sprint_watcher status back to polling idle
        update_agent_status(
            "sprint_watcher",
            "running",
            f"{'✅ Completed' if success else '❌ Failed'}: {task_title} — watching for next task"
        )

        # Note: Continuous auto-push after every task disabled per configuration. Pushes execute on daily EOD schedule if code changes exist.

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

            if "complet" in state and self._last_seen_state.get(task_id) != state:
                log_task_result(
                    task_id,
                    task.get("name", "Unknown"),
                    "sprint_watcher",
                    "completed",
                    "Synced from Plane — already marked completed.",
                )
                self._last_seen_state[task_id] = state
                console.print(
                    f"[dim]🔄 Synced completed task: {task.get('name', task_id)[:50]}[/dim]"
                )

    # ── Comment Polling ───────────────────────────────────────────────────────

    def _check_new_comments(self, tasks: list[dict]) -> list[tuple[dict, str]]:
        """
        Poll comments on every non-completed task.
        Returns list of (task, new_comment_text) for each newly detected comment.
        New comments from the bot itself (containing '🤖') are ignored.
        """
        new_comment_items = []
        for task in tasks:
            task_id    = task["id"]
            task_state = self._get_task_state(task)
            # Only watch active / open tasks for new comments
            if task_state in (STATE_DONE, "completed", "done"):
                continue

            comments = list_comments(self.project_id, task_id)
            seen_ids = self._last_seen_comment_ids.get(task_id, set())

            for comment in comments:
                cid  = comment.get("id", "")
                text = comment.get("comment_stripped") or comment.get("comment") or ""
                # Skip bot-generated comments and already-seen ones
                if cid in seen_ids or "🤖" in text or "Sprint Watcher" in text:
                    seen_ids.add(cid)
                    continue
                if text.strip():
                    console.print(
                        f"[bold magenta]💬 New comment on '{task.get('name','?')[:40]}':[/bold magenta]\n"
                        f"   {text[:200]}"
                    )
                    new_comment_items.append((task, text))
                seen_ids.add(cid)

            self._last_seen_comment_ids[task_id] = seen_ids

        return new_comment_items

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
                now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                console.rule(
                    f"[dim]Poll #{cycle} — {now_str}[/dim]"
                )
                update_agent_status(
                    "sprint_watcher",
                    "running",
                    f"Watching sprint (Poll #{cycle} @ {datetime.now().strftime('%H:%M:%S')})"
                )

                tasks = self._fetch_sprint_tasks()

                if tasks:
                    self._print_sprint_table(tasks)
                    self._sync_completed_tasks(tasks)

                    # ── Comment detection: pick up new user instructions ───────
                    new_comment_items = self._check_new_comments(tasks)
                    for (commented_task, comment_text) in new_comment_items:
                        console.print(
                            f"[bold magenta]📋 Processing comment instruction for: "
                            f"{commented_task.get('name','?')[:50]}[/bold magenta]"
                        )
                        # Inject comment text into the task description so builder sees it
                        enriched_task = dict(commented_task)
                        existing_desc = enriched_task.get("description", "") or ""
                        enriched_task["description"] = (
                            existing_desc + f"\n\n---\n**New instruction from comment:**\n{comment_text}"
                        )
                        self._handle_new_task(enriched_task)

                    # Identify actionable tasks:
                    # RULE: Only pick up tasks that are in UNSTARTED / BACKLOG state.
                    # Tasks already in-progress (started) or done/cancelled are SKIPPED.
                    # Re-trigger is allowed ONLY if:
                    #   1. Task is brand new (never seen) AND is in unstarted/backlog
                    #   2. Task state was reset back to unstarted (user re-opened it)
                    #   3. Task content/description was updated AND task is unstarted
                    actionable_tasks = []
                    ACTIONABLE_STATES = (STATE_TODO, STATE_BACKLOG, "unstarted", "backlog", "todo")
                    SKIP_STATES = (STATE_DONE, STATE_INPROG, "completed", "done", "started", "in progress", "cancelled")

                    for t in tasks:
                        task_id       = t["id"]
                        current_state = self._get_task_state(t)
                        updated_at    = t.get("updated_at") or t.get("updated", "")
                        last_state    = self._last_seen_state.get(task_id)
                        last_updated  = self._last_seen_updated.get(task_id)

                        # Always update tracking
                        self._last_seen_state[task_id] = current_state
                        self._last_seen_updated[task_id] = updated_at

                        # Skip tasks already completed by agent in this session
                        if task_id in self._completed_task_ids:
                            continue

                        # Skip tasks NOT in an actionable state (e.g. already started/done/cancelled)
                        if current_state in SKIP_STATES:
                            continue

                        # Only process if task is in an actionable (unstarted/backlog) state
                        if current_state not in ACTIONABLE_STATES:
                            console.print(f"[dim]⏭ Skipping task in state '{current_state}': {t.get('name','?')[:40]}[/dim]")
                            continue

                        # Determine the reason this task should be actioned
                        is_new            = last_state is None
                        reset_to_unstarted = last_state and last_state not in ACTIONABLE_STATES and current_state in ACTIONABLE_STATES
                        content_updated   = last_updated and updated_at and last_updated != updated_at and current_state in ACTIONABLE_STATES

                        if is_new or reset_to_unstarted or content_updated:
                            reason = (
                                "new unstarted task" if is_new
                                else "reset to unstarted" if reset_to_unstarted
                                else "content updated"
                            )
                            console.print(
                                f"[bold yellow]⚡ Actionable task ({reason}): "
                                f"{t.get('name', task_id)[:50]}[/bold yellow]"
                            )
                            actionable_tasks.append(t)

                    # Sort by priority: urgent → high → medium → low
                    priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3, "none": 4}
                    actionable_tasks.sort(
                        key=lambda t: priority_order.get(t.get("priority", "none"), 4)
                    )

                    if actionable_tasks:
                        console.print(
                            f"[bold yellow]⚡ {len(actionable_tasks)} task(s) to process![/bold yellow]"
                        )
                        for task in actionable_tasks:
                            self._handle_new_task(task)
                    else:
                        console.print("[dim]✓ No new or updated tasks — all up to date.[/dim]")
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
        default=15,
        help="Poll interval in seconds (default: 15)",
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
