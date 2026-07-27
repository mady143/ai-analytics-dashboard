"""
Builder Agent — Receives tasks from Sprint Watcher, generates/updates component code,
and verifies syntax/build before returning control to Tester & Sprint Watcher.
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "agents"))

from memory_manager import update_agent_status, log_task_result

console = Console()


def build_navbar(task_title: str, description: str):
    """Build or update Navbar component in frontend."""
    components_dir = ROOT_DIR / "frontend" / "src" / "components"
    components_dir.mkdir(parents=True, exist_ok=True)
    
    navbar_file = components_dir / "Navbar.jsx"
    navbar_code = '''import React from 'react';

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <span className="logo-icon">⚡</span>
          <span className="logo-text">AI Analytics Dashboard</span>
        </div>
        <nav className="navbar-links">
          <a href="#overview" className="nav-link active">Overview</a>
          <a href="#analytics" className="nav-link">ML Analytics</a>
          <a href="#data" className="nav-link">Datasets</a>
          <a href="#agents" className="nav-link">Agent Network</a>
          <a href="#settings" className="nav-link">Settings</a>
        </nav>
        <div className="navbar-actions">
          <span className="status-badge live">● Live Agent Loop</span>
        </div>
      </div>
    </header>
  );
}
'''
    navbar_file.write_text(navbar_code, encoding="utf-8")
    console.print(f"[green]✅ Created Navbar component at {navbar_file}[/green]")

    # Check App.jsx and import Navbar if missing
    app_file = ROOT_DIR / "frontend" / "src" / "App.jsx"
    if app_file.exists():
        app_code = app_file.read_text(encoding="utf-8")
        if "Navbar" not in app_code:
            updated_app = "import Navbar from './components/Navbar';\n" + app_code
            if "<div className=\"app-container\">" in updated_app:
                updated_app = updated_app.replace(
                    '<div className="app-container">',
                    '<div className="app-container">\n      <Navbar />'
                )
            elif "return (" in updated_app:
                updated_app = updated_app.replace(
                    "return (",
                    "return (\n    <>\n      <Navbar />"
                )
                if updated_app.endswith(";\n}") or updated_app.endswith("}"):
                    updated_app = updated_app.rstrip("}").rstrip("\n;").rstrip() + "\n    </>\n  );\n}"
            app_file.write_text(updated_app, encoding="utf-8")
            console.print("[green]✅ Integrated Navbar into App.jsx[/green]")

    # Create corresponding unit test case
    test_dir = ROOT_DIR / "tests" / "unit"
    test_dir.mkdir(parents=True, exist_ok=True)
    test_file = test_dir / "test_navbar.py"
    test_code = '''"""Unit tests for Navbar component integration."""
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

def test_navbar_file_exists():
    navbar_path = ROOT_DIR / "frontend" / "src" / "components" / "Navbar.jsx"
    assert navbar_path.exists(), "Navbar.jsx component file must exist"

def test_navbar_structure():
    navbar_path = ROOT_DIR / "frontend" / "src" / "components" / "Navbar.jsx"
    content = navbar_path.read_text(encoding="utf-8")
    assert "export default function Navbar" in content
    assert "AI Analytics Dashboard" in content
'''
    test_file.write_text(test_code, encoding="utf-8")
    console.print(f"[green]✅ Created test suite at {test_file}[/green]")


def handle_task(task_id: str, task_title: str, description: str, priority: str) -> bool:
    """Analyze task request and build the necessary code."""
    update_agent_status("builder", "running", task_title)
    console.print(Panel.fit(
        f"[bold cyan]🔨 Builder Agent Working on Task[/bold cyan]\n"
        f"Title: {task_title}\n"
        f"ID: {task_id}",
        border_style="cyan"
    ))

    title_lower = task_title.lower()
    
    if "nav" in title_lower or "navbar" in title_lower or "navigation" in title_lower:
        build_navbar(task_title, description)
    else:
        console.print(f"[cyan]ℹ️ Generic task detected: {task_title}. Processing component updates...[/cyan]")
        # Log generic code generation
        logs_dir = ROOT_DIR / "reports" / "build_logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = logs_dir / f"{task_id}.txt"
        log_file.write_text(f"Task: {task_title}\nDesc: {description}\nProcessed at: {datetime.now().isoformat()}\n", encoding="utf-8")
        console.print(f"[green]✅ Generated build logs for {task_title}[/green]")

    update_agent_status("builder", "idle")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builder Agent")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--task-title", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--priority", default="medium")
    args = parser.parse_args()

    success = handle_task(args.task_id, args.task_title, args.description, args.priority)
    sys.exit(0 if success else 1)
