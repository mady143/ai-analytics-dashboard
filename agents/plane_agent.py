"""
Plane Agent — Manages tasks, sprints, and issues in Plane via REST API.
Handles: create project, create cycles (sprints), create/update issues.
Includes robust timeout & auto-retry resilience for all Plane REST API calls.
"""

import os
import json
import time
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

# Robust Timeout (30s read, 10s connect)
CLIENT_TIMEOUT = httpx.Timeout(30.0, connect=10.0)


def _get_client() -> httpx.Client:
    """Helper to return an httpx.Client with explicit 30s timeouts."""
    return httpx.Client(timeout=CLIENT_TIMEOUT, follow_redirects=True)


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

    for attempt in range(3):
        try:
            with _get_client() as client:
                resp = client.post(url, headers=HEADERS, json=payload)
                resp.raise_for_status()
                project = resp.json()
                project_id = project["id"]
                config["project_id"] = project_id
                _save_plane_config(config)
                console.print(f"[bold green]Created Plane project: {config['project_name']} (ID: {project_id})[/bold green]")
                return project_id
        except Exception as e:
            if attempt == 2:
                raise e
            time.sleep(1)

    return config.get("project_id", "")


# ── Cycles (Sprints) ───────────────────────────────────────────────────────────

def create_sprint(project_id: str, sprint_name: str, description: str, duration_weeks: int = 1) -> dict:
    """Create a new sprint (cycle) in Plane."""
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(weeks=duration_weeks)).strftime("%Y-%m-%d")

    # Ensure cycle_view is enabled on project
    try:
        with _get_client() as client:
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

    with _get_client() as client:
        resp = client.post(url, headers=HEADERS, json=payload)
        resp.raise_for_status()
        cycle = resp.json()

    console.print(f"[cyan]Created sprint: {sprint_name}[/cyan]")
    return cycle


def list_sprints(project_id: str) -> list[dict]:
    """List all sprints (cycles) for a project."""
    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles/"
    for attempt in range(3):
        try:
            with _get_client() as client:
                resp = client.get(url, headers=HEADERS)
                resp.raise_for_status()
                return resp.json().get("results", [])
        except Exception as e:
            if attempt == 2:
                console.print(f"[yellow]⚠️ list_sprints failed: {e}[/yellow]")
                return []
            time.sleep(1)
    return []


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

    with _get_client() as client:
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

    for attempt in range(3):
        try:
            with _get_client() as client:
                resp = client.patch(url, headers=HEADERS, json=payload)
                resp.raise_for_status()
                issue = resp.json()
                console.print(f"[green]Task status updated -> {status}[/green]")
                return issue
        except Exception as e:
            if attempt == 2:
                console.print(f"[red]Failed updating task status: {e}[/red]")
                return {}
            time.sleep(1)
    return {}


def get_states(project_id: str) -> list[dict]:
    """Get all workflow states for a project."""
    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/states/"
    for attempt in range(3):
        try:
            with _get_client() as client:
                resp = client.get(url, headers=HEADERS)
                resp.raise_for_status()
                return resp.json().get("results", [])
        except Exception as e:
            if attempt == 2:
                console.print(f"[yellow]⚠️ get_states failed: {e}[/yellow]")
                return []
            time.sleep(1)
    return []


def add_task_to_sprint(project_id: str, cycle_id: str, issue_id: str) -> None:
    """Add an issue to a sprint cycle."""
    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/"
    payload = {"issues": [issue_id]}
    with _get_client() as client:
        resp = client.post(url, headers=HEADERS, json=payload)
        resp.raise_for_status()


def add_comment(project_id: str, issue_id: str, comment: str) -> dict:
    """Add a comment to an issue (used for daily summaries and test results)."""
    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/{issue_id}/comments/"
    payload = {"comment_html": f"<p>{comment}</p>"}
    with _get_client() as client:
        resp = client.post(url, headers=HEADERS, json=payload)
        resp.raise_for_status()
        return resp.json()


def list_tasks(project_id: str, state_filter: Optional[str] = None) -> list[dict]:
    """List all issues in a project, optionally filtered by state."""
    url = f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    for attempt in range(3):
        try:
            with _get_client() as client:
                resp = client.get(url, headers=HEADERS)
                resp.raise_for_status()
                issues = resp.json().get("results", [])

                if state_filter:
                    issues = [i for i in issues if state_filter.lower() in i.get("state_detail", {}).get("name", "").lower()]

                return issues
        except Exception as e:
            if attempt == 2:
                console.print(f"[yellow]⚠️ list_tasks failed: {e}[/yellow]")
                return []
            time.sleep(1)
    return []


def list_comments(project_id: str, issue_id: str) -> list[dict]:
    """
    Fetch all activity/comments for a specific Plane issue.
    Returns a list of comment dicts with 'id', 'comment_html', 'created_at', 'actor_detail'.
    """
    url = (
        f"{PLANE_BASE_URL}/workspaces/{PLANE_WORKSPACE_SLUG}"
        f"/projects/{project_id}/issues/{issue_id}/comments/"
    )
    with _get_client() as client:
        resp = client.get(url, headers=HEADERS)
        resp.raise_for_status()
        return resp.json().get("results", [])
