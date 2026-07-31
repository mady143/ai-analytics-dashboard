import CopilotSearchFixes from '../components/CopilotSearchFixes';
import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import KPICard from '../components/KPICard'
import WarehouseSalesAnalytics from '../components/WarehouseSalesAnalytics'
import WarehouseAnalytics from '../components/WarehouseAnalytics'
import AiDataCopilot from '../components/AiDataCopilot'
import AnomalyAlertPanel from '../components/AnomalyAlertPanel'
import AgentTaskActivityTracker from '../components/AgentTaskActivityTracker'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  ScatterChart, Scatter, Cell
} from 'recharts'

const API = import.meta.env.VITE_API_URL || ''

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
  { title: "TOTAL WAREHOUSES", value: "...", unit: "Facilities", trend: 0.0, trend_direction: "up", color: "#7C3AED" },
  { title: "CASES BUILT (cases_bld)", value: "...", unit: "Cases", trend: 8.4, trend_direction: "up", color: "#06B6D4" },
  { title: "ORIGINAL ORDER QTY", value: "...", unit: "Cases", trend: 6.2, trend_direction: "up", color: "#F59E0B" },
  { title: "INVOICES PROCESSED", value: "...", unit: "Invoices", trend: 4.1, trend_direction: "up", color: "#10B981" },
  { title: "FULFILLMENT RATE", value: "...", unit: "Target 95%", trend: 2.1, trend_direction: "up", color: "#34D399" },
  { title: "SCRATCH RATE", value: "...", unit: "...", trend: -1.5, trend_direction: "down", color: "#EF4444" }
]

export default function Dashboard() {
  // ── Form Input State ──────────
  const [selectedDate, setSelectedDate] = useState(todayISO())
  const [selectedDb, setSelectedDb] = useState('pg_dev')

  // ── Applied State (submitted) ──
  const [appliedDate, setAppliedDate] = useState(todayISO())
  const [appliedTargetDb, setAppliedTargetDb] = useState('pg_dev')

  // ── Table Filter Synchronization State ──
  const [tableFilters, setTableFilters] = useState(null)
  // Tracks whether the Copilot has pushed an ACTIVE filter to the page
  // (distinct from any random tableFilters change — only true when Copilot fired onApplyFilter)
  const [copilotFilterActive, setCopilotFilterActive] = useState(false)

  const handleApplyTableFilter = (filters) => {
    const nextFilters = { ...(tableFilters || {}), ...filters, _ts: Date.now() };
    setTableFilters(nextFilters);
    setCopilotFilterActive(true);

    const targetWhse = nextFilters.whse || nextFilters.oewhse || nextFilters.whs_num || nextFilters.filtered_whse || '';
    fetchAll(appliedDate, appliedTargetDb, targetWhse, true);
  }

  const [kpis, setKpis] = useState(DEFAULT_KPIS)
  const [barData, setBarData] = useState([])
  const [scatterData, setScatterData] = useState([])

  const fetchAll = (dateVal, dbVal, whseVal = '', forceCopilot = false) => {
    // ✅ Rule (TASK 19 & TASK 24):
    // - When Copilot filter is EXPLICITLY active → bypass date (oerdte='') so full dataset is shown
    // - When using normal date picker → always send the selected date so all widgets are date-filtered
    // - Both modes must populate KPI, Bar Chart, Scatter, and Table correctly
    const isCopilot = forceCopilot || copilotFilterActive;
    const effectiveDateVal = isCopilot ? '' : dateVal;
    const oerdte = effectiveDateVal ? toOerdte(effectiveDateVal) : '';
    const whseParam = whseVal ? `&oewhse=${whseVal}` : '';

    axios.get(`/api/charts/kpi?oerdte=${oerdte}&target_db=${dbVal}${whseParam}`)
      .then(res => {
        if (res.data?.kpis) setKpis(res.data.kpis)
      })
      .catch(err => console.error('Failed to fetch KPI cards:', err))

    axios.get(`/api/charts/bar?oerdte=${oerdte}&target_db=${dbVal}${whseParam}`)
      .then(res => {
        if (res.data?.data) setBarData(res.data.data)
      })
      .catch(err => console.error('Failed to fetch Bar chart data:', err))

    axios.get(`/api/charts/scatter?oerdte=${oerdte}&target_db=${dbVal}${whseParam}`)
      .then(res => {
        if (res.data?.data) setScatterData(res.data.data)
      })
      .catch(err => console.error('Failed to fetch Scatter plot data:', err))
  }

  // Initial fetch and on submission or filter change
  useEffect(() => {
    const activeWhse = tableFilters?.whse || tableFilters?.oewhse || tableFilters?.whs_num || tableFilters?.filtered_whse || '';
    fetchAll(appliedDate, appliedTargetDb, activeWhse)
    const timer = setInterval(() => fetchAll(appliedDate, appliedTargetDb, activeWhse), 15000)
    return () => clearInterval(timer)
  }, [appliedDate, appliedTargetDb, tableFilters, copilotFilterActive])


  const handleSubmit = (e) => {
    if (e) e.preventDefault()
    // When user manually submits date — deactivate Copilot filter so date is respected
    setCopilotFilterActive(false)
    setTableFilters(null)
    setAppliedDate(selectedDate)
    setAppliedTargetDb(selectedDb)
    fetchAll(selectedDate, selectedDb)
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* ── Global Date & DB Selector Header ── */}
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 className="page-title">Warehouse Sales &amp; Invoice Analytics Dashboard</h1>
          <p className="page-subtitle">Sprint AAD-5 · Real-time Warehouse Item &amp; Procurement Analytics</p>
        </div>

        {/* Global Date + DB Controls + Submit Button */}
        <form onSubmit={handleSubmit} style={{
          display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap',
          background: 'var(--bg-card)', border: '1px solid var(--border-color)',
          borderRadius: '10px', padding: '10px 16px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: 600 }}>Order Date (Global):</span>
            <input
              id="global-date-picker"
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
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
            <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: 600 }}>Target DB:</span>
            <select
              id="global-db-selector"
              value={selectedDb}
              onChange={(e) => setSelectedDb(e.target.value)}
              style={{
                background: 'var(--bg-secondary)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border-color)',
                padding: '6px 10px',
                borderRadius: '6px',
                fontSize: '13px',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              <option value="pg_dev">PostgreSQL DEV</option>
              <option value="oracle_dev">Oracle DEV</option>
              <option value="oracle_f1">Oracle F1</option>
            </select>
          </div>

          <button
            type="submit"
            id="submit-db-btn"
            onClick={handleSubmit}
            style={{
              background: 'linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%)',
              color: '#FFFFFF',
              border: 'none',
              padding: '7px 18px',
              borderRadius: '6px',
              fontSize: '13px',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'all 0.2s ease',
              boxShadow: '0 2px 6px rgba(124, 58, 237, 0.4)'
            }}
          >
            Submit
          </button>

          <span style={{
            fontSize: '11px', color: '#34d399', fontWeight: 700,
            background: 'rgba(52,211,153,0.1)', padding: '3px 8px', borderRadius: '4px'
          }}>
            Active: {appliedTargetDb.toUpperCase()}
          </span>
        </form>
      </div>

      {/* ── AI Data Copilot Feature ── */}
      <AiDataCopilot
        globalDate={appliedDate}
        globalTargetDb={appliedTargetDb}
        onApplyFilter={handleApplyTableFilter}
        onClearFilter={() => {
          setCopilotFilterActive(false)
          setTableFilters(null)
        }}
        copilotFilterActive={copilotFilterActive}
      />

      {/* ── Real-Time Anomaly & Risk Alerts Feature ── */}
      <AnomalyAlertPanel
        globalDate={copilotFilterActive ? '' : appliedDate}
        globalTargetDb={appliedTargetDb}
        selectedWhse={tableFilters?.whse || tableFilters?.whs_num || ''}
        onApplyFilter={handleApplyTableFilter}
      />

      {/* ── Warehouse Level KPI Grid ── */}
      <div className="kpi-grid" style={{ marginTop: '24px' }}>
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
          <div className="chart-title">Cases Built by Warehouse</div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={barData} margin={{ top: 5, right: 10, bottom: 5, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="label" interval={0} tick={{ fill: '#8B949E', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#8B949E', fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(124,58,237,0.08)' }} />
              <Bar dataKey="value" name="Cases Built Qty" radius={[6, 6, 0, 0]}>
                {barData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <CopilotSearchFixes />
    </motion.div>

        {/* Scatter Chart */}
        <motion.div
          className="chart-card"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
        >
          <div className="chart-title">Original Order Qty vs Cases Built</div>
          <ResponsiveContainer width="100%" height={280}>
            <ScatterChart margin={{ top: 5, right: 10, bottom: 5, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis type="number" dataKey="x" name="Order Qty" tick={{ fill: '#8B949E', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis type="number" dataKey="y" name="Cases Built" tick={{ fill: '#8B949E', fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} content={<CustomTooltip />} />
              <Scatter name="Order vs Built" data={scatterData} fill="#06B6D4" opacity={0.8} />
            </ScatterChart>
          </ResponsiveContainer>
          <CopilotSearchFixes />
    </motion.div>
      </div>

      {/* ── Autonomous Agent Task Pickup & Execution Stream ── */}
      <AgentTaskActivityTracker />

      {/* ── Warehouse Sales & Invoice Analytics — receives global date, db & external filters ── */}
      <WarehouseSalesAnalytics
        globalDate={appliedDate}
        globalTargetDb={appliedTargetDb}
        externalFilters={tableFilters}
        copilotFilterActive={copilotFilterActive}
      />

      {/* ── Warehouse Inventory Level Statistics ── */}
      <WarehouseAnalytics />
      <CopilotSearchFixes />
    </motion.div>
  )
}


