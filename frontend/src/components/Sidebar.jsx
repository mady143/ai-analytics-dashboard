import { useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, BarChart3, LineChart, Bot, 
  GitBranch, Database, Settings, ChevronRight, Activity
} from 'lucide-react'

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard, section: 'MAIN' },
  { path: '/analytics', label: 'Analytics', icon: BarChart3, section: 'MAIN' },
  { path: '/charts', label: 'Charts Explorer', icon: LineChart, section: 'MAIN' },
  { path: '/data', label: 'Data Manager', icon: Database, section: 'DATA' },
  { path: '/agents', label: 'Agent Monitor', icon: Bot, section: 'AGENTS' },
  { path: '/sprints', label: 'Sprint Board', icon: GitBranch, section: 'AGENTS' },
]

export default function Sidebar() {
  const location = useLocation()
  const [agentStatus] = useState({
    orchestrator: 'idle',
    builder: 'idle',
    tester: 'idle',
    git: 'idle'
  })

  const sections = [...new Set(navItems.map(n => n.section))]

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="logo-icon">📊</div>
        <div>
          <div className="logo-text">AI Analytics</div>
          <div className="logo-subtitle">Agentic Dashboard</div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        {sections.map(section => (
          <div key={section}>
            <div className="nav-section-label">{section}</div>
            {navItems
              .filter(item => item.section === section)
              .map(item => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={`nav-item ${isActive ? 'active' : ''}`}
                  >
                    <Icon size={18} className="nav-icon" />
                    <span>{item.label}</span>
                    {isActive && <ChevronRight size={14} style={{ marginLeft: 'auto', opacity: 0.5 }} />}
                  </NavLink>
                )
              })}
          </div>
        ))}
      </nav>

      {/* Agent Status Footer */}
      <div style={{ 
        padding: '16px 8px', 
        borderTop: '1px solid var(--border-subtle)',
        marginTop: 'auto'
      }}>
        <div className="nav-section-label" style={{ paddingTop: 0 }}>AGENT STATUS</div>
        {Object.entries(agentStatus).map(([name, status]) => (
          <div key={name} style={{ 
            display: 'flex', alignItems: 'center', gap: '8px',
            padding: '6px 8px', fontSize: '12px', color: 'var(--text-secondary)'
          }}>
            <span className={`status-dot ${status}`} />
            <span style={{ textTransform: 'capitalize' }}>{name}</span>
            <span style={{ marginLeft: 'auto', fontSize: '10px', color: 'var(--text-muted)' }}>
              {status}
            </span>
          </div>
        ))}
      </div>
    </aside>
  )
}
