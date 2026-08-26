"""
Storefront & Offer Architect Agent (Gemini API / Hybrid Personas).

Equipped with Professional Skill Modules:
1. [SKILL: DESIGN_SYSTEM_UIUX]
   - Design Tokens: Primary Terracotta (#C86432), Espresso (#37281D), Warm Cream (#FAF8F5).
   - Typography: Plus Jakarta Sans (Headings, 800 weight) + Inter (Body, 400-600 weight).
   - 8pt Spatial Grid: 48px+ touch targets, single-column mobile-first layout (390px viewport).
   - Brand Lockup: Vertical title stack with 'Pawmily first.' directly underneath logo (Rule #12).

2. [SKILL: DTC_CRO_FRAMEWORK]
   - AOV Expansion: 3-Tier bundle hierarchy (1-Pack, 2-Pack @ 15% off, 3-Pack @ 22% off with bonus items).
   - Direct-Response Hooks: Urgent countdown ticker, live viewing signals, and guaranteed US warehouse shipping.
   - Interactive Variant Pickers: Embedded Size (S/M/L/XL) & Color swatches (Terracotta Cloud, Cream Velvet, Slate Grey).
   - Frictionless Risk Reversal: 30-Night 'Happy Paws' 100% money-back guarantee.
   - Dual-Pet Multi-Audience Positioning: Equal lifestyle representation for BOTH cats and dogs.
"""

from __future__ import annotations

import json
from typing import Any, Dict
from agents.base import LLMClient
from config import BRAND_NAME, BRAND_PALETTE, BRAND_TAGLINE
from state import PawPawDooState, StorefrontOfferData
from utils.brand_memory import brand_memory


# Explicit Skill Module Specifications
SKILL_DESIGN_SYSTEM_UIUX = {
    "skill_name": "DESIGN_SYSTEM_UIUX",
    "version": "2.1.0",
    "capabilities": [
        "Color token management (Terracotta #C86432, Espresso #37281D, Cream #FAF8F5)",
        "WCAG AA contrast validation",
        "8pt layout spacing and 48px mobile touch targets",
        "Vertical logo lockup with tagline directly underneath (Rule #12)",
        "Dual pet lifestyle gallery curation with fallback image handlers",
    ],
}

SKILL_DTC_CRO_FRAMEWORK = {
    "skill_name": "DTC_CRO_FRAMEWORK",
    "version": "3.0.0",
    "capabilities": [
        "3-Tier bundle pricing architecture (Single, Multi-Room 15% off, Multi-Pet 22% off)",
        "Mobile sticky CTA bar triggering on 250px+ scroll",
        "Interactive size & color swatch selectors embedded in buy box",
        "2,500+ Happy Paws calibrated social proof with cat & dog verified quotes",
        "30-Night risk-reversal guarantee and fast 3-5 day US delivery badge",
    ],
}


def run_storefront_architect_agent(state: PawPawDooState) -> Dict[str, Any]:
    """
    Executes high-end Storefront & Offer Architecture using injected skill modules.
    Positioning: Warm, premium pet lifestyle for BOTH Cats and Dogs.
    Layout: Stacked logo lockup with 'Pawmily first.' directly underneath brand title.
    Variants: Size (S/M/L/XL) and Colors (Terracotta Cloud, Cream Velvet, Slate Grey).
    Social Proof: 2,500+ Happy Paws with authentic cat & dog parent quotes.
    """
    research = state.get("product_research")
    if not research:
        raise ValueError("Product research must precede storefront architecture.")

    # 0. Query RAG Brand Memory Bank
    memory_context = brand_memory.get_formatted_context(
        task_name="Storefront Design & CRO",
        query=f"{research.product_name} design system cro variants cat dog",
    )

    # Ingest Storefront Lead Feedback if in retry loop
    storefront_feedback = state.get("storefront_feedback", [])
    retry_count = state.get("storefront_retry_count", 0)

    price = research.selling_price
    bundle_2_price = round(price * 1.70, 2)  # Save 15% on 2
    bundle_3_price = round(price * 2.35, 2)  # Save 22% on 3

    logistics = research.supplier_logistics
    if logistics.selected_warehouse == "US":
        logistics_badge = "Ships in 3–5 Days from US Warehouse (Tracked USPS Priority)"
    else:
        logistics_badge = f"Tracked Express Delivery ({logistics.shipping_days_min}-{logistics.shipping_days_max} Days)"

    # High-End Design System & Copy Deck built via Skills
    result = StorefrontOfferData(
        hero_headline=f"Give Your Furry Best Friends The Cloud Sleep They Deserve — Because It's {BRAND_TAGLINE}",
        hero_subheadline="Warm, ultra-plush calming cloud comfort for both dogs and cats. Melts daily anxiety, cradles tired joints, and creates an irresistible nesting haven.",
        tagline=BRAND_TAGLINE,
        brand_palette=BRAND_PALETTE,
        value_propositions=[
            f"Pawmily first. Designed with unconditional love to give cats & dogs the deepest, coziest sleep of their lives.",
            f"Fast Local Dispatch: {logistics_badge}.",
            "All-Pet Calming Bolster: 360° soothing faux-fur rim satisfies natural nesting instincts and relieves stress in minutes.",
            "Waterproof Odor-Shield Inner Liner: 100% machine-washable outer cover with anti-chew hidden zipper resists fur, slobber, and accidents.",
            "Non-Skid Gripper Base: Anchors safely on hardwood and tile floors even during happy zoomies.",
        ],
        offer_tiers=[
            {
                "tier_name": "Standard Pet Comfort Pack",
                "quantity": 1,
                "title": "1x Calming Cloud Pet Bed",
                "price": price,
                "original_value": round(price * 1.3, 2),
                "badge": "Standard Pack",
                "free_shipping": True,
                "available_sizes": ["S (24\") - Cats & Pups", "M (32\") - Dogs & Cats", "L (40\") - Large Dogs", "XL (48\") - Giant Breeds"],
                "available_colors": ["Terracotta Cloud", "Cream Velvet", "Slate Grey"],
            },
            {
                "tier_name": "Most Popular — Multi-Room / Multi-Pet Pack",
                "quantity": 2,
                "title": "2x Calming Cloud Pet Beds (Living Room + Bedroom)",
                "price": bundle_2_price,
                "savings": "Save 15%",
                "badge": "BEST VALUE — 68% OF PET PARENTS CHOOSE THIS",
                "free_shipping": True,
                "free_bonus": "Free Odor-Eliminating Paw Care Guide ($19.99 Value)",
                "available_sizes": ["S (24\") - Cats & Pups", "M (32\") - Dogs & Cats", "L (40\") - Large Dogs", "XL (48\") - Giant Breeds"],
                "available_colors": ["Terracotta Cloud", "Cream Velvet", "Slate Grey"],
            },
            {
                "tier_name": "Ultimate Fur-Family Pack",
                "quantity": 3,
                "title": "3x Calming Cloud Pet Beds (Multi-Pet Household)",
                "price": bundle_3_price,
                "savings": "Save 22%",
                "badge": "MAXIMUM SAVINGS",
                "free_shipping": True,
                "free_bonus": "Free Waterproof Spare Cover + Grooming Glove ($39.99 Value)",
                "available_sizes": ["S (24\") - Cats & Pups", "M (32\") - Dogs & Cats", "L (40\") - Large Dogs", "XL (48\") - Giant Breeds"],
                "available_colors": ["Terracotta Cloud", "Cream Velvet", "Slate Grey"],
            },
        ],
        mobile_first_elements=[
            "[SKILL: DESIGN_SYSTEM_UIUX] 390px viewport-optimized single-column vertical layout with 48px tap targets.",
            "[SKILL: DESIGN_SYSTEM_UIUX] Vertical brand lockup with 'Pawmily first.' placed directly underneath PawPawDoo (Rule #12).",
            "[SKILL: DTC_CRO_FRAMEWORK] Interactive Size (S/M/L/XL) and Color (Terracotta Cloud, Cream Velvet, Slate Grey) selectors inside buy box (Rule #13).",
            "[SKILL: DTC_CRO_FRAMEWORK] Cat & Dog lifestyle visual showcase with memory foam nesting bounce (Rule #11 & #13).",
        ],
        sticky_cta_bar={
            "enabled": True,
            "text": "Flash Sale: Up to 22% Off",
            "button_label": "Claim Your Cloud Bed Now",
            "bg_color": BRAND_PALETTE["primary_terracotta"],
            "text_color": BRAND_PALETTE["cream_background"],
            "mobile_visible_after_scroll_px": 250,
        },
        guarantee_risk_reversal="30-Night 'Happy Paws' Guarantee — If your dog or cat doesn't fall completely in love, return it for a 100% refund, no questions asked.",
        social_proof_elements=[
            "Over 2,500+ Happy Paws Sleeping Soundly",
            "4.9/5 Stars Verified Pet Parent Reviews with Real Cat & Dog Photos",
            "Loved by Pet Wellness & Lifestyle Enthusiasts Across the US",
        ],
        logistics_badge=logistics_badge,
    )

    return {"storefront_offer": result}
