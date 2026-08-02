import { useState, useEffect } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import axios from 'axios'
import { 
  LayoutDashboard, BarChart3, LineChart, Bot, 
  GitBranch, Database, Settings, ChevronRight, Activity, Menu, EyeOff, X
} from 'lucide-react'

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard, section: 'MAIN' },
  { path: '/analytics', label: 'Analytics', icon: BarChart3, section: 'MAIN' },
  { path: '/charts', label: 'Charts Explorer', icon: LineChart, section: 'MAIN' },
  { path: '/data', label: 'Data Manager', icon: Database, section: 'DATA' },
  { path: '/agents', label: 'Agent Monitor', icon: Bot, section: 'AGENTS' },
  { path: '/sprints', label: 'Sprint Board', icon: GitBranch, section: 'AGENTS' },
]

export default function Sidebar({ collapsed, onToggle, onHide }) {
  const location = useLocation()
  const [agentsData, setAgentsData] = useState({
    orchestrator: { status: 'running', current_task: 'Task & Agent State Coordination Active' },
    builder: { status: 'running', current_task: 'Autonomous Builder Agent Active' },
    tester: { status: 'running', current_task: 'Automated Pytest & Playwright Suite Active' },
    git: { status: 'running', current_task: 'Continuous EOD Auto-Push Active' },
    sprint_watcher: { status: 'running', current_task: 'Watching sprint (60s Polling Loop Active)' }
  })

  useEffect(() => {
    const fetchStatus = () => {
      axios.get('/api/agents/status')
        .then(res => {
          if (res.data?.agents) {
            const raw = res.data.agents
            setAgentsData({
              orchestrator: raw.orchestrator || { status: 'running', current_task: 'Task & Agent State Coordination Active' },
              builder: raw.builder || { status: 'running', current_task: 'Autonomous Builder Agent Active' },
              tester: raw.tester || { status: 'running', current_task: 'Automated Pytest & Playwright Suite Active' },
              git: raw.git_agent || raw.git || { status: 'running', current_task: 'Continuous EOD Auto-Push Active' },
              sprint_watcher: raw.sprint_watcher || { status: 'running', current_task: 'Watching sprint (60s Polling Loop Active)' }
            })
          }
        })
        .catch(() => {})
    }
    fetchStatus()
    const timer = setInterval(fetchStatus, 4000)
    return () => clearInterval(timer)
  }, [])

  const sections = [...new Set(navItems.map(n => n.section))]

  return (
    <aside
      className={`sidebar ${collapsed ? 'collapsed' : ''}`}
      style={{
        width: collapsed ? '72px' : '260px',
        minWidth: collapsed ? '72px' : '260px',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        overflowX: 'hidden'
      }}
    >
      {/* Logo, Three-Line Toggle, & Hide Component Header */}
      <div
        className="sidebar-logo"
        style={{
          display: 'flex',
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: collapsed ? 'center' : 'space-between',
          padding: collapsed ? '14px 2px' : '16px 12px',
          gap: collapsed ? '5px' : '0px',
          width: '100%'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div
            className="logo-icon"
            title="AI Analytics · Agentic Dashboard"
            style={{
              width: collapsed ? '30px' : '40px',
              height: collapsed ? '30px' : '40px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              borderRadius: collapsed ? '6px' : '12px'
            }}
            onClick={collapsed ? onToggle : undefined}
          >
            <BarChart3 size={collapsed ? 16 : 20} color="#7C3AED" />
          </div>
          {!collapsed && (
            <div>
              <div className="logo-text">AI Analytics</div>
              <div className="logo-subtitle">Agentic Dashboard</div>
            </div>
          )}
        </div>

        {/* Action Buttons: Toggle (Collapse/Expand) & Hide Entire Component */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
          {/* Three Line Toggle Button */}
          <button
            id="sidebar-toggle-btn"
            onClick={onToggle}
            title={collapsed ? "Enable Nav Bar (AI Analytics)" : "Disable Nav Bar"}
            aria-label={collapsed ? "Enable Nav Bar" : "Disable Nav Bar"}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#FFFFFF',
              padding: '6px',
              borderRadius: '6px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: collapsed ? '30px' : '36px',
              height: collapsed ? '30px' : '36px',
              transition: 'all 0.2s ease'
            }}
          >
            <Menu size={22} color="#FFFFFF" strokeWidth={2.5} />
          </button>

          {/* Hide Left Nav Bar Component Button */}
          {onHide && !collapsed && (
            <button
              id="sidebar-hide-btn"
              onClick={onHide}
              title="Hide Left Side Nav Bar"
              aria-label="Hide Left Side Nav Bar"
              style={{
                background: 'rgba(239, 68, 68, 0.12)',
                border: '1px solid rgba(239, 68, 68, 0.3)',
                color: '#ef4444',
                padding: '6px',
                borderRadius: '6px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                height: '40px',
                width: '32px'
              }}
            >
              <EyeOff size={16} />
            </button>
          )}
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="sidebar-nav">
        {sections.map(section => (
          <div key={section}>
            {!collapsed && <div className="nav-section-label">{section}</div>}
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
                    title={collapsed ? item.label : undefined}
                    style={{
                      justifyContent: collapsed ? 'center' : 'flex-start',
                      padding: collapsed ? '10px 0' : '10px 14px'
                    }}
                  >
                    <Icon size={18} className="nav-icon" />
                    {!collapsed && <span>{item.label}</span>}
                    {!collapsed && isActive && <ChevronRight size={14} style={{ marginLeft: 'auto', opacity: 0.5 }} />}
                  </NavLink>
                )
              })}
          </div>
        ))}
      </nav>

      {/* Agent Status Footer with Live Current Task Visibility */}
      {!collapsed && (
        <div style={{ 
          padding: '14px 8px', 
          borderTop: '1px solid var(--border-subtle)',
          marginTop: 'auto'
        }}>
          <div className="nav-section-label" style={{ paddingTop: 0, marginBottom: '6px' }}>AGENT STATUS</div>
          {Object.entries(agentsData).map(([name, info]) => {
            const status = info.status || 'running';
            const taskDesc = info.current_task || 'Active';
            const isWorking = taskDesc.includes('🔨') || taskDesc.includes('🧪') || taskDesc.includes('Picked up') || taskDesc.includes('Building') || taskDesc.includes('Implementing');

            return (
              <div key={name} title={taskDesc} style={{ 
                padding: '5px 8px', borderRadius: '6px', marginBottom: '4px',
                background: isWorking ? 'rgba(124, 58, 237, 0.12)' : 'transparent',
                border: isWorking ? '1px solid rgba(124, 58, 237, 0.3)' : '1px solid transparent',
                transition: 'all 0.2s ease'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: 'var(--text-secondary)' }}>
                  <span className={`status-dot ${status}`} />
                  <span style={{ textTransform: 'capitalize', fontWeight: 600, color: 'var(--text-primary)' }}>{name.replace('_', ' ')}</span>
                  <span style={{ marginLeft: 'auto', fontSize: '10px', color: isWorking ? '#a78bfa' : 'var(--text-muted)', fontWeight: isWorking ? 700 : 400 }}>
                    {isWorking ? 'WORKING ⚡' : status}
                  </span>
                </div>
                <div style={{
                  fontSize: '10px',
                  color: isWorking ? '#c4b5fd' : 'var(--text-muted)',
                  marginTop: '2px',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  paddingLeft: '14px'
                }}>
                  {taskDesc}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </aside>
  )
}
