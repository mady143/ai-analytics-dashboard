# 🧪 Sprint Test Cases Specification (`sprint_test_cases.md`)

This document records the unit and browser automation test cases for each sprint component.

---

## 🔹 Sprint Task: "Add The Nav bar"

### 1. Unit Test Suite: [`tests/unit/test_navbar.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/unit/test_navbar.py)

- **Test Case 1: `test_navbar_file_exists`**
  - **Goal:** Verify component source file [`Navbar.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/Navbar.jsx) exists in project structure.
  - **Result:** `PASSED`

- **Test Case 2: `test_navbar_structure`**
  - **Goal:** Validate export statement and brand title text `"AI Analytics Dashboard"`.
  - **Result:** `PASSED`

---

### 2. Browser Automation Test Suite: [`tests/browser/test_dashboard_loads.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/browser/test_dashboard_loads.py)

- **Test Case 1: `test_navbar_renders`**
  - **Goal:** Launch Playwright Chromium, navigate to `http://localhost:5173/`, and verify selector `.navbar` is visible.
  - **Result:** `PASSED`

- **Test Case 2: `test_dashboard_loads`**
  - **Goal:** Verify page title matches `"AI Analytics Dashboard"` and KPI cards render.
  - **Result:** `PASSED`

- **Test Case 3: `test_sidebar_navigation`**
  - **Goal:** Click sidebar link `.sidebar a[href='/analytics']` and verify URL updates to `http://localhost:5173/analytics`.
  - **Result:** `PASSED`
