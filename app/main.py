"""
Main FastAPI application for Azure Foundry AI Agent chat interface.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from pathlib import Path
import logging

from app.agent import AIAgent
from app.config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sof-IA, my Evaluator",
    description="Interface para interagir com a avaliadora Sof-IA (AI-102)",
    version="1.0.0"
)

# Initialize settings
settings = Settings()

# Initialize AI Agent
try:
    ai_agent = AIAgent(settings)
    logger.info("AI Agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize AI Agent: {e}")
    ai_agent = None

# Mount static files
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


# Pydantic models
class Message(BaseModel):
    """Chat message model with optional history"""
    content: str
    role: str = "user"
    history: Optional[list] = None  # Full conversation history


class ChatResponse(BaseModel):
    """Chat response model"""
    message: str
    success: bool
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    agent_ready: bool


# Routes
@app.get("/")
async def root():
    """Serve the main HTML page"""
    index_path = Path(__file__).parent.parent / "static" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Welcome to Azure Foundry AI Chat API"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    agent_ready = ai_agent is not None
    return HealthResponse(
        status="healthy",
        agent_ready=agent_ready
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: Message):
    """Chat endpoint - interact with AI agent"""
    
    if not ai_agent:
        raise HTTPException(
            status_code=503,
            detail="AI Agent is not initialized. Check server logs and environment variables."
        )
    
    if not message.content.strip():
        raise HTTPException(
            status_code=400,
            detail="Message content cannot be empty"
        )
    
    try:
        response = await ai_agent.process_message(
            user_message=message.content,
            conversation_history=message.history or []
        )
        return ChatResponse(
            message=response,
            success=True
        )
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return ChatResponse(
            message="",
            success=False,
            error=str(e)
        )


@app.get("/api/config")
async def get_config():
    """Get frontend configuration"""
    return {
        "app_name": "Sof-IA, my Evaluator",
        "version": "1.0.0",
        "agent_ready": ai_agent is not None
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
