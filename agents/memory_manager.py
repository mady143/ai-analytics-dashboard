"""
Memory Manager — Manages persistent agent conversation state, task history, and logging.
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from rich.console import Console

ROOT_DIR = Path(__file__).parent.parent
MEMORY_DIR = ROOT_DIR / "memory"
CONVERSATIONS_DIR = MEMORY_DIR / "conversations"
TASK_HISTORY_DIR = MEMORY_DIR / "task_history"
STATE_FILE = MEMORY_DIR / "agent_state.json"

console = Console()


def _ensure_dirs():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
    TASK_HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def load_state() -> dict:
    _ensure_dirs()
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "agents": {},
        "current_sprint": None,
        "plane_project_id": None,
        "plane_workspace_slug": "agentbuilder",
        "last_active": datetime.now().isoformat()
    }


def save_state(state: dict):
    _ensure_dirs()
    state["last_active"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def update_agent_status(agent_name: str, status: str, current_task: Optional[str] = None):
    state = load_state()
    if "agents" not in state:
        state["agents"] = {}
    state["agents"][agent_name] = {
        "status": status,
        "current_task": current_task,
        "updated_at": datetime.now().isoformat()
    }
    save_state(state)


def log_task_result(
    task_id: str,
    task_title: str,
    agent_name: str,
    status: str,
    output: str,
    test_results: Optional[dict] = None
):
    _ensure_dirs()
    today_str = datetime.now().strftime("%Y-%m-%d")
    history_file = TASK_HISTORY_DIR / f"{today_str}_task_history.jsonl"

    record = {
        "timestamp": datetime.now().isoformat(),
        "task_id": task_id,
        "task_title": task_title,
        "agent": agent_name,
        "status": status,
        "output_snippet": output[-1000:] if output else "",
        "test_results": test_results or {}
    }

    with history_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def get_todays_summary() -> dict:
    _ensure_dirs()
    today_str = datetime.now().strftime("%Y-%m-%d")
    history_file = TASK_HISTORY_DIR / f"{today_str}_task_history.jsonl"

    tasks_completed = 0
    tasks_failed = 0
    details = []

    if history_file.exists():
        with history_file.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        rec = json.loads(line.strip())
                        details.append(rec)
                        if rec.get("status") == "completed":
                            tasks_completed += 1
                        elif rec.get("status") == "failed":
                            tasks_failed += 1
                    except Exception:
                        pass

    try:
        import subprocess
        res = subprocess.run(["git", "status", "--porcelain"], cwd=str(ROOT_DIR), capture_output=True, text=True)
        files_changed = [line.strip().split()[-1] for line in res.stdout.strip().split("\n") if line.strip()]
    except Exception:
        files_changed = []

    return {
        "date": today_str,
        "tasks_completed": tasks_completed,
        "tasks_failed": tasks_failed,
        "files_changed": files_changed,
        "details": details
    }


def cleanup_old_memory(retention_days: int = 30):
    _ensure_dirs()
    cutoff = datetime.now() - timedelta(days=retention_days)
    for folder in [CONVERSATIONS_DIR, TASK_HISTORY_DIR]:
        for filepath in folder.glob("*.jsonl"):
            try:
                mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                if mtime < cutoff:
                    filepath.unlink()
                    console.print(f"[dim]Deleted old memory: {filepath.name}[/dim]")
            except Exception:
                pass


if __name__ == "__main__":
    console.print(f"Memory Manager status: {load_state()}")
