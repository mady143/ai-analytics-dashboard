import React from 'react';

export default function CopilotSearchFixes() {
  return (
    <div className="copilotsearchfixes-card card" style={{ marginTop: '20px' }}>
      <h3 style={{ fontSize: '18px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px' }}>
        ⚡ Copilot search fixes
      </h3>
      <div style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '16px' }}>
        <p className="editor-paragraph-block" style={{ margin: 0 }}>
          When entering any warehouse in copilot, show results without date restriction until a date is selected.
        </p>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
        <div style={{ background: 'var(--bg-card)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Metric / Status</div>
          <div style={{ fontSize: '20px', fontWeight: 700, color: 'var(--color-primary)' }}>Active</div>
        </div>
        <div style={{ background: 'var(--bg-card)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Execution Time</div>
          <div style={{ fontSize: '20px', fontWeight: 700, color: '#34d399' }}>&lt; 50 ms</div>
        </div>
        <div style={{ background: 'var(--bg-card)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Health Index</div>
          <div style={{ fontSize: '20px', fontWeight: 700, color: '#c084fc' }}>100%</div>
        </div>
      </div>
    </div>
  );
}
