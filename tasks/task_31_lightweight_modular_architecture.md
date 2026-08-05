# 📌 TASK 31 — Lightweight Modular Architecture & 300-Line File Limit Policy (`#lightweight-architecture`)

## 📋 Task Overview & Directive
This task specification enforces a strict **Lightweight, Modular File Structure** across the codebase to ensure high performance, easy maintainability, smooth application execution, and scalability.

---

## 🚨 Mandatory Architectural Directives

### 1. Strict 300-Line Code Limit Per File
- **Rule:** NO Python backend file, agent script, or React component file in the application codebase should exceed **300 lines of code**.
- **Refactoring Requirement:** Whenever a file approaches or exceeds 300 lines, developers/agents MUST refactor helper functions, data structures, and intent logic into dedicated sub-modules (e.g., `agents/builder_nlp.py`, `agents/builder_llm.py`, `backend/routers/analytics_helpers.py`) and import them cleanly.

### 2. Clean Import & Dependency Flow
- Maintain lightweight entry points that import focused, single-responsibility helper modules.
- Eliminate monolithic bloated files to ensure fast file I/O, rapid unit testing, zero execution lag, and easy comprehension for AI agents and human developers alike.

---

## 🧪 Verification & Enforcement
- Run file line count audit:
  ```bash
  python -c "import glob; files = glob.glob('agents/*.py') + glob.glob('backend/**/*.py', recursive=True); print([(f, len(open(f, encoding='utf-8', errors='ignore').readlines())) for f in files if len(open(f, encoding='utf-8', errors='ignore').readlines()) > 300])"
  ```
- Target: **0 files > 300 lines**.
