"""
LangGraph Hierarchical Autonomous Multi-Agent Swarm Orchestrator for PawPawDoo.
Architecture:
1. Chief of Staff: Mission briefing, RAG context injection, and final executive sign-off.
2. Sourcing Lead & Worker: Supplier vetting, landed COGS, US warehouse delta, DSers SKU mapping.
3. Storefront Lead & Worker: DTC copy, cat+dog multi-pet positioning, vertical brand lockup, variant selectors.
4. Growth Lead & Worker: Direct-response paid social angles, viral hooks, and UGC storyboards.
5. Gatekeeper Auditor: 14-Rule compliance & undercut opportunity audit.
6. Feedback Loops & Circuit Breakers (max_retries=3 per sub-team).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Literal
from langgraph.graph import END, START, StateGraph

from agents.ad_strategist import run_ad_strategist_agent
from agents.chief_of_staff import run_chief_of_staff_briefing_node, run_chief_of_staff_final_signoff_node
from agents.gatekeeper_auditor import run_gatekeeper_auditor_agent
from agents.product_research import run_product_research_agent
from agents.storefront_architect import run_storefront_architect_agent
from agents.team_leads import (
    MAX_RETRIES,
    run_growth_lead_review_node,
    run_sourcing_lead_review_node,
    run_storefront_lead_review_node,
)
from state import PawPawDooState
from utils.export_doc import GoogleDocExporter

logger = logging.getLogger("pawpawdoo.graph")


# --- Conditional Routing Functions ---

def route_sourcing_lead(
    state: PawPawDooState,
) -> Literal["sourcing_worker", "storefront_worker"]:
    """Routes back to sourcing worker on rejection (up to max_retries), or advances to storefront worker."""
    verdict = state.get("sourcing_lead_verdict", "APPROVED")
    retry_count = state.get("sourcing_retry_count", 0)

    if verdict == "REJECT_WITH_FEEDBACK" and retry_count < MAX_RETRIES:
        logger.warning(f"Sourcing Lead requested rework (Attempt {retry_count}/{MAX_RETRIES}). Routing back to Sourcing Worker.")
        return "sourcing_worker"

    logger.info("Sourcing Lead APPROVED deliverable. Routing to Storefront Worker.")
    return "storefront_worker"


def route_storefront_lead(
    state: PawPawDooState,
) -> Literal["storefront_worker", "growth_worker"]:
    """Routes back to storefront worker on rejection (up to max_retries), or advances to growth worker."""
    verdict = state.get("storefront_lead_verdict", "APPROVED")
    retry_count = state.get("storefront_retry_count", 0)

    if verdict == "REJECT_WITH_FEEDBACK" and retry_count < MAX_RETRIES:
        logger.warning(f"Storefront Lead requested rework (Attempt {retry_count}/{MAX_RETRIES}). Routing back to Storefront Worker.")
        return "storefront_worker"

    logger.info("Storefront Lead APPROVED deliverable. Routing to Growth Worker.")
    return "growth_worker"


def route_growth_lead(
    state: PawPawDooState,
) -> Literal["growth_worker", "gatekeeper_auditor"]:
    """Routes back to growth worker on rejection (up to max_retries), or advances to Gatekeeper Auditor."""
    verdict = state.get("growth_lead_verdict", "APPROVED")
    retry_count = state.get("growth_retry_count", 0)

    if verdict == "REJECT_WITH_FEEDBACK" and retry_count < MAX_RETRIES:
        logger.warning(f"Growth Lead requested rework (Attempt {retry_count}/{MAX_RETRIES}). Routing back to Growth Worker.")
        return "growth_worker"

    logger.info("Growth Lead APPROVED deliverable. Routing to Gatekeeper Auditor.")
    return "gatekeeper_auditor"


def route_after_audit(
    state: PawPawDooState,
) -> Literal["self_healing_corrector_node", "chief_of_staff_final"]:
    """Conditional router determining if global self-healing loop or final signoff should run."""
    audit = state.get("audit_report")
    iterations = state.get("iteration_count", 0)
    max_iters = state.get("max_iterations", 3)

    if audit and audit.passed:
        logger.info(f"Gatekeeper Audit passed ({audit.status}). Routing to Chief of Staff Final Sign-Off.")
        return "chief_of_staff_final"

    if iterations < max_iters:
        logger.warning(f"Audit rejected ({iterations}/{max_iters}). Routing to Self-Healing Corrector.")
        return "self_healing_corrector_node"

    logger.warning("Max global iterations reached. Routing to Chief of Staff Final Sign-Off with audit flags.")
    return "chief_of_staff_final"


# --- Workflow Nodes ---

def self_healing_corrector_node(state: PawPawDooState) -> Dict[str, Any]:
    """Applies global corrections from Gatekeeper audit before re-entering swarm workflow."""
    current_iter = state.get("iteration_count", 0) + 1
    audit = state.get("audit_report")
    history = list(state.get("feedback_history", []))

    if audit:
        history.append(f"Global Iteration {current_iter} Rejection: {audit.detailed_feedback}")

    logger.info(f"Global Self-Healing Loop (Iteration {current_iter}). Applying corrections...")

    req = dict(state.get("product_request", {}))
    if audit and not audit.finance_markup_check and audit.status == "HARD_REJECT":
        base_item = float(req.get("base_item_cost", 14.50))
        req["target_price"] = round((base_item + 8.00) * 3.5, 2)

    return {
        "iteration_count": current_iter,
        "feedback_history": history,
        "product_request": req,
    }


def finalize_draft_node(state: PawPawDooState) -> Dict[str, Any]:
    """Assembles the final DRAFT deliverable package, exports Google Doc, and syncs draft to Shopify."""
    research = state.get("product_research")
    storefront = state.get("storefront_offer")
    ad_campaign = state.get("ad_campaign")
    audit = state.get("audit_report")
    chief_verdict = state.get("chief_of_staff_verdict")

    # Export Google Doc Blueprint Markdown
    doc_path = Path(__file__).parent / "output_google_doc_blueprint.md"
    GoogleDocExporter.export_to_file(state, doc_path)

    # Push to Shopify Store as Draft (Rule #3 compliant)
    shopify_result = None
    try:
        from adapters.shopify_adapter import ShopifyAdapter
        adapter = ShopifyAdapter()
        if audit and audit.passed:
            shopify_result = adapter.push_approved_draft_product(state)
            if shopify_result.get("success"):
                logger.info(f"Shopify draft created successfully: ID {shopify_result.get('product_id')}")
            else:
                logger.warning(f"Shopify draft creation note: {shopify_result.get('error')}")
    except Exception as e:
        logger.warning(f"Shopify draft sync skipped or failed: {e}")

    final_payload = {
        "mode": "DRAFT_REVIEW_ONLY",
        "live_publishing_enabled": False,
        "chief_of_staff": chief_verdict,
        "team_leads": {
            "sourcing_lead": state.get("sourcing_lead_verdict"),
            "storefront_lead": state.get("storefront_lead_verdict"),
            "growth_lead": state.get("growth_lead_verdict"),
        },
        "audit_summary": {
            "status": audit.status if audit else "UNKNOWN",
            "status_icon": audit.status_icon if audit else "❓",
            "passed": audit.passed if audit else False,
            "overall_score": audit.overall_score if audit else 0,
            "violations": [v.model_dump() for v in audit.violations] if audit else [],
            "undercut_opportunity": audit.undercut_opportunity_report,
        },
        "product_research": research.model_dump() if research else None,
        "storefront_offer": storefront.model_dump() if storefront else None,
        "ad_campaign": ad_campaign.model_dump() if ad_campaign else None,
        "shopify_draft": shopify_result,
        "google_doc_export_path": str(doc_path),
        "self_healing_iterations": state.get("iteration_count", 0),
    }

    return {"final_output": final_payload}


# --- Swarm Graph Builder ---

def build_pawpawdoo_graph() -> StateGraph:
    """Builds and compiles the Hierarchical Autonomous Multi-Agent Swarm LangGraph."""
    workflow = StateGraph(PawPawDooState)

    # 1. Executive & Worker Nodes
    workflow.add_node("chief_of_staff_briefing", run_chief_of_staff_briefing_node)
    
    # Sub-Team 1: Sourcing
    workflow.add_node("sourcing_worker", run_product_research_agent)
    workflow.add_node("sourcing_lead_review", run_sourcing_lead_review_node)
    
    # Sub-Team 2: Storefront
    workflow.add_node("storefront_worker", run_storefront_architect_agent)
    workflow.add_node("storefront_lead_review", run_storefront_lead_review_node)
    
    # Sub-Team 3: Growth & Creative
    workflow.add_node("growth_worker", run_ad_strategist_agent)
    workflow.add_node("growth_lead_review", run_growth_lead_review_node)

    # Executive Auditor & Final Sign-Off
    workflow.add_node("gatekeeper_auditor", run_gatekeeper_auditor_agent)
    workflow.add_node("chief_of_staff_final", run_chief_of_staff_final_signoff_node)
    workflow.add_node("self_healing_corrector_node", self_healing_corrector_node)
    workflow.add_node("finalize_draft_node", finalize_draft_node)

    # 2. Executive Delegation
    workflow.add_edge(START, "chief_of_staff_briefing")
    workflow.add_edge("chief_of_staff_briefing", "sourcing_worker")

    # 3. Sourcing Sub-Team Review Loop
    workflow.add_edge("sourcing_worker", "sourcing_lead_review")
    workflow.add_conditional_edges(
        "sourcing_lead_review",
        route_sourcing_lead,
        {
            "sourcing_worker": "sourcing_worker",
            "storefront_worker": "storefront_worker",
        },
    )

    # 4. Storefront Sub-Team Review Loop
    workflow.add_edge("storefront_worker", "storefront_lead_review")
    workflow.add_conditional_edges(
        "storefront_lead_review",
        route_storefront_lead,
        {
            "storefront_worker": "storefront_worker",
            "growth_worker": "growth_worker",
        },
    )

    # 5. Growth Sub-Team Review Loop
    workflow.add_edge("growth_worker", "growth_lead_review")
    workflow.add_conditional_edges(
        "growth_lead_review",
        route_growth_lead,
        {
            "growth_worker": "growth_worker",
            "gatekeeper_auditor": "gatekeeper_auditor",
        },
    )

    # 6. Global Gatekeeper Audit & Chief of Staff Sign-Off
    workflow.add_conditional_edges(
        "gatekeeper_auditor",
        route_after_audit,
        {
            "chief_of_staff_final": "chief_of_staff_final",
            "self_healing_corrector_node": "self_healing_corrector_node",
        },
    )

    workflow.add_edge("self_healing_corrector_node", "sourcing_worker")
    workflow.add_edge("chief_of_staff_final", "finalize_draft_node")
    workflow.add_edge("finalize_draft_node", END)

    return workflow.compile()


# Compiled singleton graph
pawpawdoo_graph = build_pawpawdoo_graph()
