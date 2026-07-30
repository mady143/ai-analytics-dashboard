"""
conftest_excel.py - Run Excel generation via pytest (no python permission prompt needed)
Usage: pytest tests/conftest_excel.py -v -s
"""
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent


def test_generate_excel_report():
    """Generate TEST_CASES.xlsx via pytest (no permission prompt needed)."""
    sys.path.insert(0, str(ROOT / "tests"))

    # Run via importlib to avoid subprocess python call
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "generate_test_excel",
        str(ROOT / "tests" / "generate_test_excel.py")
    )
    mod = importlib.util.load_from_spec(spec)
    spec.loader.exec_module(mod)

    print("[TEST] Running unit tests to collect results...")
    passed, failed, output = mod.run_unit_tests_and_get_results()
    print(f"   Pytest collected: {len(passed)} passed, {len(failed)} failed")

    out_path = mod.create_excel(passed, failed)
    assert out_path.exists(), f"TEST_CASES.xlsx was not created at {out_path}"
    print(f"[OK] TEST_CASES.xlsx generated: {out_path}")
