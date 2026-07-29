"""
Analytics Router — ML model training, evaluation, and prediction endpoints.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.schemas import TrainRequest, PredictRequest
from services import data_service, ml_service

import json
import difflib
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).parent.parent.parent
TAXONOMY_FILE = ROOT_DIR / "memory" / "nlp_taxonomy.json"

def load_nlp_taxonomy() -> dict:
    """Loads persistent NLP keyword taxonomy from memory/nlp_taxonomy.json."""
    if TAXONOMY_FILE.exists():
        try:
            data = json.loads(TAXONOMY_FILE.read_text(encoding="utf-8"))
            return data.get("taxonomy", {})
        except Exception:
            pass
    return {
        "scratch": ["scratch", "scratched", "shortage", "damaged", "missing", "unfulfilled", "unshipped", "scrtch", "defect"],
        "transfer": ["pending", "transfer", "procurement", "staged", "processing", "untransferred", "holding", "delayed"],
        "volume": ["volume", "surge", "spike", "large order", "bulk", "high cases"],
        "warehouse": ["warehouse", "whse", "facility", "loc", "site"]
    }

def learn_unknown_keywords(prompt_text: str, detected_intent: str) -> None:
    """Dynamically learns unknown words from user queries and appends them to memory/nlp_taxonomy.json."""
    if not TAXONOMY_FILE.exists() or not detected_intent:
        return
    try:
        data = json.loads(TAXONOMY_FILE.read_text(encoding="utf-8"))
        taxonomy = data.get("taxonomy", {})
        learned = set(data.get("learned_keywords", []))
        words = [w.strip().lower() for w in prompt_text.split() if len(w) > 3]
        
        category_words = taxonomy.get(detected_intent, [])
        for word in words:
            if word not in category_words:
                matches = difflib.get_close_matches(word, category_words, n=1, cutoff=0.7)
                if matches or any(kw in word for kw in ["scratch", "short", "trans", "vol", "whs"]):
                    taxonomy[detected_intent].append(word)
                    learned.add(word)
                    
        data["taxonomy"] = taxonomy
        data["learned_keywords"] = list(learned)
        data["last_updated"] = datetime.now().isoformat()
        TAXONOMY_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"[NLP Engine] Failed to record learned keywords: {e}")

router = APIRouter()


@router.post("/train")
async def train_model(request: TrainRequest):
    """Train ML model(s) on the current dataset."""
    df = data_service.get_or_generate()

    if request.target_column not in df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Column '{request.target_column}' not found. Available: {df.columns.tolist()}"
        )

    try:
        result = ml_service.train_models(
            df=df,
            target_col=request.target_column,
            model_type=request.model_type.value,
            test_size=request.test_size,
            n_estimators=request.n_estimators,
            max_depth=request.max_depth,
            lr_max_iter=request.lr_max_iter
        )
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@router.get("/results")
async def get_results():
    """Return the latest training results."""
    if not ml_service._models:
        raise HTTPException(
            status_code=404,
            detail="No models trained yet. Call POST /api/analytics/train first."
        )
    return JSONResponse({
        "trained_models": list(ml_service._models.keys()),
        "feature_columns": ml_service._feature_columns
    })


@router.post("/predict")
async def predict(request: PredictRequest):
    """Make a prediction using a trained model."""
    try:
        result = ml_service.predict(
            features=request.features,
            model_type=request.model_type.value
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return JSONResponse(result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/columns")
async def get_columns():
    """Return available columns for target selection."""
    df = data_service.get_or_generate()
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    return JSONResponse({
        "all_columns": df.columns.tolist(),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "suggested_targets": ["target", "attrition", "promoted", "performance_score"]
    })


# ── AI Data Copilot Endpoint ───────────────────────────────────────────────────
from pydantic import BaseModel
from typing import Optional

class CopilotRequest(BaseModel):
    prompt: str
    target_db: Optional[str] = "pg_dev"
    oerdte: Optional[str] = ""

@router.post("/ai-copilot")
async def ai_copilot_query(request: CopilotRequest):
    """Natural Language AI Data Copilot query parser and filter generator."""
    from app.warehouse_service import get_warehouse_statistics
    
    prompt = request.prompt.lower().strip()
    target_db = request.target_db or "pg_dev"
    oerdte = request.oerdte or ""
    
    stats = get_warehouse_statistics(target_db=target_db, oerdte=oerdte, limit=500)
    items = stats.get("warehouse_items", [])
    summary = stats.get("summary", {})
    whs_totals_map = summary.get("warehouse_totals", {})
    
    filtered_whse = ""
    filtered_batch = ""
    filtered_invoice = ""
    
    import re
    # 100% Dynamic warehouse extraction via regex (matches 'warehouse 58', 'whse 58', 'whs #58', or standalone warehouse numbers)
    whs_match = re.search(r'(?:warehouse|whse|whs|facility|loc|w)\s*#?\s*(\d+)', prompt, re.IGNORECASE)
    if whs_match:
        filtered_whse = whs_match.group(1).lstrip("0") or "0"
    else:
        # Dynamic fallback: check against distinct warehouses returned from active DB query
        distinct_whs_list = summary.get("distinct_warehouses", [])
        for w in distinct_whs_list:
            w_clean = str(w).strip().lstrip("0")
            if w_clean and re.search(r'\b0*' + re.escape(w_clean) + r'\b', prompt):
                filtered_whse = w_clean
                break

    # Regex detection for batch ID and invoice #
    batch_match = re.search(r'(?:batch|batch_id)\s*#?\s*(\d+)', prompt)
    if batch_match:
        filtered_batch = batch_match.group(1)

    inv_match = re.search(r'(?:invoice|inv|oeinv)\s*#?\s*(\d+)', prompt)
    if inv_match:
        filtered_invoice = inv_match.group(1)

    # If warehouse is specified, do a targeted query to ensure accurate totals with dynamic date fallback
    whs_stat = whs_totals_map.get(filtered_whse, {}) or whs_totals_map.get(filtered_whse.zfill(2), {})
    whs_items = [it for it in items if str(it.get("whs_num")).strip().lstrip("0") == filtered_whse.lstrip("0")]
    
    # Check if fallback is needed when selected date has 0 records
    fallback_used = stats.get("filters_applied", {}).get("fallback_used", False)
    effective_date = stats.get("filters_applied", {}).get("effective_date", oerdte)

    if filtered_whse and not whs_items and not whs_stat:
        # Perform explicit warehouse lookup without date constraint
        whs_specific_stats = get_warehouse_statistics(target_db=target_db, oerdte="", oewhse=filtered_whse, limit=500)
        whs_specific_items = whs_specific_stats.get("warehouse_items", [])
        if whs_specific_items:
            items = whs_specific_items
            summary = whs_specific_stats.get("summary", {})
            whs_totals_map = summary.get("warehouse_totals", {})
            whs_stat = whs_totals_map.get(filtered_whse, {}) or whs_totals_map.get(filtered_whse.zfill(2), {})
            whs_items = [it for it in items if str(it.get("whs_num")).strip().lstrip("0") == filtered_whse.lstrip("0")]
            fallback_used = True
            effective_date = items[0].get("oerdte", "")

    # Response generation logic
    date_label = f" (showing available dataset for date {effective_date})" if (fallback_used and effective_date) else f" for date {oerdte or 'all'}"

    # ── Expanded Dynamic NLP Taxonomy & Online Learning Engine ─────────────────
    taxonomy = load_nlp_taxonomy()
    prompt_lower = prompt.lower()
    
    scratch_keywords = taxonomy.get("scratch", ["scratch", "scratched", "shortage", "damaged", "missing", "unfulfilled"])
    transfer_keywords = taxonomy.get("transfer", ["pending", "transfer", "procurement", "staged", "processing", "untransferred"])
    volume_keywords = taxonomy.get("volume", ["volume", "surge", "spike", "large order", "bulk", "high cases"])

    is_scratch_query = any(kw in prompt_lower for kw in scratch_keywords)
    is_transfer_query = any(kw in prompt_lower for kw in transfer_keywords)
    is_volume_query = any(kw in prompt_lower for kw in volume_keywords)

    if is_scratch_query:
        learn_unknown_keywords(prompt, "scratch")
        scratch_items = [it for it in items if it.get("whs_scrtch_qty_stg", 0) > 0]
        if not scratch_items and not fallback_used:
            all_date_stats = get_warehouse_statistics(target_db=target_db, oerdte="", limit=500)
            scratch_items = [it for it in all_date_stats.get("warehouse_items", []) if it.get("whs_scrtch_qty_stg", 0) > 0]
            if scratch_items:
                fallback_used = True
                effective_date = scratch_items[0].get("oerdte", "")
                date_label = f" (showing available dataset for date {effective_date})"
        if scratch_items and not filtered_whse:
            filtered_whse = str(scratch_items[0].get("whs_num", "")).strip()
        answer = f"Found {len(scratch_items)} line item(s) with scratch quantities under {target_db.upper()}{date_label}. Total scratches: {sum(it.get('whs_scrtch_qty_stg', 0) for it in scratch_items):,} cases."
        suggested = ["Filter Scratch Items", "View Warehouse 58", "Check Pending Transfers"]
    elif is_transfer_query:
        learn_unknown_keywords(prompt, "transfer")
        pending_items = [it for it in items if it.get("procurement_transfer_status") in ("PENDING", "PROCESSING", "STAGED")]
        if not pending_items:
            all_date_stats = get_warehouse_statistics(target_db=target_db, oerdte="", limit=500)
            all_items = all_date_stats.get("warehouse_items", [])
            pending_items = [it for it in all_items if it.get("procurement_transfer_status") in ("PENDING", "PROCESSING", "STAGED")]
            if not pending_items and all_items:
                pending_items = all_items[:15]  # Fallback to general procurement transfer items
            if pending_items:
                fallback_used = True
                effective_date = pending_items[0].get("oerdte", "")
                date_label = f" (showing available dataset for date {effective_date})"
        if pending_items and not filtered_whse:
            filtered_whse = str(pending_items[0].get("whs_num", "")).strip()
        answer = f"Detected {len(pending_items)} procurement transfer line item(s) in {target_db.upper()} database{date_label}."
        suggested = ["Show Pending Items", "Check High Volume Orders", "Warehouse 61 Breakdown"]
    elif is_volume_query:
        high_vol_items = [it for it in items if it.get("orgnl_ordr_qty_stg", 0) > 500]
        answer = f"Identified {len(high_vol_items)} high-volume line item(s) exceeding 500 cases in {target_db.upper()}{date_label}."
        suggested = ["High Scratch Quantity", "Pending Transfers", "Warehouse 58 Overview"]
    elif filtered_whse:
        if whs_stat:
            cases = whs_stat.get("cases_built", 0)
            item_count = whs_stat.get("invoices", 0)
        else:
            cases = sum(it.get("cases_bld_stg", 0) for it in whs_items)
            item_count = len(whs_items)
            
        answer = f"Warehouse {filtered_whse} has {item_count} items loaded with {cases:,} cases built for target DB {target_db.upper()}{date_label}."
        suggested = [f"Focus Warehouse {filtered_whse}", "Clear Filters", "Show Scratch Rates"]
    else:
        answer = f"Analyzed database query for '{request.prompt}'. Connected to {target_db.upper()} database{date_label} with {summary.get('total_warehouses', 0)} active warehouses and {summary.get('total_cases_built', 0):,} total cases built."
        suggested = ["High Scratch Quantity", "Pending Transfers", "Warehouse 58 Overview"]
        
    return JSONResponse({
        "status": "success",
        "prompt": request.prompt,
        "summary_answer": answer,
        "filtered_whse": filtered_whse,
        "filtered_batch": filtered_batch,
        "filtered_invoice": filtered_invoice,
        "filter_scratch": is_scratch_query,
        "effective_date": effective_date,
        "suggested_actions": suggested,
        "metrics_found": {
            "total_warehouses": summary.get("total_warehouses", 0),
            "total_cases_built": summary.get("total_cases_built", 0),
            "fulfillment_rate": summary.get("procurement_fulfillment_rate", "100.0%")
        }
    })


# ── Real-Time Anomaly Alert Engine ─────────────────────────────────────────────
@router.get("/anomalies")
async def get_anomalies(target_db: str = "pg_dev", oerdte: str = "", oewhse: str = ""):
    """Evaluates database records and returns active risk anomalies."""
    from app.warehouse_service import get_warehouse_statistics
    
    stats = get_warehouse_statistics(target_db=target_db, oerdte=oerdte, oewhse=oewhse, limit=200)
    items = stats.get("warehouse_items", [])
    
    anomalies = []
    
    # 1. High Scratch Rate Anomaly (Critical)
    scratch_items = [it for it in items if it.get("whs_scrtch_qty_stg", 0) > 0]
    if not scratch_items:
        # Check across available dates if selected date has 0 scratch items
        all_scratch_stats = get_warehouse_statistics(target_db=target_db, oerdte="", oewhse=oewhse, only_scratches=True, limit=200)
        scratch_items = all_scratch_stats.get("warehouse_items", [])

    if scratch_items:
        tot_scratch = sum(it.get("whs_scrtch_qty_stg", 0) for it in scratch_items)
        whse_val = oewhse or scratch_items[0].get("whs_num", "Multi")
        eff_date = scratch_items[0].get("oerdte", "")
        anomalies.append({
            "id": "anomaly-scratch-high",
            "severity": "critical",
            "title": "High Scratch Quantity Detected",
            "warehouse": whse_val,
            "batch_id": scratch_items[0].get("batch_id", "—"),
            "count": len(scratch_items),
            "message": f"Detected {tot_scratch:,} scratched cases across {len(scratch_items)} line items for Warehouse {whse_val}{f' (Date {eff_date})' if eff_date else ''}.",
            "filter_whse": whse_val,
            "filter_scratch": True,
            "effective_date": eff_date
        })
        
    # 2. Pending Transfer Anomaly (Warning)
    pending_items = [it for it in items if it.get("procurement_transfer_status") == "PENDING"]
    if pending_items:
        whse_val = oewhse or pending_items[0].get("whs_num", "Multi")
        anomalies.append({
            "id": "anomaly-pending-transfer",
            "severity": "warning",
            "title": "Procurement Transfers Pending",
            "warehouse": whse_val,
            "batch_id": pending_items[0].get("batch_id", "—"),
            "count": len(pending_items),
            "message": f"Found {len(pending_items)} line items pending transfer to Procurement system for Warehouse {whse_val}.",
            "filter_whse": whse_val
        })
        
    # 3. High Volume Order Spike (Info)
    high_volume_items = [it for it in items if it.get("orgnl_ordr_qty_stg", 0) > 500]
    if high_volume_items:
        whse_val = oewhse or high_volume_items[0].get("whs_num", "Multi")
        anomalies.append({
            "id": "anomaly-volume-spike",
            "severity": "info",
            "title": "High Volume Order Surge",
            "warehouse": whse_val,
            "batch_id": high_volume_items[0].get("batch_id", "—"),
            "count": len(high_volume_items),
            "message": f"{len(high_volume_items)} order(s) exceeding 500 cases in single line item for Warehouse {whse_val}.",
            "filter_whse": whse_val
        })
        
    # Default baseline if zero anomalies
    if not anomalies:
        whse_display = oewhse if oewhse else "All"
        anomalies.append({
            "id": "anomaly-optimal",
            "severity": "optimal",
            "title": "Fulfillment Operations Nominal",
            "warehouse": whse_display,
            "batch_id": "—",
            "count": 0,
            "message": f"Zero critical anomalies detected across active streams{f' for Warehouse {oewhse}' if oewhse else ''}.",
            "filter_whse": oewhse
        })
        
    return JSONResponse({
        "status": "success",
        "target_db": target_db,
        "oerdte": oerdte,
        "total_anomalies": len(anomalies),
        "anomalies": anomalies
    })

