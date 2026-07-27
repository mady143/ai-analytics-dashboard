"""
Tester Agent — Runs unit tests (pytest) and browser tests (Playwright).
Reports results to Plane and memory.
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

from memory_manager import update_agent_status, log_task_result, save_state, load_state

console = Console()
ROOT_DIR = Path(__file__).parent.parent
TESTS_DIR = ROOT_DIR / "tests"
REPORTS_DIR = ROOT_DIR / "reports"


def _run_command(cmd: list[str], cwd: Path = ROOT_DIR) -> tuple[str, str, int]:
    """Run a shell command and return (stdout, stderr, returncode)."""
    result = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode


def run_unit_tests() -> dict:
    """Run pytest unit tests and return structured results."""
    console.print("\n[bold cyan]🧪 Running Unit Tests...[/bold cyan]")
    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / "unit_test_report.html"

    stdout, stderr, code = _run_command([
        "python", "-m", "pytest",
        "tests/unit/",
        "-v",
        "--tb=short",
        f"--html={report_path}",
        "--self-contained-html",
        "-q"
    ])

    passed = stdout.count(" PASSED")
    failed = stdout.count(" FAILED")
    errors = stdout.count(" ERROR")

    result = {
        "type": "unit",
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "total": passed + failed + errors,
        "success": code == 0,
        "output": stdout[-3000:],  # Last 3000 chars
        "report": str(report_path),
        "timestamp": datetime.now().isoformat()
    }

    if code == 0:
        console.print(f"[bold green]✅ Unit tests PASSED: {passed}/{result['total']}[/bold green]")
    else:
        console.print(f"[bold red]❌ Unit tests FAILED: {failed} failures, {errors} errors[/bold red]")
        console.print(stderr[-1000:])

    return result


def run_browser_tests() -> dict:
    """Run Playwright browser tests."""
    console.print("\n[bold cyan]🌐 Running Browser Tests...[/bold cyan]")
    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / "browser_test_report.html"

    # Check if playwright is installed
    _, _, install_code = _run_command(["python", "-m", "playwright", "install", "chromium", "--with-deps"])

    stdout, stderr, code = _run_command([
        "python", "-m", "pytest",
        "tests/browser/",
        "-v",
        "--tb=short",
        f"--html={report_path}",
        "--self-contained-html",
        "-q"
    ])

    passed = stdout.count(" PASSED")
    failed = stdout.count(" FAILED")

    result = {
        "type": "browser",
        "passed": passed,
        "failed": failed,
        "total": passed + failed,
        "success": code == 0,
        "output": stdout[-3000:],
        "report": str(report_path),
        "timestamp": datetime.now().isoformat()
    }

    if code == 0:
        console.print(f"[bold green]✅ Browser tests PASSED: {passed}/{result['total']}[/bold green]")
    else:
        console.print(f"[bold red]❌ Browser tests FAILED: {failed} failures[/bold red]")

    return result


def run_all_tests() -> dict:
    """Run both unit and browser tests, return combined results."""
    update_agent_status("tester", "running", "Full test suite")

    console.print(Panel.fit(
        "[bold]🧪 Tester Agent — Full Test Suite[/bold]\n"
        f"[dim]{datetime.now().strftime('%Y-%m-%d %H:%M')}[/dim]",
        border_style="cyan"
    ))

    unit_results = run_unit_tests()
    browser_results = run_browser_tests()

    combined = {
        "unit": unit_results,
        "browser": browser_results,
        "total_passed": unit_results["passed"] + browser_results["passed"],
        "total_failed": unit_results["failed"] + browser_results["failed"],
        "all_passed": unit_results["success"] and browser_results["success"],
        "timestamp": datetime.now().isoformat()
    }

    # Update state with test results
    state = load_state()
    if "agents" not in state:
        state["agents"] = {}
    if "tester" not in state["agents"]:
        state["agents"]["tester"] = {}
    state["agents"]["tester"]["last_test_results"] = {
        "unit": unit_results["success"],
        "browser": browser_results["success"],
        "passed": combined["total_passed"],
        "failed": combined["total_failed"]
    }
    save_state(state)

    # Log result
    status = "completed" if combined["all_passed"] else "failed"
    log_task_result(
        "TEST-RUN",
        "Full Test Suite",
        "tester",
        status,
        f"Unit: {unit_results['passed']}/{unit_results['total']} | Browser: {browser_results['passed']}/{browser_results['total']}",
        test_results=combined
    )

    update_agent_status("tester", "idle")

    if combined["all_passed"]:
        console.print(Panel(
            f"[bold green]✅ ALL TESTS PASSED![/bold green]\n"
            f"Unit: {unit_results['passed']}/{unit_results['total']} | "
            f"Browser: {browser_results['passed']}/{browser_results['total']}",
            border_style="green"
        ))
    else:
        console.print(Panel(
            f"[bold red]❌ TESTS FAILED[/bold red]\n"
            f"Unit failed: {unit_results['failed']} | "
            f"Browser failed: {browser_results['failed']}",
            border_style="red"
        ))

    return combined


if __name__ == "__main__":
    results = run_all_tests()
    print(json.dumps(results, indent=2))
