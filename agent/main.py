"""
FastAPI entrypoint for the Deep Agent backend.
Exposes the orchestrator agent via AG-UI protocol for CopilotKit.
"""

import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from copilotkit import LangGraphAGUIAgent

from agents.orchestrator import graph

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Fractional Quest Agent",
    description="AI-powered career assistant for fractional executives",
    version="0.1.0",
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        os.getenv("FRONTEND_URL", ""),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent": "fractional_quest"}


# Add the LangGraph AG-UI endpoint
add_langgraph_fastapi_endpoint(
    app=app,
    agent=LangGraphAGUIAgent(
        name="fractional_quest",
        description="AI career assistant for fractional executives seeking CTO, CFO, CMO and other C-level roles.",
        graph=graph,
    ),
    path="/",
)


def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8123"))
    host = os.getenv("HOST", "0.0.0.0")

    print(f"Starting Fractional Quest Agent on http://{host}:{port}")
    print("AG-UI endpoint available at /")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
    )


if __name__ == "__main__":
    main()
