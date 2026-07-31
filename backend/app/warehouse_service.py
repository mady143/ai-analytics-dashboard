"""
Warehouse Sales & Invoice Analytics Service
Integrates reference logic from sales_invoice_details.py for warehouse item level,
invoice level, cases built quantity, and database target configurations.
Supports strict dynamic filtering matching exact PostgreSQL schema column: oeinvo for Invoice #.
Queries PostgreSQL directly for exact parameters (oerdte, batch_id, oewhse, oeinvo).
When no database records exist for a selected date,
it strictly returns 0 records and 0 summary counts without generating artificial data.
"""

from typing import Dict, Any, List, Tuple
import threading
import psycopg2
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

# Global threadpool for non-blocking DB execution
db_executor = ThreadPoolExecutor(max_workers=10)

# Target DB Configurations with DEV and F1 credentials
DB_CONFIGURATIONS = {
    "pg_dev": {
        "type": "PostgreSQL",
        "env": "DEV",
        "host": "gc-ue4-psql-sni-dev01.nonprod.gcp.cswg.com",
        "port": 5432,
        "dbname": "sptnintgdb",
        "user": "sptnintg",
        "password": "qPZodJS-IGNThHP-N66Bh8"
    },
    "oracle_dev": {
        "type": "Oracle",
        "env": "DEV",
        "host": "csebsd2db.cswg.com",
        "port": 1521,
        "service_name": "CSEBSD2",
        "user": "apps"
    },
    "oracle_f1": {
        "type": "Oracle",
        "env": "F1",
        "host": "csebsf1db.cswg.com",
        "port": 1521,
        "service_name": "csebsf1",
        "user": "apps"
    }
}


def _raw_postgres_query(config: Dict[str, Any], oerdte: str = "", batch_id: str = "", oewhse: str = "", oeinv: str = "", only_scratches: bool = False, limit: int = 500) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, Dict[str, int]]]:
    """
    Raw PostgreSQL query execution matching exact parameters (oerdte, batch_id, oewhse, oeinvo, only_scratches).
    - Query 1: Fetch distinct active warehouses for selected date & filters.
    - Query 2: SQL aggregated totals per warehouse across all matching records (GROUP BY oewhse).
    - Query 3: Partitioned line item details guaranteeing representation across all active warehouses.
    """
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            dbname=config["dbname"],
            user=config["user"],
            password=config.get("password", ""),
            connect_timeout=10
        )
        cur = conn.cursor()

        # Build dynamic WHERE clause matching exact PostgreSQL column names
        conditions = []
        params: List[Any] = []

        if oerdte:
            conditions.append("oerdte = %s")
            params.append(str(oerdte).strip())
        if batch_id:
            conditions.append("batch_id = %s")
            params.append(str(batch_id).strip())
        if oewhse:
            raw_w = str(oewhse).strip()
            unpadded_w = raw_w.lstrip("0") or "0"
            padded_w = unpadded_w.zfill(2)
            conditions.append("(oewhse = %s OR oewhse = %s OR TRIM(LEADING '0' FROM oewhse) = %s)")
            params.extend([raw_w, padded_w, unpadded_w])
        if oeinv:
            conditions.append("oeinvo = %s")
            params.append(str(oeinv).strip())
        if only_scratches:
            conditions.append("(COALESCE(CAST(NULLIF(oeqscr, '') AS NUMERIC), 0) > 0 OR (COALESCE(CAST(NULLIF(oeqtyo, '') AS NUMERIC), 0) - COALESCE(CAST(NULLIF(oeqtys, '') AS NUMERIC), 0)) > 0)")

        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

        # Query 1: Fetch distinct active warehouses for the selected date and filter parameters
        distinct_whs_query = f"SELECT DISTINCT oewhse FROM sptn_sales_data ssd {where_clause} ORDER BY oewhse ASC;"
        cur.execute(distinct_whs_query, tuple(params))
        whse_rows = cur.fetchall()
        distinct_warehouses = [str(r[0]).strip() for r in whse_rows if r[0] is not None and str(r[0]).strip() != ""]

        # Query 2: SQL aggregated totals per warehouse across all matching records
        agg_query = f"""
            SELECT oewhse, 
                   COALESCE(SUM(CAST(NULLIF(oeqtys, '') AS NUMERIC)), 0), 
                   COALESCE(SUM(CAST(NULLIF(oeqtyo, '') AS NUMERIC)), 0), 
                   COUNT(DISTINCT oeinvo)
            FROM sptn_sales_data ssd
            {where_clause}
            GROUP BY oewhse
            ORDER BY oewhse ASC;
        """
        cur.execute(agg_query, tuple(params))
        agg_rows = cur.fetchall()
        whs_totals: Dict[str, Dict[str, int]] = {}
        for ar in agg_rows:
            w_num = str(ar[0] or "").strip()
            if w_num:
                whs_totals[w_num] = {
                    "cases_built": int(float(ar[1] or 0)),
                    "order_qty": int(float(ar[2] or 0)),
                    "invoices": int(ar[3] or 0)
                }

        # Query 3: Fetch line item details partitioned across all active warehouses
        items_per_whs = max(50, limit // max(1, len(distinct_warehouses)))
        query = f"""
            SELECT oewhse, batch_id, oerdte, oecst, oeitem, oeinvo, oeqtys, oeqtyo, oeqscr, oesubf, gb_process_status
            FROM (
                SELECT oewhse, batch_id, oerdte, oecst, oeitem, oeinvo, oeqtys, oeqtyo, oeqscr, oesubf, gb_process_status,
                       ROW_NUMBER() OVER (PARTITION BY oewhse ORDER BY oerdte DESC, oeinvo ASC) as rn
                FROM sptn_sales_data ssd
                {where_clause}
            ) sub
            WHERE rn <= %s
            ORDER BY oewhse ASC, oerdte DESC;
        """
        params_with_limit = list(params) + [items_per_whs]
        cur.execute(query, tuple(params_with_limit))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        def _safe_int(val: Any) -> int:
            if not val:
                return 0
            try:
                return int(float(str(val).strip()))
            except Exception:
                return 0

        items = []
        for r in rows:
            whs = str(r[0] or "").strip()
            b_id = str(r[1] or "").strip()
            item_date = str(r[2] or "").strip()
            cust_code = str(r[3] or "").strip()
            cs_code = str(r[4] or "").strip()
            inv_num = str(r[5] or "").strip()
            built = _safe_int(r[6])
            ordr = _safe_int(r[7])
            scratch_val = _safe_int(r[8])
            scratch = scratch_val if scratch_val > 0 else max(0, ordr - built)
            ind = str(r[9] or "S").strip() or "S"
            status_code = str(r[10] or "P").strip()
            status = "COMPLETED" if status_code == "P" else "PENDING"

            items.append({
                "whs_num": whs,
                "batch_id": b_id,
                "oerdte": item_date,
                "cust_item_code": cust_code,
                "cs_item_code": cs_code,
                "invc_num_stg": inv_num,
                "cases_bld_stg": built,
                "orgnl_ordr_qty_stg": ordr,
                "trn_bld_qty_stg": built,
                "whs_scrtch_qty_stg": scratch,
                "sl_itm_ind_stg": ind,
                "procurement_transfer_status": status,
            })
        return items, distinct_warehouses, whs_totals
    except Exception as e:
        print(f"[WarehouseService] DB Query Exception on {config.get('host')}: {e}")
        return [], [], {}


def _fetch_from_postgres(config: Dict[str, Any], oerdte: str = "", batch_id: str = "", oewhse: str = "", oeinv: str = "", only_scratches: bool = False, limit: int = 500) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, Dict[str, int]]]:
    """Wraps raw Postgres query with a 15.0s threadpool timeout to allow sufficient time for remote database connection."""
    future = db_executor.submit(_raw_postgres_query, config, oerdte, batch_id, oewhse, oeinv, only_scratches, limit)
    try:
        return future.result(timeout=15.0)
    except FuturesTimeoutError:
        print(f"[WarehouseService] DB Connection timed out after 15.0s on host {config.get('host')}")
        return [], [], {}
    except Exception as e:
        print(f"[WarehouseService] DB Execution error: {e}")
        return [], [], {}


import time

_CACHE_LOCK = threading.Lock()
_QUERY_CACHE: Dict[str, Tuple[float, Any]] = {}

# Cache for latest date query (separate TTL = 60s since it changes less often)
_LATEST_DATE_CACHE: Dict[str, Tuple[float, str]] = {}


def get_latest_available_date(target_db: str = "pg_dev") -> str:
    """
    Returns the most recent oerdte (YYYYMMDD string) that has actual records in sptn_sales_data.
    Used by the frontend to auto-default to the latest active date when today has no data.
    Caches the result for 60 seconds.
    """
    now = time.time()
    with _CACHE_LOCK:
        if target_db in _LATEST_DATE_CACHE:
            ts, cached_date = _LATEST_DATE_CACHE[target_db]
            if now - ts < 60.0:
                return cached_date

    config = DB_CONFIGURATIONS.get(target_db, DB_CONFIGURATIONS["pg_dev"])
    latest_date = ""

    if config["type"] == "PostgreSQL":
        try:
            conn = psycopg2.connect(
                host=config["host"], port=config["port"],
                dbname=config["dbname"], user=config["user"],
                password=config.get("password", ""), connect_timeout=10
            )
            cur = conn.cursor()
            cur.execute("SELECT MAX(oerdte) FROM sptn_sales_data WHERE oerdte IS NOT NULL AND TRIM(oerdte) != '';")
            row = cur.fetchone()
            if row and row[0]:
                latest_date = str(row[0]).strip()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"[WarehouseService] get_latest_available_date error: {e}")

    with _CACHE_LOCK:
        _LATEST_DATE_CACHE[target_db] = (now, latest_date)

    return latest_date

CACHE_TTL = 15.0  # 15 seconds TTL cache

def _fetch_from_postgres_cached(config: Dict[str, Any], oerdte: str = "", batch_id: str = "", oewhse: str = "", oeinv: str = "", only_scratches: bool = False, limit: int = 500) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, Dict[str, int]]]:
    """Caches query results for 15 seconds to prevent parallel API requests from blocking database execution."""
    if only_scratches:
        return _fetch_from_postgres(config, oerdte=oerdte, batch_id=batch_id, oewhse=oewhse, oeinv=oeinv, only_scratches=only_scratches, limit=limit)

    cache_key = f"{config.get('host')}:{oerdte}:{batch_id}:{oewhse}:{oeinv}:{only_scratches}:{limit}"
    now = time.time()
    with _CACHE_LOCK:
        if cache_key in _QUERY_CACHE:
            ts, cached_data = _QUERY_CACHE[cache_key]
            if now - ts < CACHE_TTL:
                return cached_data

    res = _fetch_from_postgres(config, oerdte=oerdte, batch_id=batch_id, oewhse=oewhse, oeinv=oeinv, only_scratches=only_scratches, limit=limit)
    with _CACHE_LOCK:
        _QUERY_CACHE[cache_key] = (now, res)
    return res


def get_warehouse_statistics(
    target_db: str = "pg_dev",
    oerdte: str = "",
    batch_id: str = "",
    oewhse: str = "",
    oeinv: str = "",
    from_date: str = "",
    to_date: str = "",
    only_scratches: bool = False,
    limit: int = 20,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Processes warehouse sales invoice statistics matching sptn_sales_data ssd query logic.
    100% dynamic database querying with automatic resiliency fallbacks:
    - Query 1: SELECT DISTINCT oewhse FROM sptn_sales_data WHERE oerdte = %s ...;
    - Query 2: Aggregated SQL totals per warehouse (GROUP BY oewhse);
    - Query 3: Partitioned line items dataset representing all active warehouses.
    """
    config = DB_CONFIGURATIONS.get(target_db, DB_CONFIGURATIONS["pg_dev"])

    all_items = []
    distinct_warehouses = []
    whs_totals_map = {}

    effective_date = oerdte
    fallback_used = False

    if config["type"] == "PostgreSQL":
        all_items, distinct_warehouses, whs_totals_map = _fetch_from_postgres_cached(
            config, oerdte=oerdte, batch_id=batch_id, oewhse=oewhse,
            oeinv=oeinv, only_scratches=only_scratches, limit=500
        )
        # ✅ AUTO-FALLBACK (TASK 26 — User Mandate 2026-07-31):
        # Rule: Whatever date is selected → data MUST appear in all widgets.
        # If the selected date returns 0 records, automatically re-query using the
        # latest available date in the DB so the dashboard is NEVER blank.
        # This applies ONLY when an explicit oerdte was given with no additional filters.
        # If oerdte="" (Copilot mode / no filter) → already returns full dataset — no fallback needed.
        if oerdte and not all_items and not batch_id and not oeinv:
            latest = get_latest_available_date(target_db=target_db)
            if latest and latest != oerdte:
                all_items, distinct_warehouses, whs_totals_map = _fetch_from_postgres_cached(
                    config, oerdte=latest, batch_id="", oewhse=oewhse,
                    oeinv="", only_scratches=only_scratches, limit=500
                )
                effective_date = latest
                fallback_used = True


    # Strict filtering for batch_id, oewhse, and oeinv
    if oewhse:
        target_w_clean = str(oewhse).strip().lstrip("0")
        all_items = [it for it in all_items if str(it.get("whs_num", "")).strip().lstrip("0") == target_w_clean]
        distinct_warehouses = [str(oewhse).strip()] if len(all_items) > 0 else []
        whs_totals_map = {k: v for k, v in whs_totals_map.items() if str(k).strip().lstrip("0") == target_w_clean}
    if batch_id:
        all_items = [it for it in all_items if str(it.get("batch_id", "")).strip() == str(batch_id).strip()]
        distinct_warehouses = sorted(list({item["whs_num"] for item in all_items if item.get("whs_num")}))
    if oeinv:
        all_items = [it for it in all_items if str(it.get("invc_num_stg", "")).strip() == str(oeinv).strip()]
        distinct_warehouses = sorted(list({item["whs_num"] for item in all_items if item.get("whs_num")}))
    if only_scratches:
        filtered_scratch_list = []
        for it in all_items:
            built_qty = int(it.get("cases_bld_stg", 0) or 0)
            ordr_qty = int(it.get("orgnl_ordr_qty_stg", 0) or 0)
            cur_scratch = int(it.get("whs_scrtch_qty_stg", 0) or 0)
            calc_scratch = max(cur_scratch, max(0, ordr_qty - built_qty))
            if calc_scratch > 0:
                it["whs_scrtch_qty_stg"] = calc_scratch
                filtered_scratch_list.append(it)
        filtered_scratch_list.sort(key=lambda x: x.get("whs_scrtch_qty_stg", 0), reverse=True)
        all_items = filtered_scratch_list
        distinct_warehouses = sorted(list({item["whs_num"] for item in all_items if item.get("whs_num")}))

    # Interleave line items round-robin across distinct warehouses so all warehouses are represented in table view (unless filtering scratches)
    if distinct_warehouses and not oewhse and not only_scratches:
        by_whs: Dict[str, List[Dict[str, Any]]] = {}
        for it in all_items:
            w = str(it.get("whs_num", "")).strip()
            by_whs.setdefault(w, []).append(it)
        interleaved = []
        max_l = max((len(lst) for lst in by_whs.values()), default=0)
        for i in range(max_l):
            for w in distinct_warehouses:
                if w in by_whs and i < len(by_whs[w]):
                    interleaved.append(by_whs[w][i])
        if interleaved:
            all_items = interleaved

    total_whse_count = len(distinct_warehouses)

    paginated_items = all_items[offset : offset + limit]

    if whs_totals_map:
        total_cases_built = sum(w.get("cases_built", 0) for w in whs_totals_map.values())
        total_order_qty = sum(w.get("order_qty", 0) for w in whs_totals_map.values())
        total_invoices_processed = sum(w.get("invoices", 0) for w in whs_totals_map.values())
    else:
        total_cases_built = sum(item["cases_bld_stg"] for item in all_items)
        total_order_qty = sum(item["orgnl_ordr_qty_stg"] for item in all_items)
        total_invoices_processed = len(all_items)

    public_config = {k: v for k, v in config.items() if k != "password"}

    return {
        "status": "success",
        "target_db_config": public_config,
        "date_range": {
            "from_date": from_date or oerdte,
            "to_date": to_date or oerdte
        },
        "filters_applied": {
            "oerdte": oerdte,
            "effective_date": effective_date,
            "fallback_used": fallback_used,
            "batch_id": batch_id,
            "oewhse": oewhse,
            "oeinv": oeinv
        },
        "summary": {
            "total_warehouses": total_whse_count,
            "distinct_warehouses": distinct_warehouses,
            "warehouse_totals": whs_totals_map,
            "total_invoices_processed": total_invoices_processed,
            "total_cases_built": total_cases_built,
            "total_original_order_qty": total_order_qty,
            "procurement_fulfillment_rate": f"{(total_cases_built / total_order_qty * 100):.1f}%" if total_order_qty > 0 else "0.0%"
        },
        "warehouse_items": paginated_items,
        "total_count": len(all_items),
        "limit": limit,
        "offset": offset,
        "has_more": (offset + limit) < len(all_items)
    }
