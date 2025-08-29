from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import routers
from routers import auth, apartments, notifications, admins, rental_contracts
from background_jobs import start_scheduler, stop_scheduler
from database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()

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
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(admins.router, prefix="/api/v1")
app.include_router(rental_contracts.router, prefix="/api/v1")

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
