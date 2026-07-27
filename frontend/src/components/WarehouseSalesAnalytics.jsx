import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function WarehouseSalesAnalytics({ globalDate, globalTargetDb }) {
  const [targetDb, setTargetDb] = useState(globalTargetDb || 'pg_prod');
  const [summary, setSummary] = useState(null);
  const [items, setItems] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const LIMIT = 20;

  useEffect(() => {
    if (globalTargetDb) {
      setTargetDb(globalTargetDb);
    }
  }, [globalTargetDb]);

  const oerdte = globalDate ? globalDate.replace(/-/g, '') : '';

  // Reset & initial load on DB target or date change
  useEffect(() => {
    const fetchInitial = async () => {
      setLoading(true);
      try {
        const res = await axios.get(`${API}/api/warehouse/statistics?target_db=${targetDb}&oerdte=${oerdte}&limit=${LIMIT}&offset=0`);
        setSummary(res.data.summary);
        setItems(res.data.warehouse_items || []);
        setTotalCount(res.data.total_count || (res.data.warehouse_items ? res.data.warehouse_items.length : 0));
        setHasMore(res.data.has_more ?? false);
      } catch (err) {
        console.error('Failed to fetch warehouse statistics:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchInitial();
  }, [targetDb, oerdte]);

  // Load next batch on scroll down
  const loadMoreData = async () => {
    if (loadingMore || !hasMore) return;
    setLoadingMore(true);
    const nextOffset = items.length;
    try {
      const res = await axios.get(`${API}/api/warehouse/statistics?target_db=${targetDb}&oerdte=${oerdte}&limit=${LIMIT}&offset=${nextOffset}`);
      setItems((prev) => [...prev, ...(res.data.warehouse_items || [])]);
      setHasMore(res.data.has_more ?? false);
    } catch (err) {
      console.error('Failed to fetch next batch of warehouse data:', err);
    } finally {
      setLoadingMore(false);
    }
  };

  const handleScroll = (e) => {
    const { scrollTop, scrollHeight, clientHeight } = e.target;
    if (scrollHeight - scrollTop - clientHeight < 50) {
      loadMoreData();
    }
  };

  return (
    <div className="card" style={{ marginTop: '24px', padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 700, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            🏢 Warehouse & Invoice Sales Analytics
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginTop: '4px' }}>
            Identifies sales information for warehouse item level and invoice level transfer to Procurement systems.
          </p>
        </div>

        {/* Database Configuration Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <label style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: 600 }}>Target DB:</label>
          <select
            value={targetDb}
            onChange={(e) => setTargetDb(e.target.value)}
            style={{
              background: 'var(--bg-card)',
              color: 'var(--text-primary)',
              border: '1px solid var(--border-color)',
              padding: '6px 12px',
              borderRadius: '6px',
              fontSize: '13px',
              fontWeight: 600
            }}
          >
            <option value="pg_prod">PostgreSQL - PROD (sptnintgdb)</option>
            <option value="pg_dev">PostgreSQL - DEV (sptnintgdb)</option>
            <option value="oracle_dev">Oracle - DEV (csebsd2)</option>
            <option value="oracle_f1">Oracle - F1 (csebsf1)</option>
            <option value="oracle_prod">Oracle - PROD (EBSP_BI)</option>
          </select>
        </div>
      </div>

      {/* Summary KPI Cards */}
      {summary && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '20px' }}>
          <div style={{ background: 'var(--bg-card)', padding: '16px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Total Cases Built (cases_bld_stg)</div>
            <div style={{ fontSize: '24px', fontWeight: 700, color: 'var(--color-primary)', marginTop: '4px' }}>
              {summary.total_cases_built.toLocaleString()}
            </div>
          </div>
          <div style={{ background: 'var(--bg-card)', padding: '16px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Original Order Qty (orgnl_ordr_qty)</div>
            <div style={{ fontSize: '24px', fontWeight: 700, color: '#34d399', marginTop: '4px' }}>
              {summary.total_original_order_qty.toLocaleString()}
            </div>
          </div>
          <div style={{ background: 'var(--bg-card)', padding: '16px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Invoices Processed</div>
            <div style={{ fontSize: '24px', fontWeight: 700, color: '#c084fc', marginTop: '4px' }}>
              {summary.total_invoices_processed}
            </div>
          </div>
          <div style={{ background: 'var(--bg-card)', padding: '16px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Procurement Transfer Rate</div>
            <div style={{ fontSize: '24px', fontWeight: 700, color: '#f59e0b', marginTop: '4px' }}>
              {summary.procurement_fulfillment_rate}
            </div>
          </div>
        </div>
      )}

      {/* Row Count Badge & Query Status */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
        <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)' }}>
          📊 Data Table Rows: <span style={{ color: 'var(--color-primary-light)', fontWeight: 700 }}>{items.length}</span> / {totalCount} Loaded
        </div>
      </div>

      {/* Warehouse Items Table with Vertical Scroll Bar & Automatic Infinite Load */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '20px', color: 'var(--text-secondary)' }}>Loading warehouse statistics...</div>
      ) : (
        <div
          onScroll={handleScroll}
          style={{
            maxHeight: '400px',
            overflowY: 'auto',
            border: '1px solid var(--border-color)',
            borderRadius: '8px',
            background: 'var(--bg-card)'
          }}
        >
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
            <thead style={{ position: 'sticky', top: 0, background: '#161B22', zIndex: 2 }}>
              <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                <th style={{ padding: '12px 10px' }}>Warehouse</th>
                <th style={{ padding: '12px 10px' }}>Batch ID</th>
                <th style={{ padding: '12px 10px' }}>Invoice #</th>
                <th style={{ padding: '12px 10px' }}>Customer Item Code</th>
                <th style={{ padding: '12px 10px' }}>C&S Item Code</th>
                <th style={{ padding: '12px 10px' }}>Cases Built Qty</th>
                <th style={{ padding: '12px 10px' }}>Order Qty</th>
                <th style={{ padding: '12px 10px' }}>Scratch Qty</th>
                <th style={{ padding: '12px 10px' }}>Sub Item (sl_itm_ind)</th>
                <th style={{ padding: '12px 10px' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <td style={{ padding: '10px', fontWeight: 700, color: 'var(--color-cyan)' }}>{item.whs_num}</td>
                  <td style={{ padding: '10px', color: '#f59e0b', fontWeight: 600, fontFamily: 'monospace' }}>{item.batch_id || '—'}</td>
                  <td style={{ padding: '10px', color: 'var(--color-primary)' }}>{item.invc_num_stg}</td>
                  <td style={{ padding: '10px' }}>{item.cust_item_code}</td>
                  <td style={{ padding: '10px', color: '#34d399', fontWeight: 600 }}>{item.cs_item_code}</td>
                  <td style={{ padding: '10px', fontWeight: 700 }}>{item.cases_bld_stg}</td>
                  <td style={{ padding: '10px' }}>{item.orgnl_ordr_qty_stg}</td>
                  <td style={{ padding: '10px', color: '#ef4444' }}>{item.whs_scrtch_qty_stg}</td>
                  <td style={{ padding: '10px' }}>
                    <span className="badge" style={{ background: 'rgba(124,58,237,0.2)', color: '#c084fc' }}>
                      {item.sl_itm_ind_stg}
                    </span>
                  </td>
                  <td style={{ padding: '10px' }}>
                    <span className={`badge ${item.procurement_transfer_status === 'COMPLETED' ? 'badge-green' : 'badge-amber'}`}>
                      ● {item.procurement_transfer_status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {loadingMore && (
            <div style={{ textAlign: 'center', padding: '12px', fontSize: '12px', color: 'var(--color-primary-light)', fontWeight: 600 }}>
              ⚡ Querying next 20 rows...
            </div>
          )}
        </div>
      )}
    </div>
  );
}
