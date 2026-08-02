import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  CheckCircle2, Clock, PlayCircle, AlertCircle, RefreshCw,
  Search, Layers, Cpu, Server, CheckSquare, Zap, Filter
} from 'lucide-react'

const API_BASE = 'http://localhost:8000'

export default function SprintBoard() {
  const [sprintData, setSprintData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  
  // Priority Enable/Disable Toggles State
  const [enabledPriorities, setEnabledPriorities] = useState({
    URGENT: true,
    HIGH: true,
    MEDIUM: true,
    LOW: true,
    NONE: true
  })

  const togglePriority = (p) => {
    setEnabledPriorities(prev => ({
      ...prev,
      [p]: !prev[p]
    }))
  }

  const toggleAllPriorities = () => {
    const allOn = Object.values(enabledPriorities).every(v => v)
    setEnabledPriorities({
      URGENT: !allOn,
      HIGH: !allOn,
      MEDIUM: !allOn,
      LOW: !allOn,
      NONE: !allOn
    })
  }

  const fetchSprintTasks = async () => {
    try {
      setLoading(true)
      const res = await fetch(`${API_BASE}/api/sprints/tasks`)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setSprintData(data)
      setError(null)
    } catch (err) {
      console.error('Failed to fetch live sprint tasks:', err)
      setError('Could not connect to live Sprint Watcher agent. Displaying cached sprint state.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSprintTasks()
    const interval = setInterval(fetchSprintTasks, 10000)
    return () => clearInterval(interval)
  }, [])

  const priorityColors = {
    urgent: { bg: 'rgba(239, 68, 68, 0.15)', text: '#ef4444', border: 'rgba(239, 68, 68, 0.4)' },
    high: { bg: 'rgba(245, 158, 11, 0.15)', text: '#f59e0b', border: 'rgba(245, 158, 11, 0.4)' },
    medium: { bg: 'rgba(59, 130, 246, 0.15)', text: '#3b82f6', border: 'rgba(59, 130, 246, 0.4)' },
    low: { bg: 'rgba(107, 114, 128, 0.15)', text: '#9ca3af', border: 'rgba(107, 114, 128, 0.4)' }
  }

  const allTasks = sprintData?.tasks?.all || []
  const filteredTasks = allTasks.filter(task => {
    const matchesSearch = task.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          (task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase()))
    const pKey = (task.priority || 'MEDIUM').toUpperCase()
    const isPriorityEnabled = enabledPriorities[pKey] !== false
    return matchesSearch && isPriorityEnabled
  })

  const todoTasks = filteredTasks.filter(t => t.status === 'unstarted' || t.status === 'backlog' || t.status === 'todo')
  const inProgressTasks = filteredTasks.filter(t => t.status === 'started' || t.status === 'in_progress')
  const completedTasks = filteredTasks.filter(t => t.status === 'completed' || t.status === 'done')

  const sprintInfo = sprintData?.sprint || {
    name: 'Sprint AAD-5 · Real-Time Warehouse Analytics',
    total_tasks: allTasks.length,
    completed_tasks: completedTasks.length,
    in_progress_tasks: inProgressTasks.length,
    todo_tasks: todoTasks.length,
    completion_percentage: allTasks.length > 0 ? ((completedTasks.length / allTasks.length) * 100).toFixed(1) : 100
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto' }}
    >
      {/* ── Sprint Header Banner ── */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(124,58,237,0.12) 0%, rgba(6,182,212,0.12) 100%)',
        border: '1px solid rgba(124,58,237,0.3)',
        borderRadius: '16px',
        padding: '24px',
        marginBottom: '24px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.2)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{
                background: 'linear-gradient(135deg, #7C3AED, #06B6D4)',
                color: '#fff', fontSize: '11px', fontWeight: 800,
                padding: '4px 10px', borderRadius: '20px', textTransform: 'uppercase', letterSpacing: '0.5px'
              }}>
                Plane Active Sprint
              </span>
              <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                🤖 Synchronized via Sprint Watcher Agent
              </span>
            </div>
            <h1 style={{ fontSize: '24px', fontWeight: 800, color: 'var(--text-primary)', marginTop: '8px', marginBottom: '4px' }}>
              {sprintInfo.name}
            </h1>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
              Real-time monitoring of tasks read directly from Plane project by AI agents
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <button
              onClick={fetchSprintTasks}
              disabled={loading}
              style={{
                background: 'var(--bg-secondary)', border: '1px solid var(--border-color)',
                color: 'var(--text-primary)', padding: '8px 16px', borderRadius: '8px',
                fontSize: '13px', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px'
              }}
            >
              <RefreshCw size={14} className={loading ? 'spin' : ''} />
              Refresh Plane
            </button>
          </div>
        </div>

        {/* Sprint Progress Bar */}
        <div style={{ marginTop: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', fontWeight: 700, marginBottom: '6px' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Sprint Completion Progress</span>
            <span style={{ color: '#34d399' }}>{sprintInfo.completion_percentage}% ({completedTasks.length}/{allTasks.length} Tasks)</span>
          </div>
          <div style={{ height: '8px', background: 'rgba(255,255,255,0.08)', borderRadius: '4px', overflow: 'hidden' }}>
            <div style={{
              width: `${sprintInfo.completion_percentage}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #7C3AED 0%, #34D399 100%)',
              borderRadius: '4px',
              transition: 'width 0.6s ease'
            }} />
          </div>
        </div>
      </div>

      {/* ── Search & Enable/Disable Priority Toggles ── */}
      <div style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        flexWrap: 'wrap', gap: '16px', marginBottom: '24px',
        background: 'var(--bg-card)', border: '1px solid var(--border-color)',
        borderRadius: '12px', padding: '12px 18px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flex: '1', minWidth: '240px' }}>
          <Search size={16} style={{ color: 'var(--text-secondary)' }} />
          <input
            type="text"
            placeholder="Filter sprint tasks by title or keyword..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              background: 'transparent', border: 'none', color: 'var(--text-primary)',
              fontSize: '13px', width: '100%', outline: 'none'
            }}
          />
        </div>

        {/* Enable/Disable Priority Toggle Buttons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Filter size={14} /> Priority Toggles:
          </span>
          
          <button
            id="toggle-all-priorities-btn"
            onClick={toggleAllPriorities}
            style={{
              background: 'rgba(124, 58, 237, 0.2)',
              color: '#a78bfa',
              border: '1px solid #7C3AED',
              padding: '4px 10px', borderRadius: '6px', fontSize: '11px', fontWeight: 700, cursor: 'pointer'
            }}
          >
            {Object.values(enabledPriorities).every(v => v) ? 'Disable All' : 'Enable All'}
          </button>

          {['URGENT', 'HIGH', 'MEDIUM', 'LOW'].map(p => {
            const isEnabled = enabledPriorities[p]
            const colors = priorityColors[p.toLowerCase()] || priorityColors.medium
            return (
              <button
                key={p}
                id={`priority-toggle-${p.toLowerCase()}`}
                onClick={() => togglePriority(p)}
                title={`Click to ${isEnabled ? 'Disable' : 'Enable'} ${p} priority tasks`}
                style={{
                  background: isEnabled ? colors.bg : 'var(--bg-secondary)',
                  color: isEnabled ? colors.text : 'var(--text-muted)',
                  border: `1px solid ${isEnabled ? colors.border : 'var(--border-color)'}`,
                  padding: '4px 10px',
                  borderRadius: '6px',
                  fontSize: '11px',
                  fontWeight: 700,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  opacity: isEnabled ? 1 : 0.45,
                  textDecoration: isEnabled ? 'none' : 'line-through',
                  transition: 'all 0.2s ease'
                }}
              >
                <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: isEnabled ? colors.text : 'var(--text-muted)' }} />
                {p} {isEnabled ? '✓' : 'OFF'}
              </button>
            )
          })}
        </div>
      </div>

      {/* ── Kanban Columns ── */}
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '20px'
      }}>
        {/* Column 1: TODO / Backlog */}
        <KanbanColumn
          title="To Do / Backlog"
          count={todoTasks.length}
          color="#3b82f6"
          icon={<Clock size={16} />}
          tasks={todoTasks}
          priorityColors={priorityColors}
        />

        {/* Column 2: In Progress */}
        <KanbanColumn
          title="In Progress"
          count={inProgressTasks.length}
          color="#f59e0b"
          icon={<PlayCircle size={16} />}
          tasks={inProgressTasks}
          priorityColors={priorityColors}
          badgeText="Active Agent Working"
        />

        {/* Column 3: Completed */}
        <KanbanColumn
          title="Completed"
          count={completedTasks.length}
          color="#10b981"
          icon={<CheckCircle2 size={16} />}
          tasks={completedTasks}
          priorityColors={priorityColors}
          badgeText="Verified & Merged"
        />
      </div>
    </motion.div>
  )
}

function KanbanColumn({ title, count, color, icon, tasks, priorityColors, badgeText }) {
  return (
    <div style={{
      background: 'var(--bg-card)', border: '1px solid var(--border-color)',
      borderRadius: '12px', padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color)', paddingBottom: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ color }}>{icon}</span>
          <h2 style={{ fontSize: '15px', fontWeight: 700, color: 'var(--text-primary)' }}>{title}</h2>
        </div>
        <span style={{
          background: 'var(--bg-secondary)', border: `1px solid ${color}`,
          color, fontSize: '12px', fontWeight: 800, padding: '2px 8px', borderRadius: '12px'
        }}>
          {count}
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', minHeight: '200px' }}>
        {tasks.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '32px 16px', color: 'var(--text-secondary)', fontSize: '13px', fontStyle: 'italic' }}>
            No tasks in this column
          </div>
        ) : (
          tasks.map(task => {
            const pStyle = priorityColors[task.priority?.toLowerCase()] || priorityColors.medium
            return (
              <motion.div
                key={task.id}
                layout
                initial={{ opacity: 0, scale: 0.96 }}
                animate={{ opacity: 1, scale: 1 }}
                style={{
                  background: 'var(--bg-secondary)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  padding: '14px',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '8px', marginBottom: '8px' }}>
                  <span style={{
                    background: pStyle.bg, color: pStyle.text, border: `1px solid ${pStyle.border}`,
                    fontSize: '10px', fontWeight: 800, padding: '2px 6px', borderRadius: '4px', textTransform: 'uppercase'
                  }}>
                    {task.priority || 'MEDIUM'}
                  </span>
                  <span style={{ fontSize: '11px', color: 'var(--text-secondary)', fontWeight: 600 }}>
                    {task.points || 3} pts
                  </span>
                </div>

                <div style={{ fontSize: '14px', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '6px' }}>
                  {task.name}
                </div>

                {task.description && (
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)', lineClamp: 2, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {task.description}
                  </div>
                )}

                {badgeText && (
                  <div style={{ marginTop: '10px', paddingTop: '8px', borderTop: '1px solid rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Zap size={12} style={{ color }} />
                    <span style={{ fontSize: '11px', color, fontWeight: 700 }}>{badgeText}</span>
                  </div>
                )}
              </motion.div>
            )
          })
        )}
      </div>
    </div>
  )
}
