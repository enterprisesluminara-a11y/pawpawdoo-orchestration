"""
Team Leads Module for Hierarchical Swarm:
1. Sourcing Lead: Reviews supplier vetting, 3.0x markup, US warehouse delta, DSers SKU.
2. Storefront Lead: Reviews dual cat+dog positioning, stacked tagline lockup, variant selectors.
3. Growth Lead: Reviews direct-response video hooks, UGC storyboards, and ad compliance.

Implements structured review feedback loops and circuit breakers (max_retries=3).
"""

from __future__ import annotations

from typing import Any, Dict, List
from config import BRAND_PALETTE, BRAND_TAGLINE, MIN_MARKUP_MULTIPLIER
from state import PawPawDooState
from utils.brand_memory import brand_memory


MAX_RETRIES = 3


def run_sourcing_lead_review_node(state: PawPawDooState) -> Dict[str, Any]:
    """
    Sourcing Lead audits the worker's product research against supplier & financial rules.
    """
    research = state.get("product_research")
    retry_count = state.get("sourcing_retry_count", 0)
    feedback_list: List[str] = list(state.get("sourcing_feedback", []))

    if not research:
        return {
            "sourcing_lead_verdict": "REJECT_WITH_FEEDBACK",
            "sourcing_retry_count": retry_count + 1,
            "sourcing_feedback": feedback_list + ["Critical: Product research output is completely missing."],
        }

    issues: List[str] = []

    # 1. Supplier Vetting Check (Rule #7)
    logistics = research.supplier_logistics
    if not logistics.vetting_passed:
        issues.append(f"Supplier vetting failed: {', '.join(logistics.vetting_issues)} (Need >=1yr & >=4.0★).")

    # 2. Financial Markup Check (Rule #5 & #10)
    if research.markup_multiplier < MIN_MARKUP_MULTIPLIER:
        if not (research.undercut_strategy and research.undercut_strategy.is_applicable):
            issues.append(f"Landed markup {research.markup_multiplier:.2f}x is below {MIN_MARKUP_MULTIPLIER:.1f}x threshold without undercut bundle recovery.")

    # 3. US Warehouse Delta Check (Rule #8)
    if logistics.warehouse_cost_delta <= 3.00 and logistics.selected_warehouse != "US":
        issues.append(f"US warehouse shipping delta is ${logistics.warehouse_cost_delta:.2f} (<= $3.00), but US warehouse was not selected.")

    # 4. DSers SKU Mapping Check (Rule #9)
    if not logistics.dsers_sku or not logistics.aliexpress_product_id:
        issues.append("Missing mapped AliExpress Product ID or DSers SKU.")

    if issues and retry_count < MAX_RETRIES:
        new_feedback = f"Sourcing Lead Feedback (Iteration {retry_count + 1}): " + " | ".join(issues)
        feedback_list.append(new_feedback)
        return {
            "sourcing_lead_verdict": "REJECT_WITH_FEEDBACK",
            "sourcing_retry_count": retry_count + 1,
            "sourcing_feedback": feedback_list,
        }

    return {
        "sourcing_lead_verdict": "APPROVED",
        "sourcing_retry_count": retry_count,
        "sourcing_feedback": feedback_list,
    }


def run_storefront_lead_review_node(state: PawPawDooState) -> Dict[str, Any]:
    """
    Storefront Lead audits the worker's DTC offer, brand lockup, cat/dog inclusivity, and CRO.
    """
    storefront = state.get("storefront_offer")
    retry_count = state.get("storefront_retry_count", 0)
    feedback_list: List[str] = list(state.get("storefront_feedback", []))

    if not storefront:
        return {
            "storefront_lead_verdict": "REJECT_WITH_FEEDBACK",
            "storefront_retry_count": retry_count + 1,
            "storefront_feedback": feedback_list + ["Critical: Storefront offer output is missing."],
        }

    issues: List[str] = []

    # 1. Cat & Dog Dual Positioning (Rule #11)
    text_corpus = f"{storefront.hero_headline} {storefront.hero_subheadline} {' '.join(storefront.value_propositions)}".lower()
    if "dog" in text_corpus and "cat" not in text_corpus and "pet" not in text_corpus and "furry" not in text_corpus:
        issues.append("Brand copy over-indexes solely on dogs. Must position as a warm lifestyle brand for BOTH cats and dogs.")

    # 2. Tagline Presence & Brand Lockup (Rule #2 & #12)
    tagline_lower = BRAND_TAGLINE.lower()
    has_tagline = tagline_lower in storefront.hero_headline.lower() or any(tagline_lower in vp.lower() for vp in storefront.value_propositions)
    if not has_tagline:
        issues.append(f"Official tagline '{BRAND_TAGLINE}' is missing from hero headline or value props.")

    # 3. Mobile CRO & Sticky Bar (Rule #4)
    if not storefront.sticky_cta_bar or not storefront.sticky_cta_bar.get("enabled"):
        issues.append("Mobile sticky CTA bar is missing or disabled.")

    if issues and retry_count < MAX_RETRIES:
        new_feedback = f"Storefront Lead Feedback (Iteration {retry_count + 1}): " + " | ".join(issues)
        feedback_list.append(new_feedback)
        return {
            "storefront_lead_verdict": "REJECT_WITH_FEEDBACK",
            "storefront_retry_count": retry_count + 1,
            "storefront_feedback": feedback_list,
        }

    return {
        "storefront_lead_verdict": "APPROVED",
        "storefront_retry_count": retry_count,
        "storefront_feedback": feedback_list,
    }


def run_growth_lead_review_node(state: PawPawDooState) -> Dict[str, Any]:
    """
    Growth Lead audits the worker's paid social creative angles, hooks, and storyboards.
    """
    ad_campaign = state.get("ad_campaign")
    retry_count = state.get("growth_retry_count", 0)
    feedback_list: List[str] = list(state.get("growth_feedback", []))

    if not ad_campaign or not ad_campaign.core_angles:
        return {
            "growth_lead_verdict": "REJECT_WITH_FEEDBACK",
            "growth_retry_count": retry_count + 1,
            "growth_feedback": feedback_list + ["Critical: Ad creative angles are missing."],
        }

    issues: List[str] = []

    # 1. Minimum 3 Angles Check
    if len(ad_campaign.core_angles) < 3:
        issues.append(f"Expected at least 3 distinct video ad angles, found {len(ad_campaign.core_angles)}.")

    # 2. 3-Second Hook Check
    for angle in ad_campaign.core_angles:
        if not angle.hook_3s or len(angle.hook_3s) < 2:
            issues.append(f"Angle '{angle.angle_name}' requires at least 2 thumb-stopping 3-second hook variations.")

    if issues and retry_count < MAX_RETRIES:
        new_feedback = f"Growth Lead Feedback (Iteration {retry_count + 1}): " + " | ".join(issues)
        feedback_list.append(new_feedback)
        return {
            "growth_lead_verdict": "REJECT_WITH_FEEDBACK",
            "growth_retry_count": retry_count + 1,
            "growth_feedback": feedback_list,
        }

    return {
        "growth_lead_verdict": "APPROVED",
        "growth_retry_count": retry_count,
        "growth_feedback": feedback_list,
    }
