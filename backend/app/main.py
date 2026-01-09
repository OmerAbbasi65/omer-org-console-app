"""
FastAPI Application - Main Entry Point

Todo API - Phase 2 Level 1 (Core Features)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.db import create_db_and_tables
from app.api.v1 import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for application startup and shutdown.

    Startup:
        - Create database tables
        - Initialize connections

    Shutdown:
        - Close connections
    """
    # Startup
    print("🚀 Starting Todo API...")
    create_db_and_tables()
    print("✅ Database tables created")

    yield

    # Shutdown
    print("👋 Shutting down Todo API...")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Todo API - Phase 2 Level 1 (Core Features)",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(
    tasks.router,
    prefix=settings.API_V1_PREFIX,
    tags=["tasks"]
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Todo API - Phase 2 Level 1",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}
