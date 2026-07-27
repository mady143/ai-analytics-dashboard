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
