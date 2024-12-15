import logging
from fastapi import FastAPI
from app.routes import llm, workflow
from app.database import engine, Base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Beta Flow API",
    description="API for executing tasks using LLMs and managing workflows",
    version="1.0.0"
)

# Include routers
app.include_router(llm.router, prefix="/api/v1")
app.include_router(workflow.router, prefix="/api/v1")

@app.get("/health-check")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))  # Default to 8000 if not set
    uvicorn.run(app, host="0.0.0.0", port=port)
