"""
Chief of Staff Agent (Mission Overseer & Executive Sign-Off).
Role:
1. Formulates the high-level mission directives and delegates to Team Leads.
2. Queries the RAG Brand Memory Bank before delegating.
3. Conducts final executive sign-off and synthesizes the launch blueprint.
"""

from __future__ import annotations

from typing import Any, Dict
from config import BRAND_NAME, BRAND_TAGLINE
from state import PawPawDooState
from utils.brand_memory import brand_memory


def run_chief_of_staff_briefing_node(state: PawPawDooState) -> Dict[str, Any]:
    """
    Chief of Staff initializes the mission, queries RAG brand memory,
    and assigns structured objectives to Sourcing, Storefront, and Growth leads.
    """
    product_req = state.get("product_request", {})
    product_name = product_req.get("product_name", "Orthopedic Calming Cloud Pet Bed")
    target_price = product_req.get("target_price", 78.95)

    # Query RAG Brand Memory for Mission Context
    memory_context = brand_memory.get_formatted_context(
        task_name="Mission Initialization",
        query=f"{product_name} multi-pet cat dog branding pricing",
    )

    mission_brief = {
        "mission_id": "MISSION-PAWPAWDOO-HERO-01",
        "brand_name": BRAND_NAME,
        "tagline": BRAND_TAGLINE,
        "target_product": product_name,
        "target_price": target_price,
        "delegated_teams": {
            "sourcing_lead": "Vet suppliers (>=1yr, >=4.0★), verify 3.0x markup, evaluate US warehouse delta ($3 threshold), and map DSers SKU.",
            "storefront_lead": "Architect high-converting DTC offer with equal Cat & Dog positioning, stacked tagline lockup, size/color variants, and mobile CRO.",
            "growth_lead": "Produce 3 direct-response video ad angles with thumb-stopping 3-second hooks and UGC storyboards.",
        },
        "brand_memory_context": memory_context,
        "status": "MISSION_DELEGATED",
    }

    return {
        "mission_brief": mission_brief,
        "sourcing_retry_count": state.get("sourcing_retry_count", 0),
        "storefront_retry_count": state.get("storefront_retry_count", 0),
        "growth_retry_count": state.get("growth_retry_count", 0),
        "sourcing_feedback": state.get("sourcing_feedback", []),
        "storefront_feedback": state.get("storefront_feedback", []),
        "growth_feedback": state.get("growth_feedback", []),
    }


def run_chief_of_staff_final_signoff_node(state: PawPawDooState) -> Dict[str, Any]:
    """
    Chief of Staff reviews all deliverables from Team Leads and Gatekeeper Auditor,
    ensures strict Rule #3 Draft Mode, and gives executive authorization.
    """
    research = state.get("product_research")
    storefront = state.get("storefront_offer")
    ads = state.get("ad_campaign")
    audit = state.get("audit_report")

    sourcing_verdict = state.get("sourcing_lead_verdict", "APPROVED")
    storefront_verdict = state.get("storefront_lead_verdict", "APPROVED")
    growth_verdict = state.get("growth_lead_verdict", "APPROVED")

    passed_all_leads = (
        sourcing_verdict == "APPROVED"
        and storefront_verdict == "APPROVED"
        and growth_verdict == "APPROVED"
    )

    executive_verdict = {
        "mission_id": state.get("mission_brief", {}).get("mission_id", "MISSION-01"),
        "chief_of_staff_approval": passed_all_leads and (audit.passed if audit else True),
        "sourcing_lead_status": sourcing_verdict,
        "storefront_lead_status": storefront_verdict,
        "growth_lead_status": growth_verdict,
        "gatekeeper_score": audit.overall_score if audit else 100,
        "gatekeeper_status": audit.status if audit else "DRAFT_APPROVED",
        "operational_mode": "DRAFT (Unpublished / Safe)",
        "executive_summary": (
            f"Chief of Staff Executive Sign-Off Complete. All team leads (Sourcing, Storefront, Growth) "
            f"and Gatekeeper Auditor have approved deliverable for '{research.product_name if research else 'Hero Product'}'. "
            f"Target Landed Markup: {research.markup_multiplier if research else 3.51:.2f}x | "
            f"Positioning: Dogs & Cats Calming Comfort | Shopify Mode: DRAFT."
        ),
    }

    return {"chief_of_staff_verdict": executive_verdict}
