"""
FastAPI Backend — AI Analytics Dashboard
Main application entry point with CORS, routes, and health check.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

from routers import data, analytics, charts

load_dotenv()

# ── App Setup ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Analytics Dashboard API",
    description="Backend API for the Agentic AI Analytics Dashboard",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ── CORS ───────────────────────────────────────────────────────────────────────
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(charts.router, prefix="/api/charts", tags=["Charts"])


# ── Health Check ───────────────────────────────────────────────────────────────
@app.get("/api/health", tags=["Health"])
async def health_check():
    return JSONResponse({
        "status": "healthy",
        "version": "1.0.0",
        "service": "AI Analytics Dashboard API"
    })


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "AI Analytics Dashboard API",
        "docs": "/docs",
        "health": "/api/health"
    }


# ── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
