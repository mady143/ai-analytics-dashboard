import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import axios from 'axios'
import KPICard from '../components/KPICard'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  ScatterChart, Scatter, LineChart, Line, Legend, Cell
} from 'recharts'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const COLORS = ['#7C3AED', '#06B6D4', '#F59E0B', '#10B981', '#EF4444', '#8B5CF6']

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border-subtle)',
        borderRadius: '8px',
        padding: '10px 14px',
        fontSize: '13px'
      }}>
        {label && <p style={{ color: 'var(--text-secondary)', marginBottom: 4 }}>{label}</p>}
        {payload.map((p, i) => (
          <p key={i} style={{ color: p.color || 'var(--text-primary)', fontWeight: 600 }}>
            {p.name}: {typeof p.value === 'number' ? p.value.toLocaleString() : p.value}
          </p>
        ))}
      </div>
    )
  }
  return null
}

export default function Dashboard() {
  const [kpis, setKpis] = useState([])
  const [barData, setBarData] = useState([])
  const [scatterData, setScatterData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [kpiRes, barRes, scatterRes] = await Promise.all([
          axios.get(`${API}/api/charts/kpi`),
          axios.get(`${API}/api/charts/bar?column=department&metric=salary`),
          axios.get(`${API}/api/charts/scatter?x=experience_years&y=salary&color=department`)
        ])
        setKpis(kpiRes.data.kpis)
        setBarData(barRes.data.data)
        setScatterData(scatterRes.data.data)
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchAll()
  }, [])

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <div className="spinner" />
      </div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <div className="page-header">
        <h1 className="page-title">📊 Analytics Dashboard</h1>
        <p className="page-subtitle">Real-time insights powered by AI agents · Auto-refreshes every 5 minutes</p>
      </div>

      {/* KPI Grid */}
      <div className="kpi-grid">
        {kpis.map((kpi, i) => (
          <KPICard key={kpi.title} {...kpi} index={i} />
        ))}
      </div>

      {/* Charts Grid */}
      <div className="chart-grid">
        {/* Bar Chart */}
        <motion.div
          className="chart-card"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
        >
          <div className="chart-title">💰 Avg Salary by Department</div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={barData} margin={{ top: 5, right: 10, bottom: 5, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="label" tick={{ fill: '#8B949E', fontSize: 12 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#8B949E', fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `$${(v/1000).toFixed(0)}k`} />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(124,58,237,0.08)' }} />
              <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                {barData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Scatter Chart */}
        <motion.div
          className="chart-card"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
        >
          <div className="chart-title">📈 Experience vs Salary</div>
          <ResponsiveContainer width="100%" height={280}>
            <ScatterChart margin={{ top: 5, right: 10, bottom: 5, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="x" name="Experience (yrs)" tick={{ fill: '#8B949E', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis dataKey="y" name="Salary" tick={{ fill: '#8B949E', fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `$${(v/1000).toFixed(0)}k`} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} content={<CustomTooltip />} />
              <Scatter data={scatterData} fill="#7C3AED" opacity={0.7} />
            </ScatterChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Quick Stats */}
      <motion.div
        className="card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div className="chart-title" style={{ marginBottom: 0 }}>🤖 Agent Activity</div>
          <span className="badge badge-green">● Live</span>
        </div>
        <div style={{ 
          marginTop: 16, 
          display: 'grid', 
          gridTemplateColumns: 'repeat(4, 1fr)', 
          gap: 16, 
          textAlign: 'center' 
        }}>
          {[
            { label: 'Tasks Today', value: '0', color: 'var(--color-primary-light)' },
            { label: 'Tests Passed', value: '0', color: 'var(--color-green)' },
            { label: 'Files Changed', value: '0', color: 'var(--color-cyan)' },
            { label: 'Git Commits', value: '0', color: 'var(--color-amber)' },
          ].map(stat => (
            <div key={stat.label}>
              <div style={{ fontSize: 28, fontWeight: 700, color: stat.color }}>{stat.value}</div>
              <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 4 }}>{stat.label}</div>
            </div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  )
}
