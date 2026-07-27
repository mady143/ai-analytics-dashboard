"""
End-of-Day Script — Summarizes work and pushes to GitHub.
Can be run manually or scheduled to run at EOD time.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "agents"))
load_dotenv(ROOT_DIR / ".env")
console = Console()


def main():
    console.print(Panel.fit(
        f"[bold blue]🌙 End of Day — {datetime.now().strftime('%Y-%m-%d %H:%M')}[/bold blue]",
        border_style="blue"
    ))

    from memory_manager import get_todays_summary
    from git_agent import eod_push

    summary = get_todays_summary()
    console.print(f"[cyan]📋 Tasks completed today: {summary['tasks_completed']}[/cyan]")
    console.print(f"[cyan]📁 Files changed: {len(summary['files_changed'])}[/cyan]")

    # Build commit summary
    task_names = [r.get("task_title", "") for r in summary.get("details", [])
                  if r.get("status") == "completed"]

    success = eod_push(
        tasks_completed=task_names,
        custom_summary=f"Sprint progress: {summary['tasks_completed']} tasks completed"
    )

    if success:
        console.print("[bold green]🎉 EOD push complete![/bold green]")
    else:
        console.print("[red]❌ EOD push failed. Check git configuration.[/red]")


if __name__ == "__main__":
    main()
