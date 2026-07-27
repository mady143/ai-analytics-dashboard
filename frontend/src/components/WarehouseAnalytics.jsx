import React from 'react';

export default function WarehouseAnalytics() {
  return (
    <div className="warehouse-card card" style={{ marginTop: '20px' }}>
      <h3 style={{ fontSize: '18px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px' }}>
        🏢 Warehouse Level Statistics & Metrics
      </h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
        <div style={{ background: 'var(--bg-card)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Total Storage Utilized</div>
          <div style={{ fontSize: '20px', fontWeight: 700, color: 'var(--color-primary)' }}>84.2%</div>
        </div>
        <div style={{ background: 'var(--bg-card)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Active Units Streamed</div>
          <div style={{ fontSize: '20px', fontWeight: 700, color: '#34d399' }}>12,450</div>
        </div>
        <div style={{ background: 'var(--bg-card)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Processing Latency</div>
          <div style={{ fontSize: '20px', fontWeight: 700, color: '#c084fc' }}>18 ms</div>
        </div>
      </div>
    </div>
  );
}
