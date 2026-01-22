"""
State models for the Deep Agent.
Uses CopilotKitState as base for automatic frontend sync.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from copilotkit import CopilotKitState


# ============================================
# Onboarding State
# ============================================

OnboardingStep = Literal[
    "intro",           # Step 1: Introduction/greeting
    "role_preference", # Step 2: CTO, CFO, CMO, etc.
    "trinity",         # Step 3: Fractional/Interim/Advisory preference
    "experience",      # Step 4: Years of experience, industries
    "location",        # Step 5: Location and remote preferences
    "search_prefs",    # Step 6: Search preferences (salary, engagement type)
    "completed"        # Done with onboarding
]


class OnboardingState(BaseModel):
    """Tracks progress through the 6-step onboarding flow."""

    current_step: OnboardingStep = "intro"
    completed: bool = False

    # Step 2: Role preference
    role_preference: Optional[str] = None  # 'cto', 'cfo', 'cmo', 'coo', 'cro', etc.

    # Step 3: Trinity (engagement type preference)
    trinity: Optional[str] = None  # 'fractional', 'interim', 'advisory', or combination

    # Step 4: Experience
    years_experience: Optional[int] = None
    industries: List[str] = Field(default_factory=list)

    # Step 5: Location
    location: Optional[str] = None
    remote_preference: Optional[str] = None  # 'remote', 'hybrid', 'onsite', 'flexible'

    # Step 6: Search preferences
    target_compensation: Optional[str] = None
    availability: Optional[str] = None  # 'immediately', '2_weeks', '1_month', etc.


# ============================================
# User State
# ============================================

class UserState(BaseModel):
    """User identity and profile information."""

    id: Optional[str] = None  # User ID from auth/session
    email: Optional[str] = None
    name: Optional[str] = None

    # Profile completeness tracking
    profile_complete: bool = False


# ============================================
# Page Context
# ============================================

class PageContext(BaseModel):
    """Tracks which page the user is currently viewing."""

    current_page: str = "/"
    page_type: Optional[str] = None  # 'home', 'jobs', 'coaching', 'service', 'article'
    role_context: Optional[str] = None  # If on a role-specific page like /cto-services


# ============================================
# Job Search State
# ============================================

class JobSearchState(BaseModel):
    """State for job search and matching."""

    last_search_query: Optional[str] = None
    saved_jobs: List[str] = Field(default_factory=list)  # Job IDs
    liked_jobs: List[str] = Field(default_factory=list)
    applied_jobs: List[str] = Field(default_factory=list)


# ============================================
# Coaching State
# ============================================

class CoachingState(BaseModel):
    """State for executive coaching features."""

    interested_in_coaching: Optional[bool] = None
    coach_connected: bool = False
    scheduled_sessions: List[str] = Field(default_factory=list)


# ============================================
# Main Agent State
# ============================================

class AgentState(CopilotKitState):
    """
    Root state for the orchestrator agent.
    Extends CopilotKitState for automatic frontend synchronization.

    This state is shared bidirectionally:
    - Agent updates flow to frontend via CopilotKit
    - Frontend updates (via useCoAgent setState) flow to agent
    """

    # Core state objects
    user: UserState = Field(default_factory=UserState)
    onboarding: OnboardingState = Field(default_factory=OnboardingState)
    page_context: PageContext = Field(default_factory=PageContext)
    job_search: JobSearchState = Field(default_factory=JobSearchState)
    coaching: CoachingState = Field(default_factory=CoachingState)

    # Which subagent is currently active (for UI feedback)
    active_agent: Optional[str] = None  # 'orchestrator', 'onboarding', 'job_search', 'coaching'
