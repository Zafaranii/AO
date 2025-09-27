from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import routers
from routers import auth, apartments, admins, rental_contracts
from routers import uploads as uploads_router
from background_jobs import start_scheduler, stop_scheduler
from database import engine, Base

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Create all database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

# Create database tables on startup
create_tables()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting AO API server...")
    try:
        # Ensure tables are created on every startup
        create_tables()
        start_scheduler()
        logger.info("Server started successfully")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise
    yield
    # Shutdown
    logger.info("Shutting down server...")
    stop_scheduler()
    logger.info("Server shutdown complete")

app = FastAPI(
    title="AO API",
    description="A FastAPI application for AO",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(apartments.router, prefix="/api/v1")
app.include_router(admins.router, prefix="/api/v1")
app.include_router(rental_contracts.router, prefix="/api/v1")
app.include_router(uploads_router.router, prefix="/api/v1")

# Serve uploaded files only when using local storage
storage_backend = os.getenv("STORAGE_BACKEND", "local").strip().lower()
if storage_backend == "local":
    uploads_dir = os.getenv("UPLOADS_DIR", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

@app.get("/")
async def root():
    return {
        "message": "Welcome to AO",
        "documentation": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "real-estate-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
