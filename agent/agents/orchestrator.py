"""
Orchestrator Agent for Fractional Quest.

Routes requests to appropriate subagents based on context:
- If onboarding incomplete -> onboarding agent
- If asking about jobs -> job search agent
- If asking about coaching -> coaching agent
- General questions -> answer directly
"""

# Load environment variables FIRST before any LangChain imports
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from copilotkit import CopilotKitMiddleware

from state import AgentState
from tools.onboarding import (
    confirm_role_preference,
    confirm_trinity,
    confirm_experience,
    confirm_location,
    confirm_search_prefs,
    complete_onboarding,
)


# ============================================
# Orchestrator Tools
# ============================================

@tool
def get_onboarding_status(state: AgentState) -> dict:
    """
    Check the current onboarding status.
    Returns the current step and completion status.
    """
    return {
        "current_step": state.onboarding.current_step,
        "completed": state.onboarding.completed,
        "role_preference": state.onboarding.role_preference,
        "location": state.onboarding.location,
    }


@tool
def update_active_agent(agent_name: str, state: AgentState) -> dict:
    """
    Update which agent is currently active.
    This helps the UI show the right context.
    """
    state.active_agent = agent_name
    return {"active_agent": agent_name}


# ============================================
# System Prompt
# ============================================

ORCHESTRATOR_PROMPT = """You are the orchestrator for Fractional Quest, a platform helping fractional executives (CTO, CFO, CMO, etc.) find roles.

## Your Role
You route conversations to the appropriate specialist and maintain overall context. You are warm, professional, and helpful.

## Routing Rules

1. **Onboarding First**: If onboarding is not complete, guide the user through the onboarding flow. The 6 steps are:
   - intro: Greet and explain the platform
   - role_preference: What C-level role are they seeking?
   - trinity: Fractional, Interim, or Advisory preference?
   - experience: Years of experience and industries
   - location: Where are they based and remote preferences
   - search_prefs: Salary expectations and availability

2. **After Onboarding**:
   - Job questions → Help with job search
   - Coaching questions → Help connect with coaches
   - General questions → Answer directly

## Current Context

The user's current state is available in your context. Use it to:
- Know which onboarding step they're on
- Remember their preferences
- Personalize your responses

## Tone
- Professional but warm
- Concise but thorough
- Encouraging and supportive

Always acknowledge what you already know about the user rather than re-asking.
"""


# ============================================
# Create the Agent
# ============================================

# Combine all tools
ALL_TOOLS = [
    # Orchestrator tools
    get_onboarding_status,
    update_active_agent,
    # Onboarding tools (6 HITL tools)
    confirm_role_preference,
    confirm_trinity,
    confirm_experience,
    confirm_location,
    confirm_search_prefs,
    complete_onboarding,
]

agent = create_agent(
    model="google_genai:gemini-2.0-flash",
    tools=ALL_TOOLS,
    middleware=[CopilotKitMiddleware()],
    state_schema=AgentState,
    system_prompt=ORCHESTRATOR_PROMPT,
)

# Export the compiled graph
graph = agent
