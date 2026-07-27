# 🔌 MCP Servers — Complete Module Documentation

> **MCP (Model Context Protocol)** is Anthropic's open standard that lets AI agents call external tools in a structured, auditable way.  
> Each MCP server exposes a set of **tools** that agents can invoke by name.

---

## What is MCP?

```
Agent (Claude)
    │
    │  "I need to create a Plane task"
    ▼
MCP Client (agents/mcp_client.py)
    │
    │  routes call → correct MCP server
    ▼
MCP Server (e.g. Plane MCP)
    │
    │  executes Plane REST API call
    ▼
External Service (Plane / GitHub / Browser / Memory)
    │
    └──► Returns structured result back to Agent
```

MCP provides:
- **Auditability** — every tool call is logged
- **Safety** — agents cannot call arbitrary code, only declared tools
- **Composability** — any agent can use any MCP server

---

## MCP Config File

**File:** `mcp_servers/mcp_config.json`

This is the **master registry** of all MCP servers in this project.  
Agents load this file via `agents/mcp_client.py` to know which tool maps to which server.

```json
{
  "mcpServers": {
    "plane":   { ... },
    "github":  { ... },
    "memory":  { ... },
    "browser": { ... }
  }
}
```

---

## 1. Plane MCP Server

**Purpose:** Create, update, and query tasks and sprints in Plane  
**Config key:** `plane`  
**Backed by:** `agents/plane_agent.py`

### Tools Exposed

| Tool Name | Arguments | What it does |
|---|---|---|
| `create_task` | `title, description, priority, story_points` | Creates a new Plane issue |
| `update_task_status` | `task_id, status` | Moves task to new state |
| `create_sprint` | `name, description, duration_weeks` | Creates a new cycle |
| `list_tasks` | `state_filter?` | Returns all issues (optionally filtered) |
| `add_comment` | `task_id, comment` | Posts comment on an issue |

### When Agents Use It
- **Sprint Watcher** → `update_task_status` (Todo→In Progress→Done)
- **Sprint Watcher** → `add_comment` (post test results)
- **Orchestrator** → `list_tasks` (get current sprint state)
- **Setup Script** → `create_task`, `create_sprint` (initial setup)

### Environment Variables Required
```env
PLANE_API_TOKEN=your_token_here
PLANE_WORKSPACE_SLUG=your_slug_here
```

### API Base URL
`https://api.plane.so/api/v1`

---

## 2. GitHub MCP Server

**Purpose:** Git operations — commit, push, branch management  
**Config key:** `github`  
**Backed by:** `agents/git_agent.py`

### Tools Exposed

| Tool Name | Arguments | What it does |
|---|---|---|
| `git_commit` | `message` | Stages and commits all changes |
| `git_push` | `branch` | Pushes to remote |
| `create_pull_request` | `title, body, branch` | Opens a PR on GitHub |
| `list_commits` | `n` | Returns last N commit messages |

### When Agents Use It
- **Git Agent** → `git_commit`, `git_push` (end-of-day automation)
- **Orchestrator** → `list_commits` (status report context)

### Environment Variables Required
```env
GITHUB_TOKEN=your_personal_access_token
GITHUB_REPO=username/repo-name
```

### Commit Convention
All agent commits follow this format:
```
EOD YYYY-MM-DD @ HH:MM — [summary]

## Tasks Completed
- ✅ Task name
...
🤖 Auto-committed by Git Agent
```

---

## 3. Memory MCP Server

**Purpose:** Read and write persistent agent memory  
**Config key:** `memory`  
**Backed by:** `agents/memory_manager.py`

### Tools Exposed

| Tool Name | Arguments | What it does |
|---|---|---|
| `save_conversation` | `agent_name, messages` | Persists conversation to JSONL |
| `load_last_conversation` | `agent_name, max_messages` | Restores last session context |
| `log_task_result` | `task_id, status, output, ...` | Appends to task history |
| `get_todays_summary` | — | Returns summary dict of today's work |

### When Agents Use It
- **Every agent** → `log_task_result` (after completing any work)
- **Orchestrator** → `save_conversation`, `load_last_conversation` (context continuity)
- **Git Agent** → `get_todays_summary` (build commit message)

### Storage Layout
```
memory/
├── agent_state.json              ← global agent status
├── conversations/
│   ├── 2026-07-27_09-00_orchestrator.jsonl
│   ├── 2026-07-27_10-30_builder.jsonl
│   └── ...
└── task_history/
    ├── 2026-07-27_task_history.jsonl
    └── ...
```

### Memory Retention
Configured in `config/agent_config.json`:
```json
{ "memory": { "retention_days": 30 } }
```
Files older than `retention_days` are deleted on next run of `cleanup_old_memory()`.

---

## 4. Browser MCP Server

**Purpose:** Automated browser control for UI testing and verification  
**Config key:** `browser`  
**Backed by:** Playwright (`tests/browser/`)

### Tools Exposed

| Tool Name | Arguments | What it does |
|---|---|---|
| `navigate` | `url` | Open a URL in Chromium |
| `click` | `selector` | Click an element |
| `screenshot` | `filename` | Capture page screenshot |
| `get_text` | `selector` | Read element text |
| `fill_form` | `selector, value` | Type into an input field |

### When Agents Use It
- **Tester Agent** → Runs `tests/browser/test_dashboard_loads.py` using Playwright
- **Sprint Watcher** → Triggers browser tests after Builder completes a frontend task

### Browser Test Files
| File | What it tests |
|---|---|
| `test_dashboard_loads.py` | Homepage renders, KPI cards visible, charts present |
| `test_csv_upload.py` (planned) | Full CSV upload + model training flow |

### Environment Variables Required
```env
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
```

### Running Browser Tests Manually
```bash
# Make sure frontend is running at :5173 first!
pytest tests/browser/ -v

# View HTML report
open reports/browser_test_report.html
```

---

## MCP Client (`mcp_client.py`)

**File:** `agents/mcp_client.py` *(to be implemented)*

The MCP Client is the **routing layer** that agents import. Instead of calling `plane_agent.py` directly, agents call:

```python
from mcp_client import call_tool

# Route automatically to correct MCP server
result = call_tool("create_task", {
    "title": "Add pie chart endpoint",
    "priority": "high",
    "story_points": 3
})
```

This decouples agents from specific implementations — you can swap the Plane backend without changing any agent code.

### How it routes
```python
TOOL_SERVER_MAP = {
    "create_task":          "plane",
    "update_task_status":   "plane",
    "git_commit":           "github",
    "git_push":             "github",
    "save_conversation":    "memory",
    "navigate":             "browser",
    ...
}
```

---

## Security Notes

> [!CAUTION]
> Never commit `.env` to git. All API tokens are loaded via `python-dotenv` from `.env` which is in `.gitignore`.

> [!NOTE]
> MCP tool calls are logged to `memory/task_history/` for full auditability.

---

## Adding a New MCP Server

1. Create your server module in `agents/my_new_agent.py`
2. Add it to `mcp_servers/mcp_config.json`:
   ```json
   "my_server": {
     "description": "...",
     "command": "python",
     "args": ["-m", "agents.my_new_agent"],
     "tools": ["my_tool_1", "my_tool_2"]
   }
   ```
3. Add tool routing in `agents/mcp_client.py`'s `TOOL_SERVER_MAP`
4. Any agent can now call `call_tool("my_tool_1", {...})`
