"""
Script to mark Plane task AAD-20 completed with implementation comment.
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "agents"))

from plane_agent import get_or_create_project, list_tasks, update_task_status, add_comment

if __name__ == "__main__":
    pid = get_or_create_project()
    tasks = list_tasks(pid)
    target = None
    for t in tasks:
        if "Nav Bar" in t.get("name", "") or "AAD-20" in t.get("name", ""):
            target = t
            break

    if target:
        tid = target["id"]
        update_task_status(pid, tid, "completed")
        add_comment(
            pid, tid,
            "🤖 Task Implemented & Verified: Added 3-line hamburger hide/show toggle button (#nav-bar-toggle-btn & #nav-bar-enable-btn) to Sidebar.jsx and App.jsx. Created Footer.jsx with default copyright notice. Passed unit tests."
        )
        print(f"Successfully marked task {target['name']} ({tid}) as completed!")
    else:
        print("Task AAD-20 not found in Plane.")
