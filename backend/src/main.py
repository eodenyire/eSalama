"""Main FastAPI application"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import get_settings

# Import routes
from src.auth.routes import router as auth_router
from src.students.routes import router as students_router
from src.attendance.routes import router as attendance_router
from src.qr_verification.routes import router as qr_router
from src.location_tracking.routes import router as location_router
from src.notifications.routes import router as notifications_router
from src.reports.routes import router as reports_router
from src.users.routes import router as users_router
from src.audit_logs.routes import router as audit_logs_router
from src.streaming.routes import router as streaming_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    from config.database import engine, Base
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (if needed)


# Initialize FastAPI app
app = FastAPI(
    title="eSalama Schools API",
    description="Secure, real-time student tracking and communication system",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
api_prefix = f"/api/{settings.api_version}"
app.include_router(auth_router, prefix=api_prefix)
app.include_router(students_router, prefix=api_prefix)
app.include_router(attendance_router, prefix=api_prefix)
app.include_router(qr_router, prefix=api_prefix)
app.include_router(location_router, prefix=api_prefix)
app.include_router(notifications_router, prefix=api_prefix)
app.include_router(reports_router, prefix=api_prefix)
app.include_router(users_router, prefix=api_prefix)
app.include_router(audit_logs_router, prefix=api_prefix)
app.include_router(streaming_router, prefix=api_prefix)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to eSalama Schools API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
