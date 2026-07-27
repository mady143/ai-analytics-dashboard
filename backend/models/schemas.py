"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
from enum import Enum


class ModelType(str, Enum):
    random_forest = "random_forest"
    logistic_regression = "logistic_regression"
    both = "both"


class Priority(str, Enum):
    urgent = "urgent"
    high = "high"
    medium = "medium"
    low = "low"


# ── Data Schemas ───────────────────────────────────────────────────────────────

class DataSummaryResponse(BaseModel):
    rows: int
    columns: int
    column_names: list[str]
    dtypes: dict[str, str]
    missing_values: dict[str, int]
    numeric_stats: dict[str, Any]


class SampleDataResponse(BaseModel):
    data: list[dict]
    columns: list[str]
    total_rows: int


# ── Analytics Schemas ──────────────────────────────────────────────────────────

class TrainRequest(BaseModel):
    target_column: str = Field(..., description="Name of the target/label column")
    model_type: ModelType = Field(ModelType.random_forest, description="Model to train")
    test_size: float = Field(0.2, ge=0.1, le=0.5, description="Test split ratio")
    n_estimators: int = Field(100, ge=10, le=500, description="RF: number of trees")
    max_depth: Optional[int] = Field(None, description="RF: max tree depth")
    lr_max_iter: int = Field(1000, ge=100, description="LR: max iterations")


class ModelMetrics(BaseModel):
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: list[list[int]]
    feature_importance: Optional[dict[str, float]] = None
    classification_report: dict[str, Any]


class TrainResponse(BaseModel):
    success: bool
    message: str
    results: list[ModelMetrics]
    training_time_seconds: float


class PredictRequest(BaseModel):
    features: dict[str, Any] = Field(..., description="Feature values for prediction")
    model_type: ModelType = Field(ModelType.random_forest)


class PredictResponse(BaseModel):
    prediction: Any
    probability: Optional[list[float]] = None
    model_used: str


# ── Chart Schemas ──────────────────────────────────────────────────────────────

class KPICard(BaseModel):
    title: str
    value: Any
    unit: Optional[str] = None
    trend: Optional[float] = None  # % change
    trend_direction: Optional[str] = None  # "up" | "down" | "flat"
    color: Optional[str] = "#7C3AED"


class ChartDataResponse(BaseModel):
    chart_type: str
    title: str
    data: list[dict]
    x_label: Optional[str] = None
    y_label: Optional[str] = None


class KPIResponse(BaseModel):
    kpis: list[KPICard]


# ── Generic ────────────────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


class SuccessResponse(BaseModel):
    message: str
    data: Optional[Any] = None
