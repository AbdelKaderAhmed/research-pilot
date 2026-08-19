import logging
from fastapi import FastAPI, HTTPException
from app.schemas.research import ResearchRequest, ResearchResponse
from app.services.research_service import generate_basic_research

logger = logging.getLogger("research_pilot")

app = FastAPI(
    title="ResearchPilot API",
    description="AI Research Agent Assistant",
    version="0.1.0"
)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

@app.post("/api/v1/research", response_model=ResearchResponse, tags=["Research"])
async def create_research(request: ResearchRequest):
    try:
        # Function returns a fully constructed ResearchResponse instance
        research_result = await generate_basic_research(
            topic=request.topic, 
            depth=request.depth
        )
        # Return the response directly without double-wrapping
        return research_result

    except Exception as e:
        logger.error(f"Endpoint failed: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Research generation failed: {str(e)}"
        )