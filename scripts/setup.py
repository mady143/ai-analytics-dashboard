"""
Setup Script — One-time project initialization.
Run this first to: install deps, set up git, configure Plane, and initialize agent state.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()
ROOT_DIR = Path(__file__).parent.parent
ENV_FILE = ROOT_DIR / ".env"
ENV_EXAMPLE = ROOT_DIR / ".env.example"


def check_python():
    """Check Python version."""
    ver = sys.version_info
    if ver.major < 3 or (ver.major == 3 and ver.minor < 10):
        console.print("[red]❌ Python 3.10+ required. Current: {ver.major}.{ver.minor}[/red]")
        sys.exit(1)
    console.print(f"[green]✅ Python {ver.major}.{ver.minor}.{ver.micro}[/green]")


def install_dependencies():
    """Install Python dependencies."""
    console.print("\n[cyan]📦 Installing Python dependencies...[/cyan]")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"],
        cwd=str(ROOT_DIR)
    )
    if result.returncode == 0:
        console.print("[green]✅ Python dependencies installed[/green]")
    else:
        console.print("[yellow]⚠️  Some packages may have failed to install[/yellow]")


def install_playwright():
    """Install Playwright browsers."""
    console.print("\n[cyan]🎭 Installing Playwright browsers...[/cyan]")
    subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        cwd=str(ROOT_DIR)
    )
    console.print("[green]✅ Playwright Chromium installed[/green]")


def setup_env():
    """Create .env from .env.example if not exists."""
    if ENV_FILE.exists():
        console.print("[green]✅ .env file already exists[/green]")
        return

    console.print("\n[yellow]📝 Setting up .env file...[/yellow]")
    console.print("[dim]You'll need to fill in your API keys.[/dim]\n")

    env_content = ENV_EXAMPLE.read_text()

    # Prompt for required keys
    anthropic_key = Prompt.ask("[cyan]Enter your Anthropic API Key[/cyan] (or press Enter to skip)")
    plane_token = Prompt.ask("[cyan]Enter your Plane API Token[/cyan] (or press Enter to skip)")
    plane_slug = Prompt.ask("[cyan]Enter your Plane Workspace Slug[/cyan] (or press Enter to skip)")
    github_token = Prompt.ask("[cyan]Enter your GitHub Token[/cyan] (or press Enter to skip)")
    github_repo = Prompt.ask("[cyan]Enter your GitHub Repo (user/repo)[/cyan] (or press Enter to skip)")

    replacements = {
        "your_anthropic_api_key_here": anthropic_key or "your_anthropic_api_key_here",
        "your_plane_api_token_here": plane_token or "your_plane_api_token_here",
        "your_workspace_slug_here": plane_slug or "your_workspace_slug_here",
        "your_github_personal_access_token_here": github_token or "your_github_personal_access_token_here",
        "your_username/ai-analytics-dashboard": github_repo or "your_username/ai-analytics-dashboard"
    }

    for old, new in replacements.items():
        env_content = env_content.replace(old, new)

    ENV_FILE.write_text(env_content)
    console.print("[green]✅ .env file created[/green]")


def setup_git():
    """Initialize git repository."""
    from agents.git_agent import init_repo, setup_git_config
    init_repo()
    setup_git_config()


def setup_plane():
    """Set up Plane project and sprints."""
    # Load env
    from dotenv import load_dotenv
    load_dotenv(ENV_FILE)

    token = os.getenv("PLANE_API_TOKEN", "")
    slug = os.getenv("PLANE_WORKSPACE_SLUG", "")

    if not token or token == "your_plane_api_token_here":
        console.print("[yellow]⚠️  Plane API token not set — skipping Plane setup[/yellow]")
        console.print("[dim]You can set up Plane later by running: python agents/plane_agent.py[/dim]")
        return

    console.print("\n[cyan]🚀 Setting up Plane project...[/cyan]")
    try:
        sys.path.insert(0, str(ROOT_DIR / "agents"))
        from plane_agent import get_or_create_project, setup_all_sprints, setup_initial_tasks

        project_id = get_or_create_project()
        sprints = setup_all_sprints(project_id)
        if sprints:
            setup_initial_tasks(project_id, sprints[0]["id"])
            console.print("[bold green]🎉 Plane project fully set up![/bold green]")

            # Save to agent state
            state_file = ROOT_DIR / "memory" / "agent_state.json"
            with open(state_file) as f:
                state = json.load(f)
            state["plane_project_id"] = project_id
            state["plane_workspace_slug"] = slug
            state["initialized_at"] = datetime.now().isoformat()
            with open(state_file, "w") as f:
                json.dump(state, f, indent=2)
    except Exception as e:
        console.print(f"[red]❌ Plane setup failed: {e}[/red]")


def print_next_steps():
    """Print instructions for running the project."""
    console.print(Panel.fit(
        "[bold green]🎉 Setup Complete![/bold green]\n\n"
        "[bold]Next Steps:[/bold]\n\n"
        "1️⃣  Start the backend:\n"
        "   [cyan]cd backend && uvicorn main:app --reload[/cyan]\n\n"
        "2️⃣  Start the frontend:\n"
        "   [cyan]cd frontend && npm run dev[/cyan]\n\n"
        "3️⃣  Run the agents:\n"
        "   [cyan]python scripts/run_agents.py[/cyan]\n\n"
        "4️⃣  Run tests:\n"
        "   [cyan]python scripts/run_tests.py[/cyan]\n\n"
        "5️⃣  View dashboard:\n"
        "   [link=http://localhost:5173]http://localhost:5173[/link]\n\n"
        "[dim]📖 See README.md for full documentation[/dim]",
        border_style="green"
    ))


if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold magenta]🚀 AI Analytics Dashboard — Project Setup[/bold magenta]",
        border_style="magenta"
    ))

    check_python()
    setup_env()
    install_dependencies()

    if Confirm.ask("\n[cyan]Install Playwright browsers for browser testing?[/cyan]", default=True):
        install_playwright()

    setup_git()

    if Confirm.ask("\n[cyan]Set up Plane project and sprints?[/cyan]", default=True):
        setup_plane()

    print_next_steps()
