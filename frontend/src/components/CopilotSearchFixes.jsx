import React from 'react';

export default function CopilotSearchFixes() {
  return (
    <div className="copilotsearchfixes-card card" style={{ marginTop: '20px' }}>
      <h3 style={{ fontSize: '18px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px' }}>
        ⚡ Copilot search fixes
      </h3>
      <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '16px' }}>
        <image-component data-id="54a11db9-3ce0-452c-8308-c1072a83e485" src="72603a5e-ca59-4ebb-a53e-b42ff34b6ce0" id="54a11db9-3ce0-452c-8308-c1072a83e485" width="299px" height="90px" aspectratio="3.324963072378139" alignment="left" status="uploaded" data-spacing-group="container"></image-component><p class="editor-paragraph-block" data-spacing-group="body" data-id="03c13c7a-80c0-438e-aca0-1ed10cd648f3">when i entering any wharehouse to show the results in copilot then donot considered the date paramenetrs and show the results and as well when clik on apply filters as well untill date is selected individuall;y </p>
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
