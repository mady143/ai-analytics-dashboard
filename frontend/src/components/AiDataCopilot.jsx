import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Sparkles, Send, Bot, Zap, Search, CheckCircle, Filter } from 'lucide-react';

const API = import.meta.env.VITE_API_URL || '';

export default function AiDataCopilot({ globalDate, globalTargetDb = 'pg_dev', onApplyFilter }) {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [copilotResult, setCopilotResult] = useState(null);

  const quickPills = [
    "Warehouse 58 Overview",
    "High Scratch Quantity",
    "Pending Procurement Transfers",
    "Whse 61 Cases Built"
  ];

  // Automatically refresh AI response when global date or target DB changes
  useEffect(() => {
    if (prompt && copilotResult) {
      handleQuery(prompt);
    }
  }, [globalDate, globalTargetDb]);

  const handleQuery = async (queryText) => {
    const q = queryText || prompt;
    if (!q.trim()) return;

    setLoading(true);
    try {
      const oerdte = globalDate ? globalDate.replace(/-/g, '') : '';
      const res = await axios.post(`${API}/api/analytics/ai-copilot`, {
        prompt: q,
        target_db: globalTargetDb,
        oerdte: oerdte
      });
      setCopilotResult(res.data);
    } catch (err) {
      console.error('[AiDataCopilot] Query error:', err);
    } finally {
      setLoading(false);
    }
  };

  const [filterApplied, setFilterApplied] = useState(false);

  const handleApplyFilter = () => {
    if (!copilotResult) return;
    setFilterApplied(true);
    setTimeout(() => setFilterApplied(false), 2500);
    if (onApplyFilter) {
      onApplyFilter({
        whse: copilotResult.filtered_whse || '',
        batch: copilotResult.filtered_batch || '',
        invoice: copilotResult.filtered_invoice || ''
      });
    }
  };

  const hasFilterDirectives = copilotResult && (
    Boolean(copilotResult.filtered_whse) ||
    Boolean(copilotResult.filtered_batch) ||
    Boolean(copilotResult.filtered_invoice)
  );

  return (
    <div className="card" style={{ marginTop: '20px', padding: '20px', background: 'linear-gradient(135deg, rgba(30,27,75,0.6) 0%, rgba(15,23,42,0.8) 100%)', border: '1px solid rgba(124,58,237,0.3)' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px', flexWrap: 'wrap', gap: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{ background: 'rgba(124,58,237,0.2)', padding: '8px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Sparkles size={20} color="#c084fc" />
          </div>
          <div>
            <h3 style={{ fontSize: '17px', fontWeight: 700, color: 'var(--text-primary)', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
              AI Data Copilot
            </h3>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0, marginTop: '2px' }}>
              Ask natural language questions to query warehouse records and filter analytics in real time
            </p>
          </div>
        </div>

        <span style={{ fontSize: '11px', background: 'rgba(52,211,153,0.1)', color: '#34d399', border: '1px solid rgba(52,211,153,0.2)', padding: '4px 10px', borderRadius: '20px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '5px' }}>
          <Zap size={12} /> Active Agent Engine
        </span>
      </div>

      {/* Quick Prompt Pills */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px', flexWrap: 'wrap' }}>
        <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 600 }}>Quick Insights:</span>
        {quickPills.map((pill) => (
          <button
            key={pill}
            type="button"
            onClick={() => {
              setPrompt(pill);
              handleQuery(pill);
            }}
            style={{
              background: 'var(--bg-secondary)',
              color: 'var(--text-secondary)',
              border: '1px solid var(--border-color)',
              padding: '4px 10px',
              borderRadius: '16px',
              fontSize: '12px',
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
            onMouseOver={(e) => { e.currentTarget.style.borderColor = '#7C3AED'; e.currentTarget.style.color = '#FFFFFF'; }}
            onMouseOut={(e) => { e.currentTarget.style.borderColor = 'var(--border-color)'; e.currentTarget.style.color = 'var(--text-secondary)'; }}
          >
            {pill}
          </button>
        ))}
      </div>

      {/* Search Input Bar */}
      <form onSubmit={(e) => { e.preventDefault(); handleQuery(); }} style={{ display: 'flex', gap: '10px' }}>
        <div style={{ position: 'relative', flex: 1 }}>
          <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
          <input
            type="text"
            placeholder="Ask AI Data Copilot (e.g., 'Show Warehouse 58 high scratch cases')..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            style={{
              width: '100%',
              background: 'var(--bg-primary)',
              color: 'var(--text-primary)',
              border: '1px solid var(--border-color)',
              padding: '10px 12px 10px 38px',
              borderRadius: '8px',
              fontSize: '13px',
              fontWeight: 500
            }}
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          style={{
            background: 'linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%)',
            color: '#FFFFFF',
            border: 'none',
            padding: '0 20px',
            borderRadius: '8px',
            fontSize: '13px',
            fontWeight: 700,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            boxShadow: '0 2px 6px rgba(124,58,237,0.4)'
          }}
        >
          {loading ? 'Analyzing...' : <><Send size={14} /> Ask AI</>}
        </button>
      </form>

      {/* Copilot Result Insight Card */}
      {copilotResult && (
        <div style={{ marginTop: '16px', padding: '14px 16px', background: 'var(--bg-primary)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', fontWeight: 700, color: '#c084fc' }}>
              <Bot size={16} /> AI Copilot Finding
            </div>
            {hasFilterDirectives && (
              <button
                type="button"
                id="copilot-apply-filter-btn"
                onClick={handleApplyFilter}
                style={{
                  background: filterApplied ? 'rgba(52,211,153,0.3)' : 'rgba(52,211,153,0.15)',
                  color: filterApplied ? '#ffffff' : '#34d399',
                  border: '1px solid rgba(52,211,153,0.5)',
                  padding: '4px 12px',
                  borderRadius: '6px',
                  fontSize: '12px',
                  fontWeight: 700,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px',
                  transition: 'all 0.2s ease'
                }}
              >
                {filterApplied ? <CheckCircle size={14} /> : <Filter size={12} />}
                {filterApplied ? 'Filter Applied to Table ✓' : 'Apply Filter to Table'}
              </button>
            )}
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '13px', lineHeight: 1.5, margin: 0 }}>
            {copilotResult.summary_answer}
          </p>

          {copilotResult.suggested_actions && (
            <div style={{ display: 'flex', gap: '8px', marginTop: '10px', flexWrap: 'wrap' }}>
              {copilotResult.suggested_actions.map((act) => (
                <span key={act} style={{ fontSize: '11px', background: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)', padding: '2px 8px', borderRadius: '4px' }}>
                  ✓ {act}
                </span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
