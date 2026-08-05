# 📌 TASK 29 — Continuous MCP Servers Uptime & Fleet Synchronization (`#mcp-servers-uptime`)

## 📋 Task Overview
This task specification governs the **Continuous Execution & Health Supervision** of Model Context Protocol (MCP) servers within the AI Analytics Dashboard infrastructure.

---

## 🔌 Active MCP Servers & Configurations
- **Plane MCP Server:** Handles Plane PM REST API task creation, status updates, cycle tracking, and sprint task synchronization.
  - Script: [`agents/plane_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/plane_agent.py) / [`mcp_servers/plane/`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/mcp_servers/)
- **Git MCP Server:** Handles pre-approved Git automation, anti-spam commit filtering, branch merging, and GitHub API interactions.
  - Script: [`agents/git_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/git_agent.py)
- **Memory MCP Server:** Maintains agent state, daily conversation logs, and task history.
  - Script: [`agents/memory_manager.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/memory_manager.py)
- **Browser MCP Server:** Controls Playwright Chromium browser sessions for automated E2E testing.

---

## ⚡ Operational Uptime Rules
1. **Mandatory Continuous Execution:** MCP servers MUST run continuously alongside FastAPI (`:8000`) and Vite (`:5173`).
2. **Automated Launchers:** Launched automatically via [`scripts/start_all_services.bat`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/start_all_services.bat) and [`scripts/start_all_services.sh`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/start_all_services.sh).
3. **Watchdog Supervision:** Monitored by `scripts/agent_watchdog.py`. If an MCP server disconnects or crashes, the watchdog automatically relaunches it.
