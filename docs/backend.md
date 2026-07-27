# 🏗️ Backend — Module Documentation

> The backend is a **FastAPI** application exposing REST APIs for data ingestion, ML analytics, and chart data.  
> It is consumed by the React frontend and tested by the Tester Agent.

---

## Directory Structure

```
backend/
├── main.py              ← FastAPI app, CORS, router registration
├── routers/
│   ├── data.py          ← CSV upload, sample data, summary
│   ├── analytics.py     ← ML training, prediction, results
│   └── charts.py        ← Chart data for the frontend
├── models/
│   └── schemas.py       ← Pydantic request/response models
└── services/
    ├── data_service.py  ← In-memory data store + CSV parsing
    └── ml_service.py    ← scikit-learn ML training + prediction
```

---

## `main.py` — FastAPI Application

**What it does:**
- Creates the FastAPI app instance
- Registers CORS middleware (allows `localhost:5173` and `localhost:3000`)
- Mounts all three routers under `/api/`
- Exposes `/api/health` and `/` for status checks

**Start command:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Docs auto-generated at:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## `routers/data.py` — Data Endpoints

**Mount prefix:** `/api/data`

| Endpoint | Method | Description |
|---|---|---|
| `/api/data/upload` | POST | Upload a CSV file. Stores in memory. |
| `/api/data/sample` | GET | Returns first N rows of current dataset. `?rows=100` |
| `/api/data/summary` | GET | Statistical summary (mean, std, min, max per column) |
| `/api/data/reset` | DELETE | Clear dataset, revert to generated sample data |

**How data is stored:**  
Data lives in-memory via `services/data_service.py`'s `_dataframe_store` singleton.  
It resets when the server restarts. For persistent storage, extend `data_service.py` to write to disk.

---

## `routers/analytics.py` — ML Analytics Endpoints

**Mount prefix:** `/api/analytics`

| Endpoint | Method | Body | Description |
|---|---|---|---|
| `/api/analytics/train` | POST | `TrainRequest` | Train RF and/or LR on current dataset |
| `/api/analytics/results` | GET | — | List trained models and feature columns |
| `/api/analytics/predict` | POST | `PredictRequest` | Single prediction from trained model |
| `/api/analytics/columns` | GET | — | Available columns with type info |

**TrainRequest body example:**
```json
{
  "target_column": "target",
  "model_type": "random_forest",
  "n_estimators": 100,
  "test_size": 0.2
}
```

**model_type values:** `"random_forest"` | `"logistic_regression"` | `"both"`

---

## `routers/charts.py` — Chart Data Endpoints

**Mount prefix:** `/api/charts`

| Endpoint | Method | Params | Description |
|---|---|---|---|
| `/api/charts/kpi` | GET | — | 6 KPI summary cards |
| `/api/charts/bar` | GET | `column`, `metric` | Bar chart: avg metric per category |
| `/api/charts/scatter` | GET | `x`, `y`, `color` | Scatter plot (max 300 points) |
| `/api/charts/heatmap` | GET | — | Correlation matrix for all numeric columns |
| `/api/charts/distribution` | GET | `column` | 20-bin histogram for a numeric column |

All chart endpoints return **chart-ready JSON** that Recharts (frontend) can consume directly.

---

## `models/schemas.py` — Pydantic Models

Defines the **request/response contracts** for all API endpoints.

| Schema | Type | Used by |
|---|---|---|
| `TrainRequest` | Request | `POST /api/analytics/train` |
| `PredictRequest` | Request | `POST /api/analytics/predict` |
| `ModelMetrics` | Response | Nested inside `TrainResponse` |
| `TrainResponse` | Response | `POST /api/analytics/train` |
| `KPICard` | Response | Nested inside `KPIResponse` |
| `ChartDataResponse` | Response | All chart endpoints |
| `DataSummaryResponse` | Response | `GET /api/data/summary` |

---

## `services/data_service.py` — Data Layer

**Responsibilities:**
- Generate realistic sample employee data (500 rows, 14 columns)
- Parse uploaded CSV bytes into a Pandas DataFrame
- Provide a simple in-memory singleton store (`_dataframe_store`)
- Compute statistical summaries

**Sample data columns:** `employee_id`, `age`, `salary`, `experience_years`, `department`, `education`, `region`, `performance_score`, `projects_completed`, `hours_per_week`, `satisfaction_score`, `promoted`, `attrition`, `target`

**Key functions:**
| Function | Description |
|---|---|
| `generate_sample_data()` | Returns 500-row DataFrame with realistic HR data |
| `get_or_generate()` | Returns current df or generates sample if empty |
| `load_from_csv_bytes(bytes)` | Parses uploaded CSV |
| `set_dataframe(df)` | Store a new DataFrame in memory |
| `summarize(df)` | Returns statistical summary dict |

---

## `services/ml_service.py` — ML Layer

**Responsibilities:**
- Preprocess DataFrames (fill nulls, one-hot encode, scale)
- Train scikit-learn models (RandomForest, LogisticRegression)
- Compute accuracy, precision, recall, F1, confusion matrix, feature importance
- Store trained models in-memory for prediction

**Preprocessing pipeline:**
```
Raw DataFrame
    │
    ├── Fill missing values (mean for numeric, mode for categorical)
    ├── One-hot encode categorical columns
    ├── StandardScaler on numeric columns
    └── Stratified train/test split (80/20)
```

**Key functions:**
| Function | Description |
|---|---|
| `preprocess(df, target_col)` | Returns X_train, X_test, y_train, y_test |
| `train_models(df, target_col, model_type, ...)` | Train and evaluate models |
| `predict(features, model_type)` | Single prediction with probabilities |
| `_compute_metrics(model_name, y_test, y_pred, X)` | Returns full metrics dict |
