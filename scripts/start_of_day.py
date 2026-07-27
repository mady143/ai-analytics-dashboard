"""
Start-of-Day Script — Syncs latest code from GitHub at the start of your morning session.
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
        f"[bold green]☀️  Start of Day Sync — {datetime.now().strftime('%Y-%m-%d %H:%M')}[/bold green]",
        border_style="green"
    ))

    from git_agent import pull

    success = pull()

    if success:
        console.print("[bold green]🎉 Ready for work! Local repository is up-to-date.[/bold green]")
    else:
        console.print("[yellow]⚠️  Could not pull latest changes. Continuing with local copy.[/yellow]")


if __name__ == "__main__":
    main()
