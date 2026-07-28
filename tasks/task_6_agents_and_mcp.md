# 📌 TASK 6 — Autonomous Agent Network & Background Services (`#background-agent-system`)

## 🖥️ Agent & Service Locations
- **Directory:** [`agents/`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/) & [`scripts/`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/)
- **Configuration:** [`mcp_servers/mcp_config.json`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/mcp_servers/mcp_config.json)

---

## 🎯 Sub-Task Breakdown

### Sub-Task 6.1: 🤖 Sprint Watcher Agent (`run_sprint_watcher.py`)
- **Command:** `python scripts/run_sprint_watcher.py --interval 60`
- **Behavior:** Polls Plane workspace `agentbuilder` every 60s for new tasks, task state updates, and comments.

### Sub-Task 6.2: 🚀 FastAPI Backend API Server
- **Command:** `python -m uvicorn main:app --host 127.0.0.1 --port 8000`
- **URL:** [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Sub-Task 6.3: 💻 Vite Frontend Dev Server
- **Command:** `npm run dev` (inside `frontend/`)
- **URL:** [http://localhost:5173](http://localhost:5173)

### Sub-Task 6.4: 🔌 MCP Server Fleet (`mcp_servers/mcp_config.json`)
- **Plane MCP:** `agents.plane_agent`
- **GitHub MCP:** `github-mcp-server`
- **Memory MCP:** `agents.memory_manager`
- **Browser MCP:** `playwright`

### Sub-Task 6.5: 🩺 Step 0 Pre-Execution Health Check Directive
- **Rule:** Before processing any user request or code modification, verify all background agents and servers are running. Auto-restart any stopped service immediately.

### Sub-Task 6.6: ⚡ MCP & Sprint Watcher Automated Execution Pipeline (2026-07-28)
- **Mandatory Lifecycle Pipeline:**
  - Whenever Sprint Watcher or Plane MCP detects a new task, task state change, or user comment:
    1. **Code Implementation:** Builder agent writes/updates backend Python or React UI files.
    2. **Server Restart & Reload:** Restart/reload FastAPI backend and Vite frontend servers.
    3. **Unit Testing:** Run full unit test suite (`pytest tests/unit/`).
    4. **Browser Testing & Interactive Verification:** Reload Playwright browser, test interactive form parameter switching (date + target DB + Submit click), and verify populated KPI cards, charts, and table.
    5. **Strict Push Gate:** Push code to remote Git ONLY after 100% test pass rate and populated data verification.
