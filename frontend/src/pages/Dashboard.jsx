import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import InventoryRiskForecast from '../components/InventoryRiskForecast'
import KPICard from '../components/KPICard'
import WarehouseSalesAnalytics from '../components/WarehouseSalesAnalytics'
import WarehouseAnalytics from '../components/WarehouseAnalytics'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  ScatterChart, Scatter, Cell
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

const DEFAULT_KPIS = [
  { title: "TOTAL WAREHOUSES", value: "5", unit: "Facilities", trend: 0.0, trend_direction: "up", color: "#7C3AED" },
  { title: "CASES BUILT (cases_bld)", value: "8,940", unit: "Cases", trend: 8.4, trend_direction: "up", color: "#06B6D4" },
  { title: "ORIGINAL ORDER QTY", value: "9,100", unit: "Cases", trend: 6.2, trend_direction: "up", color: "#F59E0B" },
  { title: "INVOICES PROCESSED", value: "384", unit: "Invoices", trend: 4.1, trend_direction: "up", color: "#10B981" },
  { title: "FULFILLMENT RATE", value: "98.2%", unit: "Target 95%", trend: 2.1, trend_direction: "up", color: "#34D399" },
  { title: "SCRATCH RATE", value: "1.8%", unit: "160 Cases", trend: -1.5, trend_direction: "down", color: "#EF4444" }
]

const DEFAULT_SCATTER = Array.from({ length: 80 }, (_, i) => {
  const x = Math.floor(Math.random() * 1300) + 150
  const y = x - Math.floor(Math.random() * 60)
  return { x, y, color: ["01", "02", "58", "61", "71"][i % 5] }
})

export default function Dashboard() {
  const [kpis, setKpis] = useState(DEFAULT_KPIS)
  const [barData, setBarData] = useState([
    { label: "01", value: 1540 },
    { label: "02", value: 1820 },
    { label: "58", value: 2310 },
    { label: "61", value: 1980 },
    { label: "71", value: 2150 }
  ])
  const [scatterData, setScatterData] = useState(DEFAULT_SCATTER)

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [kpiRes, barRes, scatterRes] = await Promise.all([
          axios.get(`${API}/api/charts/kpi`),
          axios.get(`${API}/api/charts/bar`),
          axios.get(`${API}/api/charts/scatter`)
        ])
        if (kpiRes.data?.kpis) setKpis(kpiRes.data.kpis)
        if (barRes.data?.data) setBarData(barRes.data.data)
        if (scatterRes.data?.data) setScatterData(scatterRes.data.data)
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err)
      }
    }
    fetchAll()
  }, [])

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <div className="page-header">
        <h1 className="page-title">📊 Warehouse Sales & Invoice Analytics Dashboard</h1>
        <p className="page-subtitle">Sprint AAD-5 Specification · Real-time Warehouse Item & Procurement Analytics</p>
      </div>

      {/* Warehouse Level KPI Grid */}
      <div className="kpi-grid">
        {kpis.map((kpi, i) => (
          <KPICard key={kpi.title} {...kpi} index={i} />
        ))}
      </div>

      {/* Warehouse Charts Grid */}
      <div className="chart-grid" style={{ marginTop: '24px' }}>
        {/* Bar Chart */}
        <motion.div
          className="chart-card"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
        >
          <div className="chart-title">🔥 Cases Built by Warehouse</div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={barData} margin={{ top: 5, right: 10, bottom: 5, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="label" tick={{ fill: '#8B949E', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#8B949E', fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(124,58,237,0.08)' }} />
              <Bar dataKey="value" name="Cases Built Qty" radius={[6, 6, 0, 0]}>
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
          <div className="chart-title">📈 Original Order Qty vs Cases Built</div>
          <ResponsiveContainer width="100%" height={280}>
            <ScatterChart margin={{ top: 5, right: 10, bottom: 5, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis type="number" dataKey="x" name="Order Qty" tick={{ fill: '#8B949E', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis type="number" dataKey="y" name="Cases Built" tick={{ fill: '#8B949E', fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} content={<CustomTooltip />} />
              <Scatter name="Order vs Built" data={scatterData} fill="#06B6D4" opacity={0.8} />
            </ScatterChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Feature Component: Warehouse Sales & Invoice Analytics (Sprint AAD-5) */}
      <WarehouseSalesAnalytics />

      {/* Warehouse Inventory Level Statistics */}
      <WarehouseAnalytics />

      {/* Inventory Risk Anomaly Forecast */}
      <div style={{ marginTop: '24px' }}>
        <InventoryRiskForecast />
      </div>
    </motion.div>
  )
}
