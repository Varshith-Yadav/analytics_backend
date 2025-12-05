"""FastAPI application entry point"""
from fastapi import FastAPI
from app.core.database import init_db
from app.api.v1 import analytics
from app.api.v1 import import_routes

app = FastAPI(
    title="Multi-Domain Analytics Backend API",
    description="A FastAPI backend for serving analytics metrics across Sales/E-commerce, Food Delivery, and SaaS domains",
    version="2.0.0"
)

# Include API routers
app.include_router(analytics.router)
app.include_router(import_routes.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Multi-Domain Analytics Backend API",
        "version": "2.0.0",
        "supported_analytics_types": {
            "sales": "E-commerce / Sales Analytics",
            "food_delivery": "Food Delivery Analytics (Swiggy/Zomato style)",
            "saas": "SaaS Subscription Analytics (Stripe style)"
        },
        "endpoints": {
            "aggregations": "/api/v1/aggregate",
            "chart_data": "/api/v1/chart",
            "metrics_summary": "/api/v1/metrics/summary",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "analytics-backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
 