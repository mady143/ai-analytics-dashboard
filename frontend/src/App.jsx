import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Menu } from 'lucide-react'
import Sidebar from './components/Sidebar'
import Footer from './components/Footer'
import Dashboard from './pages/Dashboard'
import Analytics from './pages/Analytics'
import SprintBoard from './pages/SprintBoard'
import AgentMonitor from './pages/AgentMonitor'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 5 * 60 * 1000, retry: 2 }
  }
})

// Placeholder pages for sections not yet built
const Placeholder = ({ title, emoji }) => (
  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '60vh', gap: 16 }}>
    <span style={{ fontSize: 64 }}>{emoji}</span>
    <h2 style={{ color: 'var(--text-primary)', fontSize: 24, fontWeight: 700 }}>{title}</h2>
    <p style={{ color: 'var(--text-secondary)' }}>This page is being built by the AI agents...</p>
    <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
      {[...Array(3)].map((_, i) => (
        <div key={i} style={{
          width: 8, height: 8, borderRadius: '50%',
          background: 'var(--color-primary)',
          animation: `pulse ${0.8 + i * 0.2}s ease-in-out infinite alternate`
        }} />
      ))}
    </div>
  </div>
)

function AppContent() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  const toggleSidebar = () => {
    setSidebarCollapsed(prev => !prev)
  }

  return (
    <div className="app-layout">
      <Sidebar collapsed={sidebarCollapsed} onToggle={toggleSidebar} />

      <main className="main-content" style={{
        marginLeft: sidebarCollapsed ? '0' : 'var(--sidebar-width)',
        maxWidth: sidebarCollapsed ? '100vw' : 'calc(100vw - var(--sidebar-width))',
        transition: 'all 0.3s ease'
      }}>
        {/* Floating 3-Line Enable Nav Bar Button when Collapsed */}
        {sidebarCollapsed && (
          <button
            id="nav-bar-enable-btn"
            onClick={toggleSidebar}
            title="Enable/Show Navigation Bar"
            style={{
              position: 'fixed',
              top: '16px',
              left: '16px',
              zIndex: 101,
              background: 'var(--bg-card)',
              border: '1px solid var(--border-primary)',
              color: 'var(--color-primary-light)',
              padding: '8px 12px',
              borderRadius: '8px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              boxShadow: 'var(--shadow-card)',
              fontSize: '13px',
              fontWeight: 600
            }}
          >
            <Menu size={18} />
            <span>Enable Nav Bar</span>
          </button>
        )}

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/charts" element={<Placeholder title="Charts Explorer" emoji="📈" />} />
          <Route path="/data" element={<Placeholder title="Data Manager" emoji="🗄️" />} />
          <Route path="/agents" element={<AgentMonitor />} />
          <Route path="/sprints" element={<SprintBoard />} />
        </Routes>

        {/* Footer Component */}
        <Footer />
      </main>
    </div>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AppContent />
      </Router>
    </QueryClientProvider>
  )
}
