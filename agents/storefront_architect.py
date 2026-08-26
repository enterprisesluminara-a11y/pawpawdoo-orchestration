"""
Storefront & Offer Architect Agent (Gemini API).
Builds high-converting DTC product pages, offer stacks, bundles, mobile-first layouts, and brand identity.
"""

from __future__ import annotations

import json
from typing import Any, Dict
from agents.base import LLMClient
from config import BRAND_NAME, BRAND_PALETTE, BRAND_TAGLINE
from state import PawPawDooState, StorefrontOfferData


def run_storefront_architect_agent(state: PawPawDooState) -> Dict[str, Any]:
    """
    Executes Storefront & Offer Architecture.
    Model: Google Gemini
    """
    research = state.get("product_research")
    if not research:
        raise ValueError("Product research must precede storefront architecture.")

    price = research.selling_price
    bundle_2_price = round(price * 1.70, 2)  # Save 15% on 2
    bundle_3_price = round(price * 2.35, 2)  # Save 22% on 3

    logistics = research.supplier_logistics
    if logistics.selected_warehouse == "US":
        logistics_badge = f"Ships Fast in 3-5 Days from US Warehouse (Tracked USPS)"
    else:
        logistics_badge = f"Tracked Express Delivery ({logistics.shipping_days_min}-{logistics.shipping_days_max} Days)"

    result = StorefrontOfferData(
        hero_headline=f"Give Your Furry Best Friend The Cloud Sleep They Deserve — Because It's {BRAND_TAGLINE}",
        hero_subheadline=f"Engineered with orthopedic memory foam & anxiety-melting faux fur to soothe joints and melt stress within 5 minutes.",
        tagline=BRAND_TAGLINE,
        brand_palette=BRAND_PALETTE,
        value_propositions=[
            f"Pawmily first. We treat your pet like our own family with veterinarian-approved orthopedic support.",
            f"Fast Local Dispatch: {logistics_badge}.",
            "Instant Anxiety Relief: 360-degree raised bolster simulates mama dog's comforting embrace.",
            "100% Machine Washable: Zippered waterproof lining resists slobber, accidents, and stubborn odors.",
            "Non-Slip Base: High-traction grip keeps the bed safely anchored on tiles and hardwood.",
        ],
        offer_tiers=[
            {
                "tier_name": "Standard Paw Care",
                "quantity": 1,
                "title": "1x Cloud Dog Bed",
                "price": price,
                "original_value": round(price * 1.3, 2),
                "badge": "Standard Pack",
                "free_shipping": True,
            },
            {
                "tier_name": "Most Popular — Multi-Room Pack",
                "quantity": 2,
                "title": "2x Cloud Dog Beds (Living Room + Bedroom)",
                "price": bundle_2_price,
                "savings": "Save 15%",
                "badge": "BEST VALUE — 68% OF CUSTOMERS CHOOSE THIS",
                "free_shipping": True,
                "free_bonus": "Free Odor-Eliminating Paw Care Guide",
            },
            {
                "tier_name": "Ultimate Fur-Family Pack",
                "quantity": 3,
                "title": "3x Cloud Dog Beds (Multi-Pet Household)",
                "price": bundle_3_price,
                "savings": "Save 22%",
                "badge": "MAXIMUM SAVINGS",
                "free_shipping": True,
                "free_bonus": "Free Waterproof Spare Cover + Grooming Glove",
            },
        ],
        mobile_first_elements=[
            "Single-column 390px viewport-optimized vertical card layout.",
            "High-contrast 48px tap targets for frictionless thumbs-only checkout.",
            "Swipeable image/GIF carousel demonstrating memory foam bounce-back.",
            "1-click Apple Pay / Google Pay dynamic checkout button above the fold.",
        ],
        sticky_cta_bar={
            "enabled": True,
            "text": "Flash Sale: Up to 22% Off",
            "button_label": "Claim Your Cloud Bed Now",
            "bg_color": BRAND_PALETTE["primary_terracotta"],
            "text_color": BRAND_PALETTE["cream_background"],
            "mobile_visible_after_scroll_px": 250,
        },
        guarantee_risk_reversal="30-Night 'Tail-Wagging Guarantee' — If your dog doesn't instantly fall in love, return for a 100% refund, no questions asked.",
        social_proof_elements=[
            "Over 14,800+ Happy Paws Sleeping Soundly",
            "4.9/5 Stars Verified Pet Parent Reviews with Photo Evidence",
            "Featured in Modern Dog & Canine Wellness Digest",
        ],
        logistics_badge=logistics_badge,
    )

    return {"storefront_offer": result}
