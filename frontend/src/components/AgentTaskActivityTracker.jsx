import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bot, CheckCircle2, Clock, Terminal, AlertTriangle, RefreshCw, Cpu, Activity } from 'lucide-react';

const API = import.meta.env.VITE_API_URL || '';

export default function AgentTaskActivityTracker() {
  const [agents, setAgents] = useState({});
  const [recentActivity, setRecentActivity] = useState([]);
  const [activeTask, setActiveTask] = useState(null);
  const [lastActive, setLastActive] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchTaskStatus = async () => {
    try {
      const res = await axios.get(`${API}/api/agents/status`);
      if (res.data) {
        setAgents(res.data.agents || {});
        setLastActive(res.data.last_active || '');
        if (res.data.recent_activity) {
          setRecentActivity(res.data.recent_activity);
        }
        if (res.data.active_task) {
          setActiveTask(res.data.active_task);
        }
      }
    } catch (err) {
      console.error('[AgentTaskActivityTracker] Failed to fetch agent status:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTaskStatus();
    const interval = setInterval(fetchTaskStatus, 4000);
    return () => clearInterval(interval);
  }, []);

  // Find if any agent is currently actively working on a task
  const workingAgent = Object.entries(agents).find(([_, info]) => {
    const task = info.current_task || '';
    return task.includes('🔨') || task.includes('🧪') || task.includes('Picked up') || task.includes('Implementing') || task.includes('Building');
  });

  return (
    <div className="card" id="agent-task-activity-tracker" style={{ marginTop: '24px', padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: 700, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Bot size={20} color="#7C3AED" />
            Autonomous Agent Task Pickup &amp; Execution Stream
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginTop: '4px' }}>
            Real-time monitoring of tasks picked up from Sprint/Plane, active agent execution steps, and automated test results.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{
            fontSize: '11px', fontWeight: 700, padding: '4px 10px', borderRadius: '6px',
            background: workingAgent ? 'rgba(124, 58, 237, 0.2)' : 'rgba(52, 211, 153, 0.1)',
            color: workingAgent ? '#c4b5fd' : '#34d399',
            border: workingAgent ? '1px solid rgba(124, 58, 237, 0.5)' : '1px solid rgba(52, 211, 153, 0.2)',
            display: 'flex', alignItems: 'center', gap: '6px'
          }}>
            <Activity size={12} className={workingAgent ? 'animate-spin' : ''} />
            {workingAgent ? `ACTIVE: ${workingAgent[0].toUpperCase()} WORKING` : 'ALL AGENTS IDLE & MONITORING SPRINT'}
          </span>
          <button
            onClick={fetchTaskStatus}
            style={{
              background: 'var(--bg-secondary)', border: '1px solid var(--border-color)',
              color: 'var(--text-secondary)', padding: '4px 10px', borderRadius: '6px',
              fontSize: '12px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px'
            }}
          >
            <RefreshCw size={12} />
            Refresh
          </button>
        </div>
      </div>

      {/* Active Task Banner */}
      {workingAgent && (
        <div style={{
          background: 'linear-gradient(135deg, rgba(124, 58, 237, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%)',
          border: '1px solid rgba(124, 58, 237, 0.4)',
          borderRadius: '10px',
          padding: '16px 20px',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '12px'
        }}>
          <div>
            <div style={{ fontSize: '11px', textTransform: 'uppercase', tracking: '1px', color: '#a78bfa', fontWeight: 700, marginBottom: '4px' }}>
              ⚡ CURRENTLY EXECUTING TASK
            </div>
            <div style={{ fontSize: '16px', fontWeight: 700, color: '#ffffff' }}>
              {workingAgent[1].current_task}
            </div>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Assigned Agent: <strong style={{ color: '#06b6d4', textTransform: 'capitalize' }}>{workingAgent[0]}</strong> · Status: <span style={{ color: '#34d399', fontWeight: 600 }}>{workingAgent[1].status.toUpperCase()}</span>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '8px' }}>
            <span style={{ fontSize: '11px', background: 'rgba(255,255,255,0.08)', padding: '6px 12px', borderRadius: '6px', color: '#e5e7eb' }}>
              Phase: <strong>Implementation &amp; Testing</strong>
            </span>
          </div>
        </div>
      )}

      {/* Agent Activity Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px', marginBottom: '20px' }}>
        {Object.entries(agents).map(([agentName, info]) => {
          const isBusy = (info.current_task || '').includes('🔨') || (info.current_task || '').includes('🧪') || (info.current_task || '').includes('Picked up');
          return (
            <div key={agentName} style={{
              background: 'var(--bg-secondary)',
              border: isBusy ? '1px solid rgba(124, 58, 237, 0.5)' : '1px solid var(--border-color)',
              borderRadius: '8px',
              padding: '12px 14px',
              transition: 'all 0.2s ease'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--text-primary)', textTransform: 'capitalize' }}>
                  {agentName.replace('_', ' ')}
                </span>
                <span style={{
                  fontSize: '10px', fontWeight: 700, padding: '2px 6px', borderRadius: '4px',
                  background: isBusy ? 'rgba(124, 58, 237, 0.25)' : 'rgba(52, 211, 153, 0.1)',
                  color: isBusy ? '#c4b5fd' : '#34d399'
                }}>
                  {isBusy ? 'BUSY ⚡' : info.status.toUpperCase()}
                </span>
              </div>
              <div style={{ fontSize: '11px', color: 'var(--text-secondary)', lineHeight: '1.4', wordBreak: 'break-word' }}>
                {info.current_task || 'Idle / Listening for tasks'}
              </div>
            </div>
          );
        })}
      </div>

      {/* Recent Sprint Task Pickup Stream */}
      <div>
        <h3 style={{ fontSize: '14px', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Clock size={16} color="#06B6D4" />
          Recent Sprint Task Executions &amp; Log Stream
        </h3>

        {recentActivity.length === 0 ? (
          <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-secondary)', fontSize: '13px', background: 'var(--bg-secondary)', borderRadius: '8px', border: '1px dashed var(--border-color)' }}>
            No recent task execution logs recorded yet. Sprint Watcher polls Plane every 60s for new/updated tasks.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '240px', overflowY: 'auto' }}>
            {recentActivity.map((rec, i) => (
              <div key={i} style={{
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-color)',
                borderRadius: '6px',
                padding: '10px 14px',
                fontSize: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                gap: '12px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  {rec.status === 'completed' ? (
                    <CheckCircle2 size={16} color="#34d399" />
                  ) : (
                    <AlertTriangle size={16} color="#ef4444" />
                  )}
                  <div>
                    <div style={{ fontWeight: 700, color: 'var(--text-primary)' }}>
                      #{rec.task_id} — {rec.task_title}
                    </div>
                    <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                      Processed by <span style={{ color: '#a78bfa', textTransform: 'capitalize' }}>{rec.agent}</span> · {new Date(rec.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{
                    fontSize: '10px', fontWeight: 700, padding: '2px 8px', borderRadius: '4px',
                    background: rec.status === 'completed' ? 'rgba(52, 211, 153, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                    color: rec.status === 'completed' ? '#34d399' : '#fca5a5'
                  }}>
                    {rec.status.toUpperCase()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
