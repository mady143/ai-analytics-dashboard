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
import psycopg2
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

# Global threadpool for non-blocking DB execution
db_executor = ThreadPoolExecutor(max_workers=10)

# Target DB Configurations with strictly separated PROD and DEV credentials
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
    "pg_prod": {
        "type": "PostgreSQL",
        "env": "PROD",
        "host": "gc-ue4-psql-sni-prd01.prod.gcp.cswg.com",
        "port": 5432,
        "dbname": "sptnintgdb",
        "user": "sptnintg_ro",
        "password": "63Z3zk-kPEID3"
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
    },
    "oracle_prod": {
        "type": "Oracle",
        "env": "PROD",
        "host": "ebsdb.cswg.com",
        "port": 1521,
        "service_name": "EBSP_BI",
        "user": "XXMKTMED_DEALS_RO"
    }
}


def _raw_postgres_query(config: Dict[str, Any], oerdte: str = "", batch_id: str = "", oewhse: str = "", oeinv: str = "", limit: int = 500) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, Dict[str, int]]]:
    """
    Raw PostgreSQL query execution matching exact parameters (oerdte, batch_id, oewhse, oeinvo).
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
            conditions.append("oewhse = %s")
            params.append(str(oewhse).strip())
        if oeinv:
            conditions.append("oeinvo = %s")
            params.append(str(oeinv).strip())

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
            scratch = _safe_int(r[8]) if r[8] is not None else max(0, ordr - built)
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


def _fetch_from_postgres(config: Dict[str, Any], oerdte: str = "", batch_id: str = "", oewhse: str = "", oeinv: str = "", limit: int = 500) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, Dict[str, int]]]:
    """Wraps raw Postgres query with a 15.0s threadpool timeout to allow sufficient time for remote database connection."""
    future = db_executor.submit(_raw_postgres_query, config, oerdte, batch_id, oewhse, oeinv, limit)
    try:
        return future.result(timeout=15.0)
    except FuturesTimeoutError:
        print(f"[WarehouseService] DB Connection timed out after 15.0s on host {config.get('host')}")
        return [], [], {}
    except Exception as e:
        print(f"[WarehouseService] DB Execution error: {e}")
        return [], [], {}


def get_warehouse_statistics(
    target_db: str = "pg_dev",
    oerdte: str = "",
    batch_id: str = "",
    oewhse: str = "",
    oeinv: str = "",
    from_date: str = "",
    to_date: str = "",
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

    if config["type"] == "PostgreSQL":
        all_items, distinct_warehouses, whs_totals_map = _fetch_from_postgres(config, oerdte=oerdte, batch_id=batch_id, oewhse=oewhse, oeinv=oeinv, limit=500)

    # Strict filtering for batch_id, oewhse, and oeinv
    if oewhse:
        all_items = [it for it in all_items if str(it.get("whs_num", "")).strip() == str(oewhse).strip()]
        distinct_warehouses = [str(oewhse).strip()] if len(all_items) > 0 else []
        whs_totals_map = {k: v for k, v in whs_totals_map.items() if k == str(oewhse).strip()}
    if batch_id:
        all_items = [it for it in all_items if str(it.get("batch_id", "")).strip() == str(batch_id).strip()]
        distinct_warehouses = sorted(list({item["whs_num"] for item in all_items if item.get("whs_num")}))
    if oeinv:
        all_items = [it for it in all_items if str(it.get("invc_num_stg", "")).strip() == str(oeinv).strip()]
        distinct_warehouses = sorted(list({item["whs_num"] for item in all_items if item.get("whs_num")}))

    # Interleave line items round-robin across distinct warehouses so all warehouses are represented in table view
    if distinct_warehouses and not oewhse:
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
