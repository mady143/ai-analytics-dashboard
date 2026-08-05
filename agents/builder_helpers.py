"""
Builder Helpers — Helper templates and component generators for Builder Agent.
Keeps agents/builder_agent.py lightweight (< 250 lines).
"""

from pathlib import Path
from rich.console import Console

console = Console(legacy_windows=False)


def build_navbar(root_dir: Path, task_title: str, description: str):
    """Build or update Navbar component in frontend."""
    components_dir = root_dir / "frontend" / "src" / "components"
    components_dir.mkdir(parents=True, exist_ok=True)
    
    navbar_file = components_dir / "Navbar.jsx"
    navbar_code = '''import React from 'react';

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <span className="logo-icon">⚡</span>
          <span className="logo-text">AI Analytics Dashboard</span>
        </div>
        <nav className="navbar-links">
          <a href="#overview" className="nav-link active">Overview</a>
          <a href="#analytics" className="nav-link">ML Analytics</a>
          <a href="#data" className="nav-link">Datasets</a>
          <a href="#agents" className="nav-link">Agent Network</a>
          <a href="#settings" className="nav-link">Settings</a>
        </nav>
        <div className="navbar-actions">
          <span className="status-badge live">● Live Agent Loop</span>
        </div>
      </div>
    </header>
  );
}
'''
    navbar_file.write_text(navbar_code, encoding="utf-8")
    console.print(f"[green]✅ Created Navbar component at {navbar_file}[/green]")

    # Check App.jsx and import Navbar if missing
    app_file = root_dir / "frontend" / "src" / "App.jsx"
    if app_file.exists():
        app_code = app_file.read_text(encoding="utf-8")
        if "Navbar" not in app_code:
            updated_app = "import Navbar from './components/Navbar';\n" + app_code
            if '<div className="app-container">' in updated_app:
                updated_app = updated_app.replace(
                    '<div className="app-container">',
                    '<div className="app-container">\n      <Navbar />'
                )
            elif "return (" in updated_app:
                updated_app = updated_app.replace(
                    "return (",
                    "return (\n    <>\n      <Navbar />"
                )
                if updated_app.endswith(";\n}") or updated_app.endswith("}"):
                    updated_app = updated_app.rstrip("}").rstrip("\n;").rstrip() + "\n    </>\n  );\n}"
            app_file.write_text(updated_app, encoding="utf-8")
            console.print("[green]✅ Integrated Navbar into App.jsx[/green]")

    test_dir = root_dir / "tests" / "unit"
    test_dir.mkdir(parents=True, exist_ok=True)
    test_file = test_dir / "test_navbar.py"
    test_code = '''"""Unit tests for Navbar component integration."""
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

def test_navbar_file_exists():
    navbar_path = ROOT_DIR / "frontend" / "src" / "components" / "Navbar.jsx"
    assert navbar_path.exists(), "Navbar.jsx component file must exist"

def test_navbar_structure():
    navbar_path = ROOT_DIR / "frontend" / "src" / "components" / "Navbar.jsx"
    content = navbar_path.read_text(encoding="utf-8")
    assert "export default function Navbar" in content
    assert "AI Analytics Dashboard" in content
'''
    test_file.write_text(test_code, encoding="utf-8")


def build_warehouse_analytics(root_dir: Path, task_title: str, description: str):
    """Build or update Warehouse Analytics component in frontend."""
    components_dir = root_dir / "frontend" / "src" / "components"
    components_dir.mkdir(parents=True, exist_ok=True)
    
    warehouse_file = components_dir / "WarehouseAnalytics.jsx"
    warehouse_code = '''import React from 'react';

export default function WarehouseAnalytics() {
  return (
    <div className="warehouse-card card" style={{ marginTop: '20px' }}>
      <h3 style={{ fontSize: '18px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px' }}>
        🏢 Warehouse Level Statistics & Metrics
      </h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
        <div style={{ background: 'var(--bg-card)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Total Storage Utilized</div>
          <div style={{ fontSize: '20px', fontWeight: 700, color: 'var(--color-primary)' }}>84.2%</div>
        </div>
        <div style={{ background: 'var(--bg-card)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Active Units Streamed</div>
          <div style={{ fontSize: '20px', fontWeight: 700, color: '#34d399' }}>12,450</div>
        </div>
        <div style={{ background: 'var(--bg-card)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Processing Latency</div>
          <div style={{ fontSize: '20px', fontWeight: 700, color: '#c084fc' }}>18 ms</div>
        </div>
      </div>
    </div>
  );
}
'''
    warehouse_file.write_text(warehouse_code, encoding="utf-8")
    console.print(f"[green]✅ Created WarehouseAnalytics component at {warehouse_file}[/green]")

    dashboard_file = root_dir / "frontend" / "src" / "pages" / "Dashboard.jsx"
    if dashboard_file.exists():
        dash_code = dashboard_file.read_text(encoding="utf-8")
        if "WarehouseAnalytics" not in dash_code:
            updated_dash = "import WarehouseAnalytics from '../components/WarehouseAnalytics';\n" + dash_code
            if "</motion.div>" in updated_dash:
                updated_dash = updated_dash.replace("</motion.div>", "  <WarehouseAnalytics />\n    </motion.div>")
            dashboard_file.write_text(updated_dash, encoding="utf-8")

    test_dir = root_dir / "tests" / "unit"
    test_dir.mkdir(parents=True, exist_ok=True)
    test_file = test_dir / "test_warehouse_analytics.py"
    test_code = '''"""Unit tests for WarehouseAnalytics component."""
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

def test_warehouse_file_exists():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "WarehouseAnalytics.jsx"
    assert file_path.exists(), "WarehouseAnalytics.jsx should exist"

def test_warehouse_structure():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "WarehouseAnalytics.jsx"
    content = file_path.read_text(encoding="utf-8")
    assert "Warehouse Level Statistics" in content
'''
    test_file.write_text(test_code, encoding="utf-8")


def build_dynamic_component(root_dir: Path, task_title: str, description: str):
    """Parse task title/description, create component, integrate into UI, and generate tests."""
    words = [w.capitalize() for w in "".join(c if c.isalnum() or c.isspace() else "" for c in task_title).split()]
    comp_name = "".join(words) or "DynamicComponent"
    
    components_dir = root_dir / "frontend" / "src" / "components"
    components_dir.mkdir(parents=True, exist_ok=True)
    
    comp_file = components_dir / f"{comp_name}.jsx"
    
    comp_code = f'''import React from 'react';

export default function {comp_name}() {{
  return (
    <div className="{comp_name.lower()}-card card" style={{{{ marginTop: '20px' }}}}>
      <h3 style={{{{ fontSize: '18px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px' }}}}>
        ⚡ {task_title}
      </h3>
      <p style={{{{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '16px' }}}}>
        {description or "Autonomous component generated by AI Agent Network."}
      </p>
      <div style={{{{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}}}>
        <div style={{{{ background: 'var(--bg-card)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}}}>
          <div style={{{{ color: 'var(--text-secondary)', fontSize: '12px' }}}}>Metric / Status</div>
          <div style={{{{ fontSize: '20px', fontWeight: 700, color: 'var(--color-primary)' }}}}>Active</div>
        </div>
      </div>
    </div>
  );
}}
'''
    comp_file.write_text(comp_code, encoding="utf-8")
    console.print(f"[green]✅ Created dynamic component {comp_name} at {comp_file}[/green]")

    test_dir = root_dir / "tests" / "unit"
    test_dir.mkdir(parents=True, exist_ok=True)
    test_file = test_dir / f"test_{comp_name.lower()}.py"
    test_code = f'''"""Unit tests for {comp_name} component."""
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

def test_{comp_name.lower()}_exists():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "{comp_name}.jsx"
    assert file_path.exists(), "{comp_name}.jsx component file must exist"
'''
    test_file.write_text(test_code, encoding="utf-8")
