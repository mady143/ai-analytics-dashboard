"""
ML Service — handles model training, evaluation, and prediction.
"""

import time
import numpy as np
import pandas as pd
from typing import Any, Optional
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

# In-memory model store
_models: dict = {}
_scaler: Optional[StandardScaler] = None
_feature_columns: list[str] = []
_label_encoder: Optional[LabelEncoder] = None


def preprocess(df: pd.DataFrame, target_col: str) -> tuple:
    """Preprocess dataframe: encode, scale, split."""
    global _scaler, _feature_columns, _label_encoder

    X = df.drop(columns=[target_col]).copy()
    y = df[target_col].copy()

    # Encode target if not numeric
    if y.dtype == object:
        _label_encoder = LabelEncoder()
        y = pd.Series(_label_encoder.fit_transform(y))

    # Fill missing values
    numeric_cols = X.select_dtypes(include=np.number).columns.tolist()
    cat_cols = X.select_dtypes(include="object").columns.tolist()

    for col in numeric_cols:
        X[col] = X[col].fillna(X[col].mean())
    for col in cat_cols:
        X[col] = X[col].fillna(X[col].mode()[0])

    # One-hot encode categoricals
    X = pd.get_dummies(X, drop_first=True)
    _feature_columns = X.columns.tolist()

    # Scale numeric columns
    _scaler = StandardScaler()
    scaled_cols = [c for c in X.columns if c in numeric_cols]
    if scaled_cols:
        X[scaled_cols] = _scaler.fit_transform(X[scaled_cols])

    # Safe stratified split
    class_counts = Counter(y)
    min_class = min(class_counts.values())
    stratify_y = y if min_class >= 2 else None

    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=stratify_y)


def _compute_metrics(model_name: str, y_test, y_pred, X: pd.DataFrame) -> dict:
    """Compute all evaluation metrics for a trained model."""
    avg = "weighted"
    cm = confusion_matrix(y_test, y_pred).tolist()
    report = classification_report(y_test, y_pred, output_dict=True)

    result = {
        "model_name": model_name,
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, average=avg, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, average=avg, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_test, y_pred, average=avg, zero_division=0)), 4),
        "confusion_matrix": cm,
        "classification_report": report,
        "feature_importance": None
    }

    # Feature importance for Random Forest
    if model_name == "Random Forest" and hasattr(_models.get("random_forest"), "feature_importances_"):
        model = _models["random_forest"]
        fi = dict(zip(X.columns.tolist(), model.feature_importances_.tolist()))
        # Top 15 features sorted by importance
        result["feature_importance"] = dict(
            sorted(fi.items(), key=lambda x: x[1], reverse=True)[:15]
        )

    return result


def train_models(
    df: pd.DataFrame,
    target_col: str,
    model_type: str = "random_forest",
    test_size: float = 0.2,
    n_estimators: int = 100,
    max_depth: Optional[int] = None,
    lr_max_iter: int = 1000
) -> dict:
    """Train one or both models and return metrics."""
    global _models

    start_time = time.time()
    X_train, X_test, y_train, y_test = preprocess(df, target_col)

    results = []
    models_to_train = []

    if model_type in ("random_forest", "both"):
        models_to_train.append("random_forest")
    if model_type in ("logistic_regression", "both"):
        models_to_train.append("logistic_regression")

    for m in models_to_train:
        if m == "random_forest":
            model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=42,
                n_jobs=-1
            )
            display_name = "Random Forest"
        else:
            model = LogisticRegression(
                max_iter=lr_max_iter,
                random_state=42,
                solver="lbfgs"
            )
            display_name = "Logistic Regression"

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        _models[m] = model

        metrics = _compute_metrics(display_name, y_test, y_pred, X_test)
        results.append(metrics)

    elapsed = round(time.time() - start_time, 2)
    return {
        "success": True,
        "message": f"Trained {len(results)} model(s) in {elapsed}s",
        "results": results,
        "training_time_seconds": elapsed
    }


def predict(features: dict, model_type: str = "random_forest") -> dict:
    """Make a single prediction using a trained model."""
    key = "random_forest" if model_type == "random_forest" else "logistic_regression"
    model = _models.get(key)

    if not model:
        return {"error": f"Model '{model_type}' not trained yet. Call /api/analytics/train first."}

    if not _feature_columns:
        return {"error": "No feature columns available. Please train a model first."}

    # Build feature vector
    input_df = pd.DataFrame([features])
    input_df = pd.get_dummies(input_df, drop_first=True)

    # Align columns with training features
    for col in _feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[_feature_columns]

    prediction = model.predict(input_df)[0]
    probabilities = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_df)[0].tolist()

    # Decode label if encoder was used
    if _label_encoder:
        prediction = _label_encoder.inverse_transform([prediction])[0]

    return {
        "prediction": str(prediction),
        "probability": probabilities,
        "model_used": model_type
    }
