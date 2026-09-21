from fastapi import FastAPI
from app.api.traffic import router as traffic_router
from app.api.prediction import router as prediction_router


app = FastAPI(
    title="UrbanFlow AI",
    description="AI-Powered Predictive Traffic Intelligence & Emergency Green Corridor System",
    version="1.0.0"
)


app.include_router(traffic_router)
app.include_router(prediction_router)


@app.get("/")
def root():
    return {
        "project": "UrbanFlow AI",
        "status": "running",
        "message": "Predictive Traffic Intelligence System"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }