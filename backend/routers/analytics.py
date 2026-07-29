"""
Analytics Router — ML model training, evaluation, and prediction endpoints.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.schemas import TrainRequest, PredictRequest
from services import data_service, ml_service

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
    # Keyword detection for warehouses
    for w in ["58", "61", "71", "01", "02"]:
        if f"whse {w}" in prompt or f"warehouse {w}" in prompt or f"whs {w}" in prompt or prompt == w or w in prompt:
            filtered_whse = w
            break

    # Regex detection for batch ID and invoice #
    batch_match = re.search(r'(?:batch|batch_id)\s*#?\s*(\d+)', prompt)
    if batch_match:
        filtered_batch = batch_match.group(1)

    inv_match = re.search(r'(?:invoice|inv|oeinv)\s*#?\s*(\d+)', prompt)
    if inv_match:
        filtered_invoice = inv_match.group(1)

    # Response generation logic
    if "scratch" in prompt or "shortage" in prompt:
        scratch_items = [it for it in items if it.get("whs_scrtch_qty_stg", 0) > 0]
        if scratch_items and not filtered_whse:
            filtered_whse = str(scratch_items[0].get("whs_num", "")).strip()
        answer = f"Found {len(scratch_items)} line item(s) with scratch quantities under {target_db.upper()} for date {oerdte or 'all'}. Total scratches: {sum(it.get('whs_scrtch_qty_stg', 0) for it in scratch_items):,} cases."
        suggested = ["Filter Scratch Items", "View Warehouse 58", "Check Pending Transfers"]
    elif "pending" in prompt or "transfer" in prompt:
        pending_items = [it for it in items if it.get("procurement_transfer_status") == "PENDING"]
        if pending_items and not filtered_whse:
            filtered_whse = str(pending_items[0].get("whs_num", "")).strip()
        answer = f"Detected {len(pending_items)} pending procurement transfer line items in {target_db.upper()} database for date {oerdte or 'all'}."
        suggested = ["Show Pending Items", "Check High Volume Orders", "Warehouse 61 Breakdown"]
    elif filtered_whse:
        whs_stat = whs_totals_map.get(filtered_whse, {}) or whs_totals_map.get(filtered_whse.zfill(2), {})
        if whs_stat:
            cases = whs_stat.get("cases_built", 0)
            item_count = whs_stat.get("invoices", 0)
        else:
            whs_items = [it for it in items if str(it.get("whs_num")).strip().lstrip("0") == filtered_whse.lstrip("0")]
            cases = sum(it.get("cases_bld_stg", 0) for it in whs_items)
            item_count = len(whs_items)
            
        answer = f"Warehouse {filtered_whse} has {item_count} items loaded with {cases:,} cases built for target DB {target_db.upper()} for date {oerdte or 'all'}."
        suggested = [f"Focus Warehouse {filtered_whse}", "Clear Filters", "Show Scratch Rates"]
    else:
        answer = f"Analyzed database query for '{request.prompt}'. Connected to {target_db.upper()} database for date {oerdte or 'all'} with {summary.get('total_warehouses', 0)} active warehouses and {summary.get('total_cases_built', 0):,} total cases built."
        suggested = ["High Scratch Quantity", "Pending Transfers", "Warehouse 58 Overview"]
        
    return JSONResponse({
        "status": "success",
        "prompt": request.prompt,
        "summary_answer": answer,
        "filtered_whse": filtered_whse,
        "filtered_batch": filtered_batch,
        "filtered_invoice": filtered_invoice,
        "suggested_actions": suggested,
        "metrics_found": {
            "total_warehouses": summary.get("total_warehouses", 0),
            "total_cases_built": summary.get("total_cases_built", 0),
            "fulfillment_rate": summary.get("procurement_fulfillment_rate", "100.0%")
        }
    })


# ── Real-Time Anomaly Alert Engine ─────────────────────────────────────────────
@router.get("/anomalies")
async def get_anomalies(target_db: str = "pg_dev", oerdte: str = ""):
    """Evaluates database records and returns active risk anomalies."""
    from app.warehouse_service import get_warehouse_statistics
    
    stats = get_warehouse_statistics(target_db=target_db, oerdte=oerdte, limit=200)
    items = stats.get("warehouse_items", [])
    
    anomalies = []
    
    # 1. High Scratch Rate Anomaly (Critical)
    scratch_items = [it for it in items if it.get("whs_scrtch_qty_stg", 0) > 0]
    if scratch_items:
        tot_scratch = sum(it.get("whs_scrtch_qty_stg", 0) for it in scratch_items)
        anomalies.append({
            "id": "anomaly-scratch-high",
            "severity": "critical",
            "title": "High Scratch Quantity Detected",
            "warehouse": scratch_items[0].get("whs_num", "Multi"),
            "batch_id": scratch_items[0].get("batch_id", "—"),
            "count": len(scratch_items),
            "message": f"Detected {tot_scratch:,} scratched cases across {len(scratch_items)} line items.",
            "filter_whse": scratch_items[0].get("whs_num", "")
        })
        
    # 2. Pending Transfer Anomaly (Warning)
    pending_items = [it for it in items if it.get("procurement_transfer_status") == "PENDING"]
    if pending_items:
        anomalies.append({
            "id": "anomaly-pending-transfer",
            "severity": "warning",
            "title": "Procurement Transfers Pending",
            "warehouse": pending_items[0].get("whs_num", "Multi"),
            "batch_id": pending_items[0].get("batch_id", "—"),
            "count": len(pending_items),
            "message": f"Found {len(pending_items)} line items pending transfer to Procurement system.",
            "filter_whse": pending_items[0].get("whs_num", "")
        })
        
    # 3. High Volume Order Spike (Info)
    high_volume_items = [it for it in items if it.get("orgnl_ordr_qty_stg", 0) > 500]
    if high_volume_items:
        anomalies.append({
            "id": "anomaly-volume-spike",
            "severity": "info",
            "title": "High Volume Order Surge",
            "warehouse": high_volume_items[0].get("whs_num", "Multi"),
            "batch_id": high_volume_items[0].get("batch_id", "—"),
            "count": len(high_volume_items),
            "message": f"{len(high_volume_items)} order(s) exceeding 500 cases in single line item.",
            "filter_whse": high_volume_items[0].get("whs_num", "")
        })
        
    # Default baseline if zero anomalies
    if not anomalies:
        anomalies.append({
            "id": "anomaly-optimal",
            "severity": "optimal",
            "title": "Fulfillment Operations Nominal",
            "warehouse": "All",
            "batch_id": "—",
            "count": 0,
            "message": "Zero critical anomalies detected across active warehouse streams.",
            "filter_whse": ""
        })
        
    return JSONResponse({
        "status": "success",
        "target_db": target_db,
        "oerdte": oerdte,
        "total_anomalies": len(anomalies),
        "anomalies": anomalies
    })

