"""
Run Tests Script — Execute full test suite and generate reports.
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
ROOT_DIR = Path(__file__).parent.parent
REPORTS_DIR = ROOT_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


def run_unit_tests():
    console.print("\n[bold cyan]🧪 Running Unit Tests...[/bold cyan]")
    report_path = REPORTS_DIR / "unit_test_report.html"
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit/", "-v", "--tb=short",
         f"--html={report_path}", "--self-contained-html"],
        cwd=str(ROOT_DIR),
        capture_output=True, text=True
    )
    return result.returncode == 0, result.stdout, str(report_path)


def run_chart_tests():
    console.print("\n[bold cyan]📊 Running Chart Tests...[/bold cyan]")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit/test_charts.py", "-v"],
        cwd=str(ROOT_DIR), capture_output=True, text=True
    )
    return result.returncode == 0, result.stdout


def print_summary(unit_ok, unit_out, report_path):
    table = Table(title=f"Test Results — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    table.add_column("Suite", style="cyan")
    table.add_column("Status")
    table.add_column("Report")

    unit_status = "[green]✅ PASSED[/green]" if unit_ok else "[red]❌ FAILED[/red]"
    table.add_row("Unit Tests", unit_status, report_path)
    console.print(table)

    if unit_ok:
        console.print(Panel("[bold green]✅ All tests passed![/bold green]", border_style="green"))
    else:
        console.print(Panel("[bold red]❌ Some tests failed. Check reports.[/bold red]", border_style="red"))
        console.print(unit_out[-2000:])


if __name__ == "__main__":
    console.print(Panel.fit("[bold]🧪 AI Analytics Dashboard — Test Runner[/bold]", border_style="cyan"))
    unit_ok, unit_out, report_path = run_unit_tests()
    print_summary(unit_ok, unit_out, report_path)
    sys.exit(0 if unit_ok else 1)
