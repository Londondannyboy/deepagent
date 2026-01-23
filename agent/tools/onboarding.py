"""
Onboarding tools for the 6-step profile building process.

These tools validate user input and return structured data.
State updates are handled by the graph's state management.
"""

from typing import List, Optional
from langchain_core.tools import tool


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
def confirm_role_preference(role: str) -> dict:
    """
    Confirm the user's primary executive role preference.
    Call this when the user tells you what role they're looking for.

    Args:
        role: The role type (cto, cfo, cmo, coo, cro, cpo, chro, ciso, other)

    Returns:
        Confirmation of the role preference
    """
    role_lower = role.lower().strip()

    if role_lower not in VALID_ROLES:
        return {
            "success": False,
            "error": f"Invalid role. Valid options: {', '.join(VALID_ROLES)}",
            "valid_roles": VALID_ROLES,
        }

    return {
        "success": True,
        "message": f"Role preference set to {role_lower.upper()}.",
        "role_preference": role_lower,
        "next_step": "trinity",
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
def confirm_trinity(engagement_type: str) -> dict:
    """
    Confirm the user's preferred engagement type.
    Call this when the user indicates their preference for fractional, interim, or advisory roles.

    Args:
        engagement_type: fractional, interim, advisory, or all

    Returns:
        Confirmation of the engagement type preference
    """
    engagement_lower = engagement_type.lower().strip()

    if engagement_lower not in VALID_TRINITY:
        return {
            "success": False,
            "error": f"Invalid engagement type. Valid options: {', '.join(VALID_TRINITY)}",
            "valid_types": VALID_TRINITY,
        }

    return {
        "success": True,
        "message": f"Engagement type set to {engagement_lower}.",
        "trinity": engagement_lower,
        "next_step": "experience",
    }


# ============================================
# Step 4: Experience
# ============================================

@tool
def confirm_experience(years: int, industries: List[str]) -> dict:
    """
    Confirm the user's experience level and industries.
    Call this when the user shares their years of experience and industry background.

    Args:
        years: Years of executive experience
        industries: List of industries they have experience in

    Returns:
        Confirmation of experience details
    """
    if years < 0:
        return {
            "success": False,
            "error": "Years of experience must be a positive number",
        }

    return {
        "success": True,
        "message": f"{years} years of experience across {', '.join(industries)}.",
        "years_experience": years,
        "industries": industries,
        "next_step": "location",
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
def confirm_location(location: str, remote_preference: str) -> dict:
    """
    Confirm the user's location and remote work preferences.
    Call this when the user shares where they are based and their work arrangement preference.

    Args:
        location: City, region, or country
        remote_preference: remote, hybrid, onsite, or flexible

    Returns:
        Confirmation of location details
    """
    remote_lower = remote_preference.lower().strip()

    if remote_lower not in VALID_REMOTE_PREFS:
        return {
            "success": False,
            "error": f"Invalid remote preference. Valid options: {', '.join(VALID_REMOTE_PREFS)}",
            "valid_preferences": VALID_REMOTE_PREFS,
        }

    return {
        "success": True,
        "message": f"Based in {location} with {remote_lower} work preference.",
        "location": location,
        "remote_preference": remote_lower,
        "next_step": "search_prefs",
    }


# ============================================
# Step 6: Search Preferences
# ============================================

@tool
def confirm_search_prefs(
    target_compensation: Optional[str],
    availability: str,
) -> dict:
    """
    Confirm the user's search preferences including compensation and availability.
    Call this when the user shares their salary expectations and when they can start.

    Args:
        target_compensation: Target compensation range (e.g., "$200-300k", "open")
        availability: When they can start (immediately, 2_weeks, 1_month, flexible)

    Returns:
        Confirmation of search preferences
    """
    return {
        "success": True,
        "message": f"Looking for {target_compensation or 'competitive compensation'}, "
                   f"available {availability.replace('_', ' ')}.",
        "target_compensation": target_compensation,
        "availability": availability,
        "next_step": "completed",
    }


# ============================================
# Complete Onboarding
# ============================================

@tool
def complete_onboarding() -> dict:
    """
    Mark onboarding as complete. Call this after all 6 steps have been completed
    and the user has confirmed their profile information.

    Returns:
        Confirmation that onboarding is complete
    """
    return {
        "success": True,
        "message": "Your profile is complete! I can now help you find matching opportunities.",
        "onboarding_completed": True,
    }
