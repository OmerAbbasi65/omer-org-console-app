"""FastAPI application instance with CORS middleware and health check."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.api.tasks import router as tasks_router

app = FastAPI(
    title="Todo API",
    description="Phase 2 Full-Stack Todo Web Application API",
    version="0.1.0",
)

# CORS middleware - use configured origins from settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # Use origins from config/env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(tasks_router, prefix=settings.api_v1_prefix)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Todo API",
        "version": "0.1.0",
        "docs": "/docs",
    }
