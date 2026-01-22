"""
Onboarding tools for the 6-step profile building process.

These are HITL (Human-in-the-Loop) tools that:
1. Present options to the user
2. Collect and validate their response
3. Update state and persist to database
4. Return state snapshot for frontend sync

The tools use LangGraph's interrupt() for HITL when needed.
"""

from typing import List, Optional
from langchain.tools import tool
from langgraph.types import interrupt

from state import AgentState


# ============================================
# Step 2: Role Preference
# ============================================

VALID_ROLES = [
    "cto",      # Chief Technology Officer
    "cfo",      # Chief Financial Officer
    "cmo",      # Chief Marketing Officer
    "coo",      # Chief Operating Officer
    "cro",      # Chief Revenue Officer
    "cpo",      # Chief Product Officer
    "chro",     # Chief Human Resources Officer
    "ciso",     # Chief Information Security Officer
    "other",    # Other C-level or executive role
]


@tool
def confirm_role_preference(role: str, state: AgentState) -> dict:
    """
    Confirm the user's primary executive role preference.

    Args:
        role: The role type (cto, cfo, cmo, coo, cro, cpo, chro, ciso, other)
        state: Current agent state

    Returns:
        Updated state with role preference set
    """
    role_lower = role.lower().strip()

    # Validate role
    if role_lower not in VALID_ROLES:
        return {
            "success": False,
            "error": f"Invalid role. Valid options: {', '.join(VALID_ROLES)}",
            "valid_roles": VALID_ROLES,
        }

    # Update state
    state.onboarding.role_preference = role_lower
    state.onboarding.current_step = "trinity"

    # TODO: Persist to Neon database
    # await save_profile_item(state.user.id, "role_preference", role_lower)

    return {
        "success": True,
        "message": f"Great! I've noted that you're looking for {role.upper()} roles.",
        "role_preference": role_lower,
        "next_step": "trinity",
        "state_snapshot": {
            "onboarding": state.onboarding.model_dump(),
        },
    }


# ============================================
# Step 3: Trinity (Engagement Type)
# ============================================

VALID_TRINITY = [
    "fractional",   # Part-time, ongoing engagement
    "interim",      # Full-time, temporary engagement
    "advisory",     # Strategic advisor role
    "all",          # Open to all types
]


@tool
def confirm_trinity(engagement_type: str, state: AgentState) -> dict:
    """
    Confirm the user's preferred engagement type (the "trinity").

    Args:
        engagement_type: fractional, interim, advisory, or all
        state: Current agent state

    Returns:
        Updated state with trinity preference set
    """
    engagement_lower = engagement_type.lower().strip()

    if engagement_lower not in VALID_TRINITY:
        return {
            "success": False,
            "error": f"Invalid engagement type. Valid options: {', '.join(VALID_TRINITY)}",
            "valid_types": VALID_TRINITY,
        }

    # Update state
    state.onboarding.trinity = engagement_lower
    state.onboarding.current_step = "experience"

    return {
        "success": True,
        "message": f"Perfect! You're interested in {engagement_lower} roles.",
        "trinity": engagement_lower,
        "next_step": "experience",
        "state_snapshot": {
            "onboarding": state.onboarding.model_dump(),
        },
    }


# ============================================
# Step 4: Experience
# ============================================

@tool
def confirm_experience(
    years: int,
    industries: List[str],
    state: AgentState
) -> dict:
    """
    Confirm the user's experience level and industries.

    Args:
        years: Years of executive experience
        industries: List of industries they have experience in
        state: Current agent state

    Returns:
        Updated state with experience information
    """
    if years < 0:
        return {
            "success": False,
            "error": "Years of experience must be a positive number",
        }

    # Update state
    state.onboarding.years_experience = years
    state.onboarding.industries = industries
    state.onboarding.current_step = "location"

    return {
        "success": True,
        "message": f"Excellent! {years} years of experience across {', '.join(industries)}.",
        "years_experience": years,
        "industries": industries,
        "next_step": "location",
        "state_snapshot": {
            "onboarding": state.onboarding.model_dump(),
        },
    }


# ============================================
# Step 5: Location
# ============================================

VALID_REMOTE_PREFS = [
    "remote",       # Fully remote only
    "hybrid",       # Mix of remote and onsite
    "onsite",       # In-person only
    "flexible",     # Open to any arrangement
]


@tool
def confirm_location(
    location: str,
    remote_preference: str,
    state: AgentState
) -> dict:
    """
    Confirm the user's location and remote work preferences.

    Args:
        location: City, region, or country
        remote_preference: remote, hybrid, onsite, or flexible
        state: Current agent state

    Returns:
        Updated state with location information
    """
    remote_lower = remote_preference.lower().strip()

    if remote_lower not in VALID_REMOTE_PREFS:
        return {
            "success": False,
            "error": f"Invalid remote preference. Valid options: {', '.join(VALID_REMOTE_PREFS)}",
            "valid_preferences": VALID_REMOTE_PREFS,
        }

    # Update state
    state.onboarding.location = location
    state.onboarding.remote_preference = remote_lower
    state.onboarding.current_step = "search_prefs"

    return {
        "success": True,
        "message": f"Got it! Based in {location} with {remote_lower} work preference.",
        "location": location,
        "remote_preference": remote_lower,
        "next_step": "search_prefs",
        "state_snapshot": {
            "onboarding": state.onboarding.model_dump(),
        },
    }


# ============================================
# Step 6: Search Preferences
# ============================================

@tool
def confirm_search_prefs(
    target_compensation: Optional[str],
    availability: str,
    state: AgentState
) -> dict:
    """
    Confirm the user's search preferences (compensation, availability).

    Args:
        target_compensation: Target compensation range (e.g., "$200-300k", "open")
        availability: When they can start (immediately, 2_weeks, 1_month, etc.)
        state: Current agent state

    Returns:
        Updated state with search preferences
    """
    # Update state
    state.onboarding.target_compensation = target_compensation
    state.onboarding.availability = availability
    state.onboarding.current_step = "completed"

    return {
        "success": True,
        "message": f"Perfect! You're looking for {target_compensation or 'competitive compensation'} "
                   f"and can start {availability.replace('_', ' ')}.",
        "target_compensation": target_compensation,
        "availability": availability,
        "next_step": "completed",
        "state_snapshot": {
            "onboarding": state.onboarding.model_dump(),
        },
    }


# ============================================
# Complete Onboarding
# ============================================

@tool
def complete_onboarding(state: AgentState) -> dict:
    """
    Mark onboarding as complete and summarize the user's profile.

    Args:
        state: Current agent state

    Returns:
        Summary of the completed profile
    """
    state.onboarding.completed = True
    state.onboarding.current_step = "completed"
    state.user.profile_complete = True

    profile_summary = {
        "role": state.onboarding.role_preference,
        "engagement_type": state.onboarding.trinity,
        "experience": {
            "years": state.onboarding.years_experience,
            "industries": state.onboarding.industries,
        },
        "location": {
            "base": state.onboarding.location,
            "remote_preference": state.onboarding.remote_preference,
        },
        "search_preferences": {
            "compensation": state.onboarding.target_compensation,
            "availability": state.onboarding.availability,
        },
    }

    return {
        "success": True,
        "message": "Your profile is complete! I can now help you find matching opportunities.",
        "profile_summary": profile_summary,
        "onboarding_completed": True,
        "state_snapshot": {
            "onboarding": state.onboarding.model_dump(),
            "user": state.user.model_dump(),
        },
    }
