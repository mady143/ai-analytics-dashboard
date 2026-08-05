# 🚨 Section 1: Mandatory Tasks & Autonomous Execution

This document outlines the mandatory operational requirements and autonomous workflow directives for the AI Analytics Dashboard project.

---

## 1. Daily Git Synchronization & Automatic Conflict Resolution
- **Morning (Start of Day):** Run `python scripts/start_of_day.py` or `git pull origin main` to pull latest remote changes before work begins.
- **Automatic Merge Conflict Resolution:** If any git merge or rebase conflicts occur during pull, automatically analyze conflicting files, resolve all conflicts cleanly, stage changes (`git add .`), and complete the commit.
- **Task Completion & Autonomous Git Push / PR:** Automatically pull remote changes (`git pull origin main`), stage changes (`git add .`), commit with a descriptive message, create pull requests when applicable, and push updated code to remote GitHub (`mmusunur/ai-analytics-dashboard`) upon task completion or at the end of the day.

### Associated Scripts
- [`scripts/start_of_day.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/start_of_day.py)
- [`scripts/end_of_day.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/end_of_day.py)
- [`agents/git_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/git_agent.py)

---

## 2. Automatic README.md Maintenance Mandate
- **Mandatory Documentation Directive:**
  - The AI AGENT MUST automatically maintain and update [`README.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/README.md) whenever new features, backend API endpoints, multi-database architecture parameters, or agent processes are added or updated.
  - Keep `README.md` synchronized with the active project structure, API endpoints table, background agent list, and testing instructions.

---

## 3. Real End-to-End Autonomous Task Execution Pipeline
- **Sprint Watcher (`agents/sprint_watcher_agent.py`):**
  - ONLY pick up tasks in `ACTIONABLE_STATES` = `("unstarted", "backlog", "todo", "started", "in_progress")`.
  - SKIP tasks in `SKIP_STATES` = `("completed", "done", "cancelled")`.
  - Automatically triggered via non-blocking background thread when `/api/sprints/tasks` is called.

- **Builder Agent (`agents/builder_agent.py`):**
  - Performs REAL code changes to React frontend components and Python backend services.
  - Generates code patches using LLM/autonomous intent classifiers, writes modified files, runs pytest, and updates Plane task status to `Completed`.
