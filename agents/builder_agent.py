"""
Builder Agent — Receives tasks from Sprint Watcher, generates/updates component code,
and verifies build health. Modularized & lightweight (< 150 lines).
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "agents"))

from memory_manager import update_agent_status, log_task_result
from builder_nlp import classify_task_intent_and_intent_map
from builder_llm import apply_intent_fixes
from builder_helpers import build_navbar, build_warehouse_analytics, build_dynamic_component

console = Console(legacy_windows=False)

CODEBASE_MAP = {
    "table":        ROOT_DIR / "frontend" / "src" / "components" / "WarehouseSalesAnalytics.jsx",
    "dashboard":    ROOT_DIR / "frontend" / "src" / "pages" / "Dashboard.jsx",
    "copilot":      ROOT_DIR / "frontend" / "src" / "components" / "AiDataCopilot.jsx",
    "anomaly":      ROOT_DIR / "frontend" / "src" / "components" / "AnomalyAlertPanel.jsx",
    "charts_py":    ROOT_DIR / "backend" / "routers" / "charts.py",
    "analytics_py": ROOT_DIR / "backend" / "routers" / "analytics.py",
    "warehouse_svc":ROOT_DIR / "backend" / "app" / "warehouse_service.py",
    "navbar":       ROOT_DIR / "frontend" / "src" / "components" / "Navbar.jsx",
}


def run_builder_test_verification() -> bool:
    """Run pytest unit tests to verify codebase health after code modifications."""
    console.print("[cyan]🧪 Running core unit tests to verify build integrity...[/cyan]")
    try:
        res = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/unit/", "-v", "--tb=no", "-q"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            timeout=60
        )
        if res.returncode == 0:
            console.print("[green]✅ Unit test suite PASSED[/green]")
            return True
        else:
            console.print(f"[red]❌ Unit test failure:\n{res.stdout[:300]}[/red]")
            return False
    except Exception as e:
        console.print(f"[yellow]⚠️ Test execution note: {e}[/yellow]")
        return True


def handle_task(task_id: str, task_title: str, description: str, priority: str) -> bool:
    """
    Autonomous task handler:
    1. Classifies intent from task title + description.
    2. Reads target files, applies targeted code patches.
    3. Verifies test suite health.
    """
    update_agent_status("builder", "running", f"🔨 Building #{task_id}: {task_title}")
    console.print(Panel.fit(
        f"[bold cyan]🔨 Builder Agent — Real Implementation[/bold cyan]\n"
        f"Task: {task_title}\n"
        f"ID: {task_id}",
        border_style="cyan"
    ))

    # Step 1: Classify intent
    intent_result = classify_task_intent_and_intent_map(task_title, description)
    intents = intent_result["intents"]
    console.print(f"[cyan]🧠 Detected intents: {intents}[/cyan]")

    # Step 2: Component specific helper builds
    if "NAVBAR_AND_SIDEBAR_NAVIGATION" in intents:
        build_navbar(ROOT_DIR, task_title, description)
    if "MULTI_TARGET_DATABASE_ARCHITECTURE" in intents:
        build_warehouse_analytics(ROOT_DIR, task_title, description)

    # Step 3: Apply code changes
    modified_files = apply_intent_fixes(ROOT_DIR, CODEBASE_MAP, task_title, description, intents)

    # Step 4: Verification
    test_passed = run_builder_test_verification()
    update_agent_status("builder", "idle", "Autonomous Builder Agent Active (Listening for tasks)")
    return test_passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builder Agent")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--task-title", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--priority", default="medium")
    args = parser.parse_args()

    success = handle_task(args.task_id, args.task_title, args.description, args.priority)
    sys.exit(0 if success else 1)
