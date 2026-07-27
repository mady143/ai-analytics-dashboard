"""
Plane Setup Script — Creates the project, sprints, and initial tasks
in your Plane workspace (agentbuilder) and maps everything to this app.

Run this ONCE after filling in .env with PLANE_API_TOKEN.

Usage:
    python scripts/setup_plane.py
    python scripts/setup_plane.py --verify    # just verify connection
    python scripts/setup_plane.py --status    # show existing project status
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "agents"))
load_dotenv(ROOT_DIR / ".env")
console = Console()

# ── Validate env before anything else ─────────────────────────────────────────
TOKEN = os.getenv("PLANE_API_TOKEN", "")
SLUG  = os.getenv("PLANE_WORKSPACE_SLUG", "agentbuilder")


def _check_env():
    issues = []
    if not TOKEN or TOKEN.startswith("<"):
        issues.append(
            "PLANE_API_TOKEN is not set.\n"
            "  Get it from: app.plane.so → Settings → API Tokens → Add API Token"
        )
    if not SLUG or SLUG.startswith("<"):
        issues.append("PLANE_WORKSPACE_SLUG is not set. Should be: agentbuilder")
    return issues


def verify_connection():
    """Test that we can reach Plane with the given credentials."""
    import httpx
    url = f"https://api.plane.so/api/v1/workspaces/{SLUG}/projects/"
    headers = {"X-API-Key": TOKEN}
    console.print(f"\n[cyan]Testing connection to Plane workspace '{SLUG}'...[/cyan]")
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            count = data.get("count", len(data.get("results", [])))
            console.print(f"[bold green]Connection OK! Found {count} existing project(s) in '{SLUG}'.[/bold green]")
            return True
        elif resp.status_code == 401:
            console.print("[red]401 Unauthorized — your PLANE_API_TOKEN is invalid or expired.[/red]")
        elif resp.status_code == 404:
            console.print(f"[red]404 Not Found — workspace slug '{SLUG}' may be wrong.[/red]")
        else:
            console.print(f"[red]Error {resp.status_code}: {resp.text[:200]}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]Connection failed: {e}[/red]")
        return False


def show_existing_projects():
    """List all existing projects in the workspace."""
    import httpx
    url = f"https://api.plane.so/api/v1/workspaces/{SLUG}/projects/"
    headers = {"X-API-Key": TOKEN}
    with httpx.Client() as client:
        resp = client.get(url, headers=headers)
        resp.raise_for_status()
        projects = resp.json().get("results", [])

    if not projects:
        console.print("[yellow]No projects found in this workspace.[/yellow]")
        return

    table = Table(title=f"Projects in workspace '{SLUG}'")
    table.add_column("Name", style="cyan")
    table.add_column("ID", style="dim")
    table.add_column("Identifier", style="bold")
    table.add_column("Issues")

    for p in projects:
        table.add_row(
            p.get("name", ""),
            p.get("id", ""),
            p.get("identifier", ""),
            str(p.get("total_issues", 0))
        )
    console.print(table)
    return projects


def create_project_and_setup():
    """Full setup: create project, sprints, and initial tasks."""
    from plane_agent import (
        get_or_create_project,
        setup_all_sprints,
        setup_initial_tasks,
        list_sprints,
        list_tasks,
    )
    from memory_manager import load_state, save_state

    console.print(Panel.fit(
        f"[bold magenta]Setting up Plane Project[/bold magenta]\n"
        f"[dim]Workspace: {SLUG} | Token: {TOKEN[:8]}...[/dim]",
        border_style="magenta"
    ))

    # ── 1. Create / get project ───────────────────────────────────────────────
    console.print("\n[cyan]Step 1: Create/find project 'AI Analytics Dashboard'...[/cyan]")
    project_id = get_or_create_project()
    console.print(f"[green]Project ID: {project_id}[/green]")

    # ── 2. Create sprints ─────────────────────────────────────────────────────
    console.print("\n[cyan]Step 2: Creating 5 sprints (cycles)...[/cyan]")
    existing_sprints = list_sprints(project_id)
    if existing_sprints:
        console.print(f"[yellow]  {len(existing_sprints)} sprint(s) already exist — skipping sprint creation.[/yellow]")
        sprints = existing_sprints
    else:
        sprints = setup_all_sprints(project_id)
        console.print(f"[green]  Created {len(sprints)} sprints.[/green]")

    # ── 3. Create initial tasks ───────────────────────────────────────────────
    console.print("\n[cyan]Step 3: Creating initial tasks for Sprint 1...[/cyan]")
    existing_tasks = list_tasks(project_id)
    if existing_tasks:
        console.print(f"[yellow]  {len(existing_tasks)} task(s) already exist — skipping task creation.[/yellow]")
    else:
        sprint_1_id = sprints[0]["id"] if sprints else None
        if sprint_1_id:
            setup_initial_tasks(project_id, sprint_1_id)
            console.print("[green]  Initial tasks created in Sprint 1.[/green]")

    # ── 4. Persist to .env and agent_state.json ───────────────────────────────
    console.print("\n[cyan]Step 4: Saving project ID to agent state...[/cyan]")
    state = load_state()
    state["plane_project_id"]    = project_id
    state["plane_workspace_slug"] = SLUG
    state["initialized_at"]      = datetime.now().isoformat()
    save_state(state)

    # Update .env file with PLANE_PROJECT_ID
    env_file = ROOT_DIR / ".env"
    env_text = env_file.read_text()
    if "PLANE_PROJECT_ID=" in env_text:
        lines = env_text.splitlines()
        new_lines = []
        for line in lines:
            if line.startswith("PLANE_PROJECT_ID="):
                new_lines.append(f"PLANE_PROJECT_ID={project_id}")
            else:
                new_lines.append(line)
        env_file.write_text("\n".join(new_lines))
        console.print(f"[green]  .env updated: PLANE_PROJECT_ID={project_id}[/green]")

    # ── 5. Final summary ──────────────────────────────────────────────────────
    final_tasks = list_tasks(project_id)
    final_sprints = list_sprints(project_id)

    console.print(Panel(
        f"[bold green]Setup Complete![/bold green]\n\n"
        f"  Workspace:   {SLUG}\n"
        f"  Project ID:  {project_id}\n"
        f"  Sprints:     {len(final_sprints)}\n"
        f"  Tasks:       {len(final_tasks)}\n\n"
        f"  View at: https://app.plane.so/{SLUG}/projects/{project_id}/issues/\n\n"
        f"[dim]Next: python scripts/run_sprint_watcher.py[/dim]",
        border_style="green"
    ))

    return project_id


def show_project_status(project_id: str):
    """Show current project tasks and sprint status."""
    from plane_agent import list_tasks, list_sprints

    tasks   = list_tasks(project_id)
    sprints = list_sprints(project_id)

    # Sprint table
    sprint_table = Table(title="Sprints (Cycles)")
    sprint_table.add_column("Sprint", style="cyan")
    sprint_table.add_column("Start")
    sprint_table.add_column("End")
    for s in sprints:
        sprint_table.add_row(s.get("name",""), s.get("start_date",""), s.get("end_date",""))
    console.print(sprint_table)

    # Task table
    task_table = Table(title=f"Tasks ({len(tasks)} total)")
    task_table.add_column("Priority", width=10)
    task_table.add_column("Task", style="cyan", min_width=40)
    task_table.add_column("State", width=14)
    priority_colors = {"urgent":"red","high":"orange3","medium":"yellow","low":"dim"}
    for t in tasks:
        p = t.get("priority","none").lower()
        s = t.get("state_detail",{}).get("name","")
        task_table.add_row(
            f"[{priority_colors.get(p,'white')}]{p.upper()}[/{priority_colors.get(p,'white')}]",
            t.get("name","")[:55],
            s
        )
    console.print(task_table)


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plane Setup for AI Analytics Dashboard")
    parser.add_argument("--verify", action="store_true", help="Just test connection")
    parser.add_argument("--status", action="store_true", help="Show project status")
    args = parser.parse_args()

    # Environment check
    issues = _check_env()
    if issues:
        console.print("[bold red]Cannot connect to Plane:[/bold red]")
        for issue in issues:
            console.print(f"  [red]• {issue}[/red]")
        console.print(
            "\n[yellow]Steps to fix:[/yellow]\n"
            "  1. Go to: https://app.plane.so/agentbuilder/settings/api-tokens/\n"
            "  2. Click 'Add API Token' → name it 'ai-dashboard-agent'\n"
            "  3. Copy the token\n"
            "  4. Open: C:\\Users\\manik\\Downloads\\c&s\\mani_personal\\ai_analytics_dashboard\\.env\n"
            "  5. Replace <YOUR_PLANE_API_TOKEN> with your token\n"
            "  6. Re-run: python scripts/setup_plane.py"
        )
        sys.exit(1)

    if args.verify:
        verify_connection()
        sys.exit(0)

    # Test connection first
    if not verify_connection():
        sys.exit(1)

    if args.status:
        state = json.loads((ROOT_DIR / "memory" / "agent_state.json").read_text())
        pid = state.get("plane_project_id")
        if not pid:
            console.print("[yellow]No project configured yet. Run without --status first.[/yellow]")
        else:
            show_project_status(pid)
        sys.exit(0)

    # Full setup
    console.print("\n[dim]Listing existing projects...[/dim]")
    show_existing_projects()

    create_project_and_setup()
