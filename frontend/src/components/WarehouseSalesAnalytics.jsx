import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API = import.meta.env.VITE_API_URL || '';

export default function WarehouseSalesAnalytics({ globalDate, globalTargetDb = 'pg_dev', externalFilters }) {
  const [summary, setSummary] = useState(null);
  const [items, setItems] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);

  // Table Level Filter Parameters
  const [filterWhs, setFilterWhs] = useState('');
  const [filterBatchId, setFilterBatchId] = useState('');
  const [filterInvoice, setFilterInvoice] = useState('');

  // Handle external filter requests from Copilot or Anomaly panel
  useEffect(() => {
    if (externalFilters) {
      if (externalFilters.whse !== undefined) setFilterWhs(externalFilters.whse);
      if (externalFilters.batch !== undefined) setFilterBatchId(externalFilters.batch);
      if (externalFilters.invoice !== undefined) setFilterInvoice(externalFilters.invoice);
    }
  }, [externalFilters]);

  const LIMIT = 20;
  const oerdte = globalDate ? globalDate.replace(/-/g, '') : '';

  // Reset & initial load on DB target, date change, or filter inputs
  useEffect(() => {
    let isSubscribed = true;
    const fetchInitial = async () => {
      setLoading(true);
      try {
        const res = await axios.get(`${API}/api/warehouse/statistics?target_db=${globalTargetDb}&oerdte=${oerdte}&batch_id=${filterBatchId}&oewhse=${filterWhs}&oeinv=${filterInvoice}&limit=${LIMIT}&offset=0`);
        if (!isSubscribed) return;
        
        let fetchedItems = res.data?.warehouse_items || [];
        if (filterWhs) {
          const targetClean = String(filterWhs).trim().replace(/^0+/, '');
          fetchedItems = fetchedItems.filter(it => String(it.whs_num).trim().replace(/^0+/, '') === targetClean);
        }
        if (filterBatchId) {
          fetchedItems = fetchedItems.filter(it => String(it.batch_id).trim().includes(String(filterBatchId).trim()));
        }
        if (filterInvoice) {
          fetchedItems = fetchedItems.filter(it => String(it.invc_num_stg).trim().includes(String(filterInvoice).trim()));
        }
        
        setSummary(res.data.summary || null);
        setItems(fetchedItems);
        setTotalCount(res.data.total_count ?? fetchedItems.length);
        setHasMore(res.data.has_more ?? false);
      } catch (err) {
        if (!isSubscribed) return;
        console.error('[WarehouseSalesAnalytics] API query error:', err);
        setItems([]);
        setTotalCount(0);
        setSummary(null);
      } finally {
        if (isSubscribed) setLoading(false);
      }
    };
    fetchInitial();
    return () => { isSubscribed = false; };
  }, [globalTargetDb, oerdte, filterWhs, filterBatchId, filterInvoice]);

  // Load next batch on scroll down
  const loadMoreData = async () => {
    if (loadingMore || !hasMore) return;
    setLoadingMore(true);
    const nextOffset = items.length;
    try {
      const res = await axios.get(`${API}/api/warehouse/statistics?target_db=${globalTargetDb}&oerdte=${oerdte}&batch_id=${filterBatchId}&oewhse=${filterWhs}&oeinv=${filterInvoice}&limit=${LIMIT}&offset=${nextOffset}`);
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
    <div className="card" id="warehouse-table-card" style={{ marginTop: '24px', padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginBottom: '16px' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 700, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            Warehouse & Invoice Sales Analytics
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginTop: '4px' }}>
            Identifies sales information for warehouse item level and invoice level transfer to Procurement systems.
          </p>
        </div>

        {/* Dynamic Parameter Filter Bar: Warehouse (oewhse), Batch ID (batch_id), Invoice (oeinv) */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontSize: '11px', color: 'var(--text-secondary)', fontWeight: 600 }}>Warehouse (oewhse):</span>
            <select
              value={filterWhs}
              onChange={(e) => setFilterWhs(e.target.value)}
              style={{
                background: 'var(--bg-secondary)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border-color)',
                padding: '4px 8px',
                borderRadius: '6px',
                fontSize: '12px',
                fontWeight: 600
              }}
            >
              <option value="">All Warehouses</option>
              {globalTargetDb.toLowerCase().includes('dev') ? (
                <>
                  <option value="01">Whse 01</option>
                  <option value="02">Whse 02</option>
                  <option value="58">Whse 58</option>
                  <option value="61">Whse 61</option>
                  <option value="71">Whse 71</option>
                </>
              ) : (
                <>
                  <option value="58">Whse 58</option>
                  <option value="61">Whse 61</option>
                  <option value="71">Whse 71</option>
                </>
              )}
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontSize: '11px', color: 'var(--text-secondary)', fontWeight: 600 }}>Batch ID (batch_id):</span>
            <input
              type="text"
              placeholder="e.g. 1851"
              value={filterBatchId}
              onChange={(e) => setFilterBatchId(e.target.value)}
              style={{
                width: '90px',
                background: 'var(--bg-secondary)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border-color)',
                padding: '4px 8px',
                borderRadius: '6px',
                fontSize: '12px',
                fontWeight: 600
              }}
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontSize: '11px', color: 'var(--text-secondary)', fontWeight: 600 }}>Invoice # (oeinv):</span>
            <input
              type="text"
              placeholder="e.g. 487613"
              value={filterInvoice}
              onChange={(e) => setFilterInvoice(e.target.value)}
              style={{
                width: '100px',
                background: 'var(--bg-secondary)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border-color)',
                padding: '4px 8px',
                borderRadius: '6px',
                fontSize: '12px',
                fontWeight: 600
              }}
            />
          </div>

          <span style={{
            fontSize: '12px',
            color: '#34D399',
            background: 'rgba(52, 211, 153, 0.1)',
            border: '1px solid rgba(52, 211, 153, 0.2)',
            padding: '4px 10px',
            borderRadius: '6px',
            fontWeight: 700
          }}>
            Target DB: {globalTargetDb.toUpperCase()}
          </span>
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
          Data Table Rows: <span style={{ color: 'var(--color-primary-light)', fontWeight: 700 }}>{items.length}</span> / {totalCount} Loaded
        </div>
      </div>

      {/* Warehouse Items Table with Vertical Scroll Bar & Automatic Infinite Load */}
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
        <table id="warehouse-analytics-table" style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
          <thead style={{ position: 'sticky', top: 0, background: '#161B22', zIndex: 2 }}>
            <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
              <th style={{ padding: '12px 10px' }}>Warehouse</th>
              <th style={{ padding: '12px 10px' }}>Order Date</th>
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
            {loading ? (
              <tr>
                <td colSpan={11} style={{ textAlign: 'center', padding: '24px', color: 'var(--color-primary-light)', fontWeight: 600 }}>
                  Querying PostgreSQL Warehouse Statistics...
                </td>
              </tr>
            ) : items.length === 0 ? (
              <tr>
                <td colSpan={11} style={{ textAlign: 'center', padding: '32px 16px', color: 'var(--text-secondary)' }}>
                  <div style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: '14px' }}>
                    No Database Records Found for Selected Date ({globalDate || 'No Date'})
                  </div>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                    PostgreSQL {globalTargetDb.toUpperCase()} has 0 records matching the selected date & filter parameters. Please change the date picker above.
                  </div>
                </td>
              </tr>
            ) : (
              items.map((item, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <td style={{ padding: '10px', fontWeight: 700, color: 'var(--color-cyan)' }}>{item.whs_num}</td>
                  <td style={{ padding: '10px', color: '#60a5fa', fontWeight: 600, fontFamily: 'monospace' }}>{item.oerdte || '—'}</td>
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
              ))
            )}
          </tbody>
        </table>

        {loadingMore && (
          <div style={{ textAlign: 'center', padding: '12px', fontSize: '12px', color: 'var(--color-primary-light)', fontWeight: 600 }}>
            Querying next 20 rows...
          </div>
        )}
      </div>
    </div>
  );
}
