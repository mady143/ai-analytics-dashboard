import React from 'react';

export default function AiAnalyticsDashboardAddingDateParameter() {
  return (
    <div className="aianalyticsdashboardaddingdateparameter-card card" style={{ marginTop: '20px' }}>
      <h3 style={{ fontSize: '18px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px' }}>
        ⚡ AI Analytics Dashboard Adding Date Parameter
      </h3>
      <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '16px' }}>
        <p class="editor-paragraph-block" data-spacing-group="body" data-id="d78e9c29-698d-4531-883c-df31b9c02c11">Add from date and to date and populate the date accordingly </p>
      </p>
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
