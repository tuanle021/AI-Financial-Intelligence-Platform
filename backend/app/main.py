from fastapi import FastAPI

from app.core.config import settings
from app.api.routes.market import router as market_router
from app.api.routes.instruments import router as instruments_router


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(market_router)
app.include_router(instruments_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment
    }
