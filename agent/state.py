"""
State models for the Deep Agent.
Uses CopilotKitState (TypedDict) as base for automatic frontend sync.
"""

from typing import List, Optional
from typing_extensions import TypedDict
from copilotkit import CopilotKitState


# ============================================
# Onboarding State
# ============================================

class OnboardingState(TypedDict, total=False):
    """Tracks progress through the 6-step onboarding flow."""
    current_step: str  # intro, role_preference, trinity, experience, location, search_prefs, completed
    completed: bool
    role_preference: Optional[str]  # cto, cfo, cmo, coo, cro, etc.
    trinity: Optional[str]  # fractional, interim, advisory, all
    years_experience: Optional[int]
    industries: List[str]
    location: Optional[str]
    remote_preference: Optional[str]  # remote, hybrid, onsite, flexible
    target_compensation: Optional[str]
    availability: Optional[str]  # immediately, 2_weeks, 1_month, etc.


# ============================================
# User State
# ============================================

class UserState(TypedDict, total=False):
    """User identity and profile information."""
    id: Optional[str]
    email: Optional[str]
    name: Optional[str]
    profile_complete: bool


# ============================================
# Page Context
# ============================================

class PageContext(TypedDict, total=False):
    """Tracks which page the user is currently viewing."""
    current_page: str
    page_type: Optional[str]  # home, jobs, coaching, service, article
    role_context: Optional[str]


# ============================================
# Main Agent State
# ============================================

class AgentState(CopilotKitState, total=False):
    """
    Root state for the orchestrator agent.
    Extends CopilotKitState for automatic frontend synchronization.

    This state is shared bidirectionally:
    - Agent updates flow to frontend via CopilotKit
    - Frontend updates (via useCoAgent setState) flow to agent
    """
    user: UserState
    onboarding: OnboardingState
    page_context: PageContext
    active_agent: Optional[str]
