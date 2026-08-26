"""
LangGraph Multi-Agent Orchestrator for PawPawDoo.
Builds the state graph, manages sequential routing, and orchestrates the self-healing feedback loop.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Literal
from langgraph.graph import END, START, StateGraph

from agents.ad_strategist import run_ad_strategist_agent
from agents.gatekeeper_auditor import run_gatekeeper_auditor_agent
from agents.product_research import run_product_research_agent
from agents.storefront_architect import run_storefront_architect_agent
from state import PawPawDooState
from utils.export_doc import GoogleDocExporter

logger = logging.getLogger("pawpawdoo.graph")


def self_healing_corrector_node(state: PawPawDooState) -> Dict[str, Any]:
    """
    Self-healing node: extracts audit feedback, updates iteration count,
    and applies corrections to the state before re-running agent nodes.
    """
    current_iter = state.get("iteration_count", 0) + 1
    audit = state.get("audit_report")
    history = list(state.get("feedback_history", []))

    if audit:
        feedback_entry = f"Iteration {current_iter} Audit Rejection: {audit.detailed_feedback}"
        history.append(feedback_entry)

    logger.info(f"Self-healing loop triggered (Iteration {current_iter}). Applying corrections...")

    # Fix product request if markup was too low and not flagged as opportunity
    req = dict(state.get("product_request", {}))
    if audit and not audit.finance_markup_check and audit.status == "HARD_REJECT":
        base_item = float(req.get("base_item_cost", 14.50))
        # Self-heal target price to 3.5x markup over landed costs
        req["target_price"] = round((base_item + 8.00) * 3.5, 2)

    return {
        "iteration_count": current_iter,
        "feedback_history": history,
        "product_request": req,
    }


def finalize_draft_node(state: PawPawDooState) -> Dict[str, Any]:
    """
    Assembles the final human-readable DRAFT deliverable package and Google Doc export.
    """
    research = state.get("product_research")
    storefront = state.get("storefront_offer")
    ad_campaign = state.get("ad_campaign")
    audit = state.get("audit_report")

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
        "rules_appended": state.get("self_healing_rules_added", []),
    }

    return {"final_output": final_payload}


def route_after_audit(
    state: PawPawDooState,
) -> Literal["self_healing_corrector_node", "finalize_draft_node"]:
    """Conditional router determining if self-healing loop or finalization should run."""
    audit = state.get("audit_report")
    iterations = state.get("iteration_count", 0)
    max_iters = state.get("max_iterations", 3)

    if audit and audit.passed:
        logger.info(f"Audit passed with status: {audit.status}. Routing to finalize draft.")
        return "finalize_draft_node"

    if iterations < max_iters:
        logger.info(f"Audit rejected ({iterations}/{max_iters}). Routing to self-healing corrector.")
        return "self_healing_corrector_node"

    logger.warning("Max iterations reached. Routing to finalize draft with audit flags.")
    return "finalize_draft_node"


def build_pawpawdoo_graph() -> StateGraph:
    """Builds and compiles the complete PawPawDoo LangGraph."""
    workflow = StateGraph(PawPawDooState)

    # 1. Add agent and workflow nodes
    workflow.add_node("product_research", run_product_research_agent)
    workflow.add_node("storefront_architect", run_storefront_architect_agent)
    workflow.add_node("ad_strategist", run_ad_strategist_agent)
    workflow.add_node("gatekeeper_auditor", run_gatekeeper_auditor_agent)
    workflow.add_node("self_healing_corrector_node", self_healing_corrector_node)
    workflow.add_node("finalize_draft_node", finalize_draft_node)

    # 2. Add standard pipeline edges
    workflow.add_edge(START, "product_research")
    workflow.add_edge("product_research", "storefront_architect")
    workflow.add_edge("storefront_architect", "ad_strategist")
    workflow.add_edge("ad_strategist", "gatekeeper_auditor")

    # 3. Add conditional edge from Auditor (Pass/Opportunity -> Finalize, Fail -> Self-Heal)
    workflow.add_conditional_edges(
        "gatekeeper_auditor",
        route_after_audit,
        {
            "finalize_draft_node": "finalize_draft_node",
            "self_healing_corrector_node": "self_healing_corrector_node",
        },
    )

    # 4. Route self-healing back to research node
    workflow.add_edge("self_healing_corrector_node", "product_research")

    # 5. Finalize leads to END
    workflow.add_edge("finalize_draft_node", END)

    return workflow.compile()


# Compiled singleton graph
pawpawdoo_graph = build_pawpawdoo_graph()
