"""
FastAPI entrypoint for the Deep Agent backend.
Exposes the orchestrator agent via AG-UI protocol for CopilotKit.
"""

import os
import json
import logging
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from copilotkit import LangGraphAGUIAgent

from agents.orchestrator import graph

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("fractional_quest")

# Create FastAPI app
app = FastAPI(
    title="Fractional Quest Agent",
    description="AI-powered career assistant for fractional executives",
    version="0.1.0",
)

# Configure CORS - allow all origins for CopilotKit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Debug middleware to log all requests (without consuming body)
@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    logger.info(f">>> {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"<<< {request.method} {request.url.path} -> {response.status_code}")
    return response


# Health check endpoint
@app.get("/health")
async def health_check():
    google_key = os.getenv("GOOGLE_API_KEY", "NOT SET")
    return {
        "status": "healthy",
        "agent": "fractional_quest",
        "google_api_key_set": google_key != "NOT SET",
        "google_api_key_prefix": google_key[:10] + "..." if google_key != "NOT SET" else "N/A",
    }


# Debug endpoint to test agent directly
@app.get("/debug")
async def debug_info():
    return {
        "graph_type": str(type(graph)),
        "graph_nodes": list(graph.nodes.keys()) if hasattr(graph, 'nodes') else "N/A",
        "env_vars": {
            "GOOGLE_API_KEY": "set" if os.getenv("GOOGLE_API_KEY") else "NOT SET",
            "PORT": os.getenv("PORT", "8123"),
        },
    }


# Add the LangGraph AG-UI endpoint
logger.info("Registering AG-UI endpoint at /")
add_langgraph_fastapi_endpoint(
    app=app,
    agent=LangGraphAGUIAgent(
        name="fractional_quest",
        description="AI career assistant for fractional executives seeking CTO, CFO, CMO and other C-level roles.",
        graph=graph,
    ),
    path="/",
)
logger.info("AG-UI endpoint registered successfully")


def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8123"))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"Starting Fractional Quest Agent on http://{host}:{port}")
    logger.info(f"GOOGLE_API_KEY set: {bool(os.getenv('GOOGLE_API_KEY'))}")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
