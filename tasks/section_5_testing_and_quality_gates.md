# 🧪 Section 5: Testing & Quality Gates

This document defines the automated testing procedures, Quality Gate push policies, and regression validation steps.

---

## 1. Test Commands & Quality Gates

### Unit Test Execution
```bash
python -m pytest tests/unit/ -v --tb=short
```
- **Total Test Cases:** 51
- **Quality Gate Policy:** 100% test pass rate required prior to git commit and push.

### Browser (Playwright) E2E Test Execution
```bash
python -m pytest tests/browser/ -v --tb=short
```
- **Total E2E Test Cases:** 14

---

## 2. Mandatory Zero Hardcoding Verification
- **Dates:** No static hardcoded date strings in backend or tests — computed dynamically from live DOM `#global-date-picker` or `datetime`.
- **Warehouses:** Facility numbers extracted dynamically from `/api/warehouse/statistics` or DOM elements.
