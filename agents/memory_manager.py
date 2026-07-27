"""
Memory Manager — Handles persistent storage for all agents.
Saves/loads conversation history, task logs, and agent state.
"""

import json
import os
import jsonlines
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional
from rich.console import Console

console = Console()

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent.parent
MEMORY_DIR = ROOT_DIR / "memory"
CONVERSATIONS_DIR = MEMORY_DIR / "conversations"
TASK_HISTORY_DIR = MEMORY_DIR / "task_history"
STATE_FILE = MEMORY_DIR / "agent_state.json"
AGENT_CONFIG_FILE = ROOT_DIR / "config" / "agent_config.json"


def _ensure_dirs():
    """Create memory directories if they don't exist."""
    CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
    TASK_HISTORY_DIR.mkdir(parents=True, exist_ok=True)


# ── Agent State ────────────────────────────────────────────────────────────────

def load_state() -> dict:
    """Load the global agent state from disk."""
    _ensure_dirs()
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state: dict) -> None:
    """Persist the global agent state to disk."""
    _ensure_dirs()
    state["last_updated"] = datetime.now().isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    console.print(f"[green]✅ Agent state saved[/green]")


def update_agent_status(agent_name: str, status: str, task: Optional[str] = None) -> None:
    """Update the status of a specific agent in the state file."""
    state = load_state()
    if "agents" not in state:
        state["agents"] = {}
    if agent_name not in state["agents"]:
        state["agents"][agent_name] = {}
    state["agents"][agent_name]["status"] = status
    state["agents"][agent_name]["last_run"] = datetime.now().isoformat()
    if task:
        state["agents"][agent_name]["current_task"] = task
    save_state(state)


# ── Conversation History ───────────────────────────────────────────────────────

def save_conversation(agent_name: str, messages: list[dict]) -> str:
    """
    Save a conversation session to JSONL file.
    Returns the path to the saved file.
    """
    _ensure_dirs()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{agent_name}.jsonl"
    filepath = CONVERSATIONS_DIR / filename

    with jsonlines.open(filepath, mode="w") as writer:
        for msg in messages:
            msg["_saved_at"] = datetime.now().isoformat()
            writer.write(msg)

    console.print(f"[blue]💾 Conversation saved: {filename}[/blue]")
    return str(filepath)


def load_last_conversation(agent_name: str, max_messages: int = 50) -> list[dict]:
    """
    Load the most recent conversation for a given agent.
    Returns list of messages for context restoration.
    """
    _ensure_dirs()
    # Find the most recent file for this agent
    agent_files = sorted(
        [f for f in CONVERSATIONS_DIR.glob(f"*_{agent_name}.jsonl")],
        reverse=True
    )

    if not agent_files:
        console.print(f"[yellow]⚠️  No previous conversation for {agent_name}[/yellow]")
        return []

    latest_file = agent_files[0]
    messages = []

    with jsonlines.open(latest_file) as reader:
        for line in reader:
            messages.append(line)

    # Trim to max_messages (keep most recent)
    messages = messages[-max_messages:]
    console.print(f"[blue]📂 Loaded {len(messages)} messages for {agent_name}[/blue]")
    return messages


def load_all_conversations(agent_name: str, days: int = 7) -> list[dict]:
    """Load all conversations for an agent within the last N days."""
    _ensure_dirs()
    cutoff = datetime.now() - timedelta(days=days)
    all_messages = []

    for filepath in sorted(CONVERSATIONS_DIR.glob(f"*_{agent_name}.jsonl")):
        # Parse date from filename: YYYY-MM-DD_HH-MM-SS_agent.jsonl
        try:
            date_str = filepath.stem.split("_")[0]
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if file_date >= cutoff:
                with jsonlines.open(filepath) as reader:
                    all_messages.extend(list(reader))
        except (ValueError, IndexError):
            continue

    return all_messages


# ── Task History ───────────────────────────────────────────────────────────────

def log_task_result(
    task_id: str,
    task_title: str,
    agent_name: str,
    status: str,
    output: str,
    files_changed: list[str] = None,
    test_results: dict = None
) -> None:
    """
    Log the result of a task to the task history directory.
    Used for auditing and context by the orchestrator.
    """
    _ensure_dirs()
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}_task_history.jsonl"
    filepath = TASK_HISTORY_DIR / filename

    record = {
        "task_id": task_id,
        "task_title": task_title,
        "agent": agent_name,
        "status": status,  # "completed" | "failed" | "in_progress"
        "output": output,
        "files_changed": files_changed or [],
        "test_results": test_results or {},
        "timestamp": datetime.now().isoformat()
    }

    with jsonlines.open(filepath, mode="a") as writer:
        writer.write(record)

    icon = "✅" if status == "completed" else "❌" if status == "failed" else "🔄"
    console.print(f"[cyan]{icon} Task logged: {task_title} [{status}][/cyan]")


def load_task_history(days: int = 7) -> list[dict]:
    """Load task history from the last N days."""
    _ensure_dirs()
    cutoff = datetime.now() - timedelta(days=days)
    all_records = []

    for filepath in sorted(TASK_HISTORY_DIR.glob("*.jsonl")):
        try:
            date_str = filepath.stem.replace("_task_history", "")
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if file_date >= cutoff:
                with jsonlines.open(filepath) as reader:
                    all_records.extend(list(reader))
        except (ValueError, IndexError):
            continue

    return all_records


def get_todays_summary() -> dict:
    """Get a summary of what was done today."""
    today = datetime.now().strftime("%Y-%m-%d")
    history = [r for r in load_task_history(days=1)
               if r.get("timestamp", "").startswith(today)]

    completed = [r for r in history if r["status"] == "completed"]
    failed = [r for r in history if r["status"] == "failed"]
    all_files = []
    for r in history:
        all_files.extend(r.get("files_changed", []))

    return {
        "date": today,
        "tasks_completed": len(completed),
        "tasks_failed": len(failed),
        "files_changed": list(set(all_files)),
        "details": history
    }


# ── Cleanup ────────────────────────────────────────────────────────────────────

def cleanup_old_memory(retention_days: int = 30) -> None:
    """Delete conversation and task history files older than retention_days."""
    _ensure_dirs()
    cutoff = datetime.now() - timedelta(days=retention_days)

    for directory in [CONVERSATIONS_DIR, TASK_HISTORY_DIR]:
        for filepath in directory.glob("*.jsonl"):
            try:
                date_str = filepath.stem.split("_")[0]
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                if file_date < cutoff:
                    filepath.unlink()
                    console.print(f"[dim]🗑️  Deleted old memory: {filepath.name}[/dim]")
            except (ValueError, IndexError):
                continue


if __name__ == "__main__":
    # Quick test
    console.print("[bold green]Memory Manager Test[/bold green]")
    state = load_state()
    console.print(f"State keys: {list(state.keys())}")
    update_agent_status("orchestrator", "running", "Test task")
    log_task_result("TASK-001", "Test Task", "orchestrator", "completed", "All good!")
    summary = get_todays_summary()
    console.print(f"Today's summary: {summary}")
