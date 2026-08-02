import React from 'react'

export default function Footer() {
  return (
    <footer style={{
      marginTop: '40px',
      padding: '20px 24px',
      borderTop: '1px solid var(--border-subtle)',
      display: 'flex',
      justify: 'space-between',
      alignItems: 'center',
      flexWrap: 'wrap',
      gap: '12px',
      fontSize: '13px',
      color: 'var(--text-secondary)'
    }}>
      <div>
        © 2026 AI Analytics Dashboard. All rights reserved.
      </div>
      <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: 'var(--text-muted)' }}>
        <span>Powered by Agentic AI</span>
        <span>•</span>
        <span>Version 1.0.0</span>
      </div>
    </footer>
  )
}
