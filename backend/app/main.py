from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.db.database import engine
from app.api.portfolio import router as portfolio_router

app = FastAPI(
    title="Investment Portfolio Analytics & Risk Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(portfolio_router)



@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "portfolio-platform"
    }

@app.get("/db-health")
def database_health():
    try:
        with engine.connect():
            return {
                "status": "healthy",
                "database": "connected"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": str(e)
        }
