import AiAnalyticsDahsboardDateParaemeter from '../components/AiAnalyticsDahsboardDateParaemeter';
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

// Format today's date as YYYY-MM-DD for <input type="date">
const todayISO = () => {
  const d = new Date()
  return d.toISOString().slice(0, 10)
}

// Convert YYYY-MM-DD → YYYYMMDD for API
const toOerdte = (iso) => iso.replace(/-/g, '')

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
  { title: "CASES BUILT (cases_bld)", value: "—", unit: "Cases", trend: 8.4, trend_direction: "up", color: "#06B6D4" },
  { title: "ORIGINAL ORDER QTY", value: "—", unit: "Cases", trend: 6.2, trend_direction: "up", color: "#F59E0B" },
  { title: "INVOICES PROCESSED", value: "—", unit: "Invoices", trend: 4.1, trend_direction: "up", color: "#10B981" },
  { title: "FULFILLMENT RATE", value: "—", unit: "Target 95%", trend: 2.1, trend_direction: "up", color: "#34D399" },
  { title: "SCRATCH RATE", value: "—", unit: "—", trend: -1.5, trend_direction: "down", color: "#EF4444" }
]

export default function Dashboard() {
  // ── Global Date State — propagates to ALL components on this page ──────────
  const [globalDate, setGlobalDate] = useState(todayISO())
  const [targetDb, setTargetDb] = useState('pg_prod')

  const [kpis, setKpis] = useState(DEFAULT_KPIS)
  const [barData, setBarData] = useState([
    { label: "Whse 01", value: 1540 },
    { label: "Whse 02", value: 1820 },
    { label: "Whse 58", value: 2310 },
    { label: "Whse 61", value: 1980 },
    { label: "Whse 71", value: 2150 }
  ])
  const [scatterData, setScatterData] = useState([])

  // Re-fetch whenever date or DB changes
  useEffect(() => {
    const oerdte = toOerdte(globalDate)

    const fetchAll = async () => {
      try {
        const [kpiRes, barRes, scatterRes] = await Promise.all([
          axios.get(`${API}/api/charts/kpi?oerdte=${oerdte}&target_db=${targetDb}`),
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
    const timer = setInterval(fetchAll, 10000)
    return () => clearInterval(timer)
  }, [globalDate, targetDb])

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* ── Global Date & DB Selector Header ── */}
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 className="page-title">📊 Warehouse Sales &amp; Invoice Analytics Dashboard</h1>
          <p className="page-subtitle">Sprint AAD-5 · Real-time Warehouse Item &amp; Procurement Analytics</p>
        </div>

        {/* Global Date + DB Controls — changing these re-fetches ALL components */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: '16px', flexWrap: 'wrap',
          background: 'var(--bg-card)', border: '1px solid var(--border-color)',
          borderRadius: '10px', padding: '10px 16px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: 600 }}>📅 Order Date (Global):</span>
            <input
              id="global-date-picker"
              type="date"
              value={globalDate}
              onChange={(e) => setGlobalDate(e.target.value)}
              style={{
                background: 'var(--bg-secondary)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border-color)',
                padding: '6px 10px',
                borderRadius: '6px',
                fontSize: '13px',
                fontWeight: 600,
                colorScheme: 'dark'
              }}
            />
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: 600 }}>🗄️ Target DB:</span>
            <select
              id="global-db-selector"
              value={targetDb}
              onChange={(e) => setTargetDb(e.target.value)}
              style={{
                background: 'var(--bg-secondary)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border-color)',
                padding: '6px 10px',
                borderRadius: '6px',
                fontSize: '13px',
                fontWeight: 600
              }}
            >
              <option value="pg_prod">PostgreSQL PROD</option>
              <option value="pg_dev">PostgreSQL DEV</option>
              <option value="oracle_dev">Oracle DEV</option>
              <option value="oracle_f1">Oracle F1</option>
              <option value="oracle_prod">Oracle PROD</option>
            </select>
          </div>
          <span style={{
            fontSize: '11px', color: '#34d399', fontWeight: 700,
            background: 'rgba(52,211,153,0.1)', padding: '3px 8px', borderRadius: '4px'
          }}>
            ⚡ Live — applies to entire page
          </span>
        </div>
      </div>

      {/* ── Warehouse Level KPI Grid ── */}
      <div className="kpi-grid">
        {kpis.map((kpi, i) => (
          <KPICard key={kpi.title} {...kpi} index={i} />
        ))}
      </div>

      {/* ── Charts Grid ── */}
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
          <AiAnalyticsDahsboardDateParaemeter />
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
          <AiAnalyticsDahsboardDateParaemeter />
    </motion.div>
      </div>

      {/* ── Warehouse Sales & Invoice Analytics — receives global date & db ── */}
      <WarehouseSalesAnalytics globalDate={globalDate} globalTargetDb={targetDb} />

      {/* ── Warehouse Inventory Level Statistics ── */}
      <WarehouseAnalytics />

      {/* ── Inventory Risk Anomaly Forecast ── */}
      <div style={{ marginTop: '24px' }}>
        <InventoryRiskForecast />
      </div>
      <AiAnalyticsDahsboardDateParaemeter />
    </motion.div>
  )
}
