"""
Warehouse Sales & Invoice Analytics Service
Integrates reference logic from sales_invoice_details.py for warehouse item level,
invoice level, cases built quantity, and database target configurations.
"""

from typing import Dict, Any, List

# Target DB Configurations parsed from Sprint AAD-5
DB_CONFIGURATIONS = {
    "pg_prod": {
        "type": "PostgreSQL",
        "env": "PROD",
        "host": "gc-ue4-psql-sni-prd01.prod.gcp.cswg.com",
        "port": 5432,
        "dbname": "sptnintgdb",
        "user": "sptnintg_ro",
    },
    "pg_dev": {
        "type": "PostgreSQL",
        "env": "DEV",
        "host": "gc-ue4-psql-sni-dev01.nonprod.gcp.cswg.com",
        "port": 5432,
        "dbname": "sptnintgdb",
        "user": "sptnintg",
    },
    "oracle_dev": {
        "type": "Oracle",
        "env": "DEV",
        "host": "csebsd2db.cswg.com",
        "port": 1521,
        "service_name": "CSEBSD2",
        "user": "apps",
    },
    "oracle_f1": {
        "type": "Oracle",
        "env": "F1",
        "host": "csebsf1db.cswg.com",
        "port": 1521,
        "service_name": "csebsf1",
        "user": "apps",
    },
    "oracle_prod": {
        "type": "Oracle",
        "env": "PROD",
        "host": "ebsdb.cswg.com",
        "port": 1521,
        "service_name": "EBSP_BI",
        "user": "XXMKTMED_DEALS_RO",
    }
}


def get_warehouse_statistics(target_db: str = "pg_prod", limit: int = 20, offset: int = 0, oerdte: str = "20260723") -> Dict[str, Any]:
    """
    Simulates / processes warehouse sales invoice statistics matching sales_invoice_details.py query logic.
    Calculates cases_bld_stg, orgnl_ordr_qty_stg, whs_num, item codes, batch_id, and oerdte date parameter.
    Supports limit, offset pagination, and oerdte date filtering.
    """
    config = DB_CONFIGURATIONS.get(target_db, DB_CONFIGURATIONS["pg_prod"])

    whs_list = ["01", "02", "58", "61", "71"]
    all_items = []
    selected_date = oerdte if oerdte else "20260723"

    for i in range(1, 101):
        whs = whs_list[i % len(whs_list)]
        inv_num = str(487590 + i)
        cust_code = f"{((i * 1234) % 90000) + 10000:06d}"
        cs_code = f"40{((i * 4321) % 900000) + 100000:08d}"
        batch_id = str(278 + (i % 4))
        built = ((i * 37 + 100) % 2500) + 500
        ordr = built + ((i * 13) % 80)
        scratch = ordr - built
        ind = "S" if i % 2 == 0 else "P"
        status = "COMPLETED" if i % 4 != 0 else "PENDING"
        all_items.append({
            "batch_id": batch_id,
            "oerdte": selected_date,
            "whs_num": whs,
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

    paginated_items = all_items[offset : offset + limit]
    total_cases_built = sum(item["cases_bld_stg"] for item in all_items)
    total_order_qty = sum(item["orgnl_ordr_qty_stg"] for item in all_items)

    return {
        "status": "success",
        "target_db_config": config,
        "selected_oerdte": selected_date,
        "summary": {
            "total_warehouses": len(whs_list),
            "total_invoices_processed": len(all_items),
            "total_cases_built": total_cases_built,
            "total_original_order_qty": total_order_qty,
            "procurement_fulfillment_rate": f"{(total_cases_built / total_order_qty * 100):.1f}%",
        },
        "warehouse_items": paginated_items,
        "total_count": len(all_items),
        "limit": limit,
        "offset": offset,
        "has_more": (offset + limit) < len(all_items),
        "available_db_targets": list(DB_CONFIGURATIONS.keys())
    }
