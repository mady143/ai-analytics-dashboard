# 📌 TASK 8 — Continuous Parallel Background Agent Fleet (`#background-agent-fleet`)

## 🖥️ Location & File References
- **Script Files:**
  - [`scripts/run_sprint_watcher.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/run_sprint_watcher.py)
  - [`agents/sprint_watcher_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/sprint_watcher_agent.py)
  - [`agents/orchestrator_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/orchestrator_agent.py)
  - [`agents/builder_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/builder_agent.py)
  - [`agents/tester_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/tester_agent.py)
  - [`memory/agent_state.json`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/agent_state.json)

---

## 🎯 Sub-Task Breakdown

### Sub-Task 8.1: 🤖 Sprint Watcher Agent Continuous Polling
- **Command:** `python scripts/run_sprint_watcher.py --interval 60`
- **Behavior:** Runs continuously in the background, polling Plane workspace `agentbuilder` every 60 seconds to detect new tasks, task state changes, and new user comments.

### Sub-Task 8.2: ⚡ Non-Blocking Parallel Execution Architecture
- **Rule:** All agents run in parallel background tasks without blocking terminal execution or freezing the main loop.
- **Agent Fleet:**
  1. `sprint_watcher`: Continuous 60s task & comment polling
  2. `orchestrator`: Master task breakdown and coordination
  3. `builder`: Code writing & component implementation
  4. `tester`: Automated pytest unit tests & Playwright browser tests
  5. `git_agent`: Git synchronization & commit management

### Sub-Task 8.3: 🩺 Agent Auto-Restart & State Persistence
- **State File:** `memory/agent_state.json`
- **Auto-Restart Rule:** The USER will NOT run agent scripts manually. If any background agent is stopped, killed, or idle, the system MUST automatically restart it in background mode immediately.
