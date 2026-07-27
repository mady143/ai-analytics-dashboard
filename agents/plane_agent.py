"""
Plane Agent — Manages tasks, sprints, and issues in Plane via REST API.
Handles: create project, create cycles (sprints), create/update issues.
"""

import os
import json
import httpx
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from rich.console import Console
from dotenv import load_dotenv

load_dotenv()
console = Console()

# ── Config ─────────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent.parent
PLANE_CONFIG_FILE = ROOT_DIR / "config" / "plane_config.json"

PLANE_API_TOKEN = os.getenv("PLANE_API_TOKEN", "")
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG", "")
PLANE_BASE_URL = "https://api.plane.so/api/v1"

HEADERS = {
    "X-API-Key": PLANE_API_TOKEN,
    "Content-Type": "application/json"
}


def _load_plane_config() -> dict:
    with open(PLANE_CONFIG_FILE) as f:
        return json.load(f)


def _save_plane_config(config: dict) -> None:
    with open(PLANE_CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


# ── Project ────────────────────────────────────────────────────────────────────

def get_or_create_project() -> str:
    """
    Get the existing Plane project ID or create a new one.
    Returns the project ID.
    """
    config = _load_plane_config()

    # Return cached project_id if available
    if config.get("project_id"):
        console.print(f"[green]Using existing Plane project: {config['project_id']}[/green]")
        return config["project_id"]

    # Create new project
    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    payload = {
        "name": config["project_name"],
        "identifier": "AAD",
        "description": "Agentic AI Analytics Dashboard — built and managed by AI agents",
        "network": 2  # Public
    }

    with httpx.Client() as client:
        resp = client.post(url, headers=HEADERS, json=payload)
        resp.raise_for_status()
        project = resp.json()

    project_id = project["id"]
    config["project_id"] = project_id
    _save_plane_config(config)

    console.print(f"[bold green]Created Plane project: {config['project_name']} (ID: {project_id})[/bold green]")
    return project_id


# ── Cycles (Sprints) ───────────────────────────────────────────────────────────

def create_sprint(project_id: str, sprint_name: str, description: str, duration_weeks: int = 1) -> dict:
    """Create a new sprint (cycle) in Plane."""
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(weeks=duration_weeks)).strftime("%Y-%m-%d")

    # Ensure cycle_view is enabled on project
    try:
        with httpx.Client() as client:
            client.patch(f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/", headers=HEADERS, json={"cycle_view": True})
    except Exception:
        pass

    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles/"
    payload = {
        "name": sprint_name,
        "description": description,
        "start_date": start_date,
        "end_date": end_date,
        "project_id": project_id
    }

    with httpx.Client() as client:
        resp = client.post(url, headers=HEADERS, json=payload)
        resp.raise_for_status()
        cycle = resp.json()

    console.print(f"[cyan]Created sprint: {sprint_name}[/cyan]")
    return cycle


def list_sprints(project_id: str) -> list[dict]:
    """List all sprints (cycles) for a project."""
    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles/"
    with httpx.Client() as client:
        resp = client.get(url, headers=HEADERS)
        resp.raise_for_status()
        return resp.json().get("results", [])


# ── Issues (Tasks) ─────────────────────────────────────────────────────────────

def create_task(
    project_id: str,
    title: str,
    description: str = "",
    priority: str = "medium",
    story_points: int = 3,
    cycle_id: Optional[str] = None,
    parent_id: Optional[str] = None
) -> dict:
    """
    Create an issue (task) in Plane.
    priority: "urgent" | "high" | "medium" | "low" | "none"
    story_points: 1, 2, 3, 5, 8
    """
    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    payload = {
        "name": title,
        "description_html": f"<p>{description}</p>",
        "priority": priority,
        "estimate_point": story_points,
        "parent": parent_id
    }

    with httpx.Client() as client:
        resp = client.post(url, headers=HEADERS, json=payload)
        resp.raise_for_status()
        issue = resp.json()

    # Add to cycle if specified
    if cycle_id:
        add_task_to_sprint(project_id, cycle_id, issue["id"])

    console.print(f"[yellow]Created task: [{priority.upper()}] {title} ({story_points} pts)[/yellow]")
    return issue


def create_subtask(project_id: str, parent_issue_id: str, title: str, description: str = "") -> dict:
    """Create a sub-task (child issue) under a parent issue."""
    return create_task(
        project_id=project_id,
        title=title,
        description=description,
        priority="medium",
        story_points=1,
        parent_id=parent_issue_id
    )


def update_task_status(project_id: str, issue_id: str, status: str) -> dict:
    """
    Update the status of a task.
    status: "backlog" | "unstarted" | "todo" | "started" | "in progress" | "completed" | "done" | "cancelled"
    """
    states = get_states(project_id)
    state_id = None
    status_clean = status.lower().strip()
    
    # Priority match by group or exact name
    for state in states:
        name = state.get("name", "").lower().strip()
        group = state.get("group", "").lower().strip()
        if status_clean in (name, group) or (status_clean == "done" and group == "completed") or (status_clean == "completed" and name == "done"):
            state_id = state["id"]
            break

    if not state_id:
        # Fallback substring match
        for state in states:
            name = state.get("name", "").lower().strip()
            group = state.get("group", "").lower().strip()
            if status_clean in name or status_clean in group:
                state_id = state["id"]
                break

    if not state_id:
        console.print(f"[red]State '{status}' not found in project states[/red]")
        return {}

    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/{issue_id}/"
    payload = {"state": state_id}

    with httpx.Client() as client:
        resp = client.patch(url, headers=HEADERS, json=payload)
        resp.raise_for_status()
        issue = resp.json()

    console.print(f"[green]Task status updated -> {status}[/green]")
    return issue


def get_states(project_id: str) -> list[dict]:
    """Get all workflow states for a project."""
    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/states/"
    with httpx.Client() as client:
        resp = client.get(url, headers=HEADERS)
        resp.raise_for_status()
        return resp.json().get("results", [])


def add_task_to_sprint(project_id: str, cycle_id: str, issue_id: str) -> None:
    """Add an issue to a sprint cycle."""
    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/"
    payload = {"issues": [issue_id]}
    with httpx.Client() as client:
        resp = client.post(url, headers=HEADERS, json=payload)
        resp.raise_for_status()


def add_comment(project_id: str, issue_id: str, comment: str) -> dict:
    """Add a comment to an issue (used for daily summaries and test results)."""
    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/{issue_id}/comments/"
    payload = {"comment_html": f"<p>{comment}</p>"}
    with httpx.Client() as client:
        resp = client.post(url, headers=HEADERS, json=payload)
        resp.raise_for_status()
        return resp.json()


def list_tasks(project_id: str, state_filter: Optional[str] = None) -> list[dict]:
    """List all issues in a project, optionally filtered by state."""
    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    with httpx.Client() as client:
        resp = client.get(url, headers=HEADERS)
        resp.raise_for_status()
        issues = resp.json().get("results", [])

    if state_filter:
        issues = [i for i in issues if state_filter.lower() in i.get("state_detail", {}).get("name", "").lower()]

    return issues


def list_comments(project_id: str, issue_id: str) -> list[dict]:
    """
    Fetch all activity/comments for a specific Plane issue.
    Returns a list of comment dicts with 'id', 'comment_html', 'created_at', 'actor_detail'.
    """
    url = (
        f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}"
        f"/projects/{project_id}/issues/{issue_id}/comments/"
    )
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.get(url, headers=HEADERS)
            resp.raise_for_status()
            return resp.json().get("results", [])
    except Exception as e:
        console.print(f"[yellow]⚠️  Could not fetch comments for issue {issue_id}: {e}[/yellow]")
        return []


# ── Sprint Setup ───────────────────────────────────────────────────────────────

def setup_all_sprints(project_id: str) -> list[dict]:
    """Create all 5 sprints defined in the plane config."""
    config = _load_plane_config()
    created_sprints = []

    for sprint_def in config["sprints"]:
        sprint = create_sprint(
            project_id=project_id,
            sprint_name=sprint_def["name"],
            description=sprint_def["description"],
            duration_weeks=sprint_def["duration_weeks"]
        )
        created_sprints.append(sprint)

    return created_sprints


def setup_initial_tasks(project_id: str, sprint_1_id: str) -> None:
    """Create the initial set of tasks for Sprint 1 in Plane."""
    tasks = [
        # Backend epic
        {"title": "Create FastAPI project structure", "priority": "urgent", "pts": 2,
         "desc": "Set up FastAPI app with CORS, health check, and router structure"},
        {"title": "Data ingestion endpoints", "priority": "high", "pts": 3,
         "desc": "POST /upload, GET /sample, GET /summary endpoints"},
        {"title": "ML analytics endpoints", "priority": "high", "pts": 5,
         "desc": "Train model, get results, predict endpoints"},
        {"title": "Chart data endpoints", "priority": "medium", "pts": 3,
         "desc": "Bar, scatter, heatmap, KPI chart data endpoints"},

        # Memory & Agents
        {"title": "Memory system implementation", "priority": "urgent", "pts": 3,
         "desc": "Conversation history, task logs, agent state persistence"},
        {"title": "Orchestrator agent", "priority": "urgent", "pts": 8,
         "desc": "Master agent that coordinates all sub-agents"},
        {"title": "Builder agent", "priority": "high", "pts": 5,
         "desc": "Code writing agent with Plane + memory integration"},
        {"title": "Tester agent", "priority": "high", "pts": 5,
         "desc": "Automated testing agent with pytest + Playwright"},
        {"title": "Git agent", "priority": "medium", "pts": 2,
         "desc": "End-of-day git commit and push automation"},

        # MCP
        {"title": "MCP server configuration", "priority": "medium", "pts": 3,
         "desc": "Configure Plane, GitHub, Memory, Browser MCP servers"},
    ]

    for task_def in tasks:
        create_task(
            project_id=project_id,
            title=task_def["title"],
            description=task_def["desc"],
            priority=task_def["priority"],
            story_points=task_def["pts"],
            cycle_id=sprint_1_id
        )


if __name__ == "__main__":
    console.print("[bold magenta]Plane Agent -- Setup Mode[/bold magenta]")

    if not PLANE_API_TOKEN or not PLANE_WORKSPACE_SLUG:
        console.print("[red]Please set PLANE_API_TOKEN and PLANE_WORKSPACE_SLUG in .env[/red]")
    else:
        project_id = get_or_create_project()
        sprints = setup_all_sprints(project_id)
        if sprints:
            setup_initial_tasks(project_id, sprints[0]["id"])
            console.print("[bold green]Plane project fully set up![/bold green]")
