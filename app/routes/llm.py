import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)
router = APIRouter()
llm_service = LLMService()

class LLMRequest(BaseModel):
    prompt: str = Field(..., description="The input prompt for the LLM")
    model: str = Field(default="gpt-4-turbo", description="The LLM model to use")
    parameters: Optional[Dict] = Field(
        default={"temperature": 0.7, "max_tokens": 1000},
        description="Additional parameters for the LLM"
    )

@router.post("/execute-llm")
async def execute_llm(request: LLMRequest):
    try:
        logger.info(f"Received LLM request with model: {request.model}")
        result = await llm_service.execute(
            prompt=request.prompt,
            model=request.model,
            parameters=request.parameters
        )
        logger.info("LLM request completed successfully")
        return {"result": result}
    except ValueError as e:
        logger.error(f"Error executing LLM request: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
