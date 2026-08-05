# 📄 Task 28 Specification: Daily Memory Persistence & Conversation Task Updating

## 📋 Overview
This task specification governs the **Daily Memory Persistence & Conversation State Updating Engine** for the AI Analytics Dashboard Autonomous Agent Network.

---

## 🚨 Section 1: Memory Architecture & Daily Log Persistence

### 1. Conversation Memory Stream
- **Path:** `memory/conversations/assistant_conversation.jsonl`
- **Function:** Logs every user conversation query, model response summary, timestamp, and date.
- **Handler:** `update_conversation_memory(agent_name, user_query, response_summary)` in [`agents/memory_manager.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/memory_manager.py)

### 2. Daily Task History Log Stream
- **Path:** `memory/task_history/YYYY-MM-DD_task_history.jsonl`
- **Function:** Tracks task pickup IDs, titles, execution status (`completed`, `in_progress`, `failed`), agent outputs, and test durations.
- **Daily Rotation:** A new `.jsonl` file is automatically created every day (`YYYY-MM-DD`).

### 3. Agent State Singleton
- **Path:** `memory/agent_state.json`
- **Function:** Stores current active agent statuses (`sprint_watcher`, `builder`, `tester`, `memory`, `git_agent`, `orchestrator`), current sprint project metadata, active tasks queue, and `last_conversation_update` timestamp.

---

## ⚡ Section 2: Daily Workflow & Task Execution Rules

1. **Automatic Non-Blocking Task Pickup:** Whenever the frontend or user interacts with `/api/sprints/tasks`, `backend/routers/sprints.py` automatically triggers `SprintWatcherAgent` in a non-blocking background thread.
2. **Dynamic Code Modification:** `builder_agent.py` analyzes open tasks (`unstarted`, `todo`, `started`, `in_progress`), reads source code files, applies code modifications, runs unit tests via `tester_agent.py`, and updates Plane task status to `Completed`.
3. **Daily Conversation Memory Updating:** At the end of every user conversation turn, `update_conversation_memory()` is called to append the interaction to memory logs and sync state.

---

## 🧪 Section 3: Verification & Test Requirements

- Unit test suite: `pytest tests/unit/` (51 test cases).
- Verification command: `python -m agents.memory_manager`
