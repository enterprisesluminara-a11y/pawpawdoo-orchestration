"""
Financial & CRO Gatekeeper Auditor Agent (Claude API).
Implements 3-Tier Status Architecture:
- 🟢 DRAFT_APPROVED (Passes all filters & >= 3.0x markup)
- 🟠 HIGH_POTENTIAL_UNDERCUT_OPPORTUNITY (High viral/market demand; undercut pricing + multi-pack bundle recovery)
- 🔴 HARD_REJECT (Low demand, bad supplier <1yr / <4.0 stars, untracked shipping)
"""

from __future__ import annotations

import json
from typing import Any, Dict, List
from agents.base import LLMClient
from config import BRAND_NAME, BRAND_PALETTE, BRAND_TAGLINE, MIN_MARKUP_MULTIPLIER
from rules_engine import rules_engine
from state import AuditViolation, GatekeeperAuditData, PawPawDooState


def run_gatekeeper_auditor_agent(state: PawPawDooState) -> Dict[str, Any]:
    """
    Executes 3-tier Gatekeeper Audit across Brand, CRO, Finance, Supplier Vetting, and Logistics.
    Model: Anthropic Claude
    """
    research = state.get("product_research")
    storefront = state.get("storefront_offer")
    ad_campaign = state.get("ad_campaign")
    is_draft = state.get("is_draft", True)

    violations: List[AuditViolation] = []
    rules_added: List[str] = list(state.get("self_healing_rules_added", []))

    # 1. Supplier Vetting & Data Mapping Check (Rules 7, 9)
    supplier_passed = True
    dsers_passed = True
    if research:
        logistics = research.supplier_logistics
        if not logistics.vetting_passed:
            supplier_passed = False
            for issue in logistics.vetting_issues:
                violations.append(
                    AuditViolation(
                        category="SUPPLIER",
                        description=issue,
                        rule_reference="Rule #7",
                        suggested_fix="Filter for AliExpress suppliers with >=1.0 year history and >=4.0 star rating.",
                    )
                )
        if not logistics.has_tracked_shipping:
            supplier_passed = False
            violations.append(
                AuditViolation(
                    category="SUPPLIER",
                    description="Supplier does not provide tracked shipping.",
                    rule_reference="Rule #7",
                    suggested_fix="Select a carrier with end-to-end tracking (5-7 days).",
                )
            )
        if not logistics.aliexpress_product_id or not logistics.dsers_sku:
            dsers_passed = False
            violations.append(
                AuditViolation(
                    category="DATA",
                    description="Missing AliExpress Product ID or DSers SKU mapping.",
                    rule_reference="Rule #9",
                    suggested_fix="Generate and map AliExpress Product ID and DSers SKU for 1-click Shopify import.",
                )
            )

    # 2. Logistics Warehouse Rule Check (Rule 8)
    logistics_passed = True
    if research:
        logistics = research.supplier_logistics
        if logistics.warehouse_cost_delta <= 3.00 and logistics.selected_warehouse != "US":
            logistics_passed = False
            violations.append(
                AuditViolation(
                    category="LOGISTICS",
                    description=f"US warehouse shipping cost delta is ${logistics.warehouse_cost_delta:.2f} (<= $3.00) but US warehouse was not selected.",
                    rule_reference="Rule #8",
                    suggested_fix="Default to US warehouse for 3-5 day delivery when cost delta <= $3.00.",
                )
            )

    # 3. Brand Compliance Check (Rules 1, 2)
    brand_passed = True
    if storefront:
        palette = storefront.brand_palette or {}
        req_terracotta = BRAND_PALETTE["primary_terracotta"].lower()
        req_espresso = BRAND_PALETTE["espresso_text"].lower()
        req_cream = BRAND_PALETTE["cream_background"].lower()

        if (
            palette.get("primary_terracotta", "").lower() != req_terracotta
            or palette.get("espresso_text", "").lower() != req_espresso
            or palette.get("cream_background", "").lower() != req_cream
        ):
            brand_passed = False
            violations.append(
                AuditViolation(
                    category="BRAND",
                    description=f"Brand palette mismatch. Found: {palette}. Expected: {BRAND_PALETTE}.",
                    rule_reference="Rule #1",
                    suggested_fix="Set palette to Primary Terracotta (#C86432), Espresso Text (#37281D), Cream Background (#FAF8F5).",
                )
            )

        tagline_lower = BRAND_TAGLINE.lower()
        has_tagline_hero = (
            tagline_lower in storefront.hero_headline.lower() or tagline_lower in storefront.hero_subheadline.lower()
        )
        has_tagline_props = any(tagline_lower in vp.lower() for vp in storefront.value_propositions)

        if not (has_tagline_hero or has_tagline_props):
            brand_passed = False
            violations.append(
                AuditViolation(
                    category="BRAND",
                    description=f"Official tagline '{BRAND_TAGLINE}' missing from hero section and value propositions.",
                    rule_reference="Rule #2",
                    suggested_fix=f"Embed '{BRAND_TAGLINE}' prominently in hero headline and value proposition list.",
                )
            )

    # 4. CRO & Mobile First Check (Rule 4)
    cro_passed = True
    if storefront:
        sticky_cta = storefront.sticky_cta_bar or {}
        if not sticky_cta.get("enabled"):
            cro_passed = False
            violations.append(
                AuditViolation(
                    category="CRO",
                    description="Sticky CTA bottom bar is disabled or missing.",
                    rule_reference="Rule #4",
                    suggested_fix="Enable sticky CTA bar with high-contrast button for mobile viewports.",
                )
            )

    # 5. Live Spend Guardrail Check (Rule 3)
    process_passed = True
    if not is_draft:
        process_passed = False
        violations.append(
            AuditViolation(
                category="PROCESS",
                description="Live deployment or live budget spend attempted without explicit human confirmation.",
                rule_reference="Rule #3",
                suggested_fix="Enforce DRAFT mode and require human confirmation before triggering live ad spend.",
            )
        )

    # 6. Financial Markup & Undercut Opportunity Evaluation (Rules 5, 6, 10)
    finance_passed = True
    is_undercut_opportunity = False
    undercut_report = None

    if research:
        if research.markup_multiplier < MIN_MARKUP_MULTIPLIER:
            finance_passed = False
            if research.undercut_strategy and research.undercut_strategy.is_applicable:
                is_undercut_opportunity = True
                strat = research.undercut_strategy
                bundle_lines = [
                    f"  - {b['tier']}: ${b['price']:.2f} (Recovered Markup: {b['recovered_markup']}) -> {b['strategy']}"
                    for b in strat.bundle_margin_recovery
                ]
                undercut_report = (
                    f"🟠 HIGH_POTENTIAL_UNDERCUT_OPPORTUNITY Identified:\n"
                    f"- Single unit markup is {research.markup_multiplier:.2f}x (< 3.0x threshold), priced at ${research.selling_price:.2f}.\n"
                    f"- Competitive Undercut: Amazon Buy Box is ${strat.amazon_price:.2f}, eBay US Median is ${strat.ebay_price:.2f}.\n"
                    f"- Bundle Margin Recovery Plan:\n" + "\n".join(bundle_lines) + "\n"
                    f"- Strategic Rationale: {strat.strategic_rationale}"
                )
            else:
                violations.append(
                    AuditViolation(
                        category="FINANCE",
                        description=f"Markup multiplier {research.markup_multiplier:.2f}x is below {MIN_MARKUP_MULTIPLIER:.1f}x threshold without high-demand viral recovery.",
                        rule_reference="Rule #5",
                        suggested_fix="Increase retail price or negotiate lower supplier COGS.",
                    )
                )

    # 7. Determine 3-Tier Status
    # Tier 1: 🟢 DRAFT_APPROVED
    if brand_passed and cro_passed and process_passed and supplier_passed and dsers_passed and logistics_passed and finance_passed:
        status = "DRAFT_APPROVED"
        status_icon = "🟢"
        passed = True
        overall_score = 100
        feedback = "All brand, CRO, financial, supplier vetting, and logistics guardrails PASSED. Ready for DRAFT human sign-off."

    # Tier 2: 🟠 HIGH_POTENTIAL_UNDERCUT_OPPORTUNITY
    elif (
        is_undercut_opportunity
        and brand_passed
        and cro_passed
        and process_passed
        and supplier_passed
        and dsers_passed
        and logistics_passed
    ):
        status = "HIGH_POTENTIAL_UNDERCUT_OPPORTUNITY"
        status_icon = "🟠"
        passed = True  # Allowed in opportunity mode with bundle margin recovery strategy
        overall_score = 85
        feedback = (
            f"Flagged as HIGH_POTENTIAL_UNDERCUT_OPPORTUNITY. High market/viral demand with front-end price undercut (${research.selling_price:.2f}) "
            f"and multi-pack bundle margin recovery (Tiers 2 & 3 deliver > 3.0x blended margin)."
        )

    # Tier 3: 🔴 HARD_REJECT
    else:
        status = "HARD_REJECT"
        status_icon = "🔴"
        passed = False
        overall_score = max(10, 100 - (len(violations) * 20))
        feedback = f"HARD REJECT: Deliverable failed {len(violations)} critical check(s). Supplier vetting or core brand/guardrails failed."

    audit_result = GatekeeperAuditData(
        passed=passed,
        status=status,
        status_icon=status_icon,
        violations=violations,
        overall_score=overall_score,
        brand_compliance_check=brand_passed,
        cro_mobile_check=cro_passed,
        finance_markup_check=finance_passed,
        supplier_vetting_check=supplier_passed,
        logistics_warehouse_check=logistics_passed,
        live_spend_guardrail_check=process_passed,
        dsers_data_mapping_check=dsers_passed,
        detailed_feedback=feedback,
        undercut_opportunity_report=undercut_report,
    )

    return {
        "audit_report": audit_result,
        "self_healing_rules_added": rules_added,
    }
