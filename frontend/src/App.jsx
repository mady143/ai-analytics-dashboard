import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Analytics from './pages/Analytics'
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

function App() {
  return (
    <>
      <Navbar />
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="app-layout">
          <Sidebar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/charts" element={<Placeholder title="Charts Explorer" emoji="📈" />} />
              <Route path="/data" element={<Placeholder title="Data Manager" emoji="🗄️" />} />
              <Route path="/agents" element={<Placeholder title="Agent Monitor" emoji="🤖" />} />
              <Route path="/sprints" element={<Placeholder title="Sprint Board" emoji="🏃" />} />
            </Routes>
          </main>
        </div>
      </Router>
    </QueryClientProvider>
  )
}

export default App
