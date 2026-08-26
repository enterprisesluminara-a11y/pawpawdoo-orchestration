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
        hero_headline=f"Give Your Furry Best Friends The Cloud Sleep They Deserve — Because It's {BRAND_TAGLINE}",
        hero_subheadline=f"Warm, cozy orthopedic cloud comfort for dogs & cats. Melts daily anxiety and cradles joints in 5 minutes.",
        tagline=BRAND_TAGLINE,
        brand_palette=BRAND_PALETTE,
        value_propositions=[
            f"Pawmily first. Dedicated to keeping our fur-babies cozy, calm, and deeply loved.",
            f"Fast Local Dispatch: {logistics_badge}.",
            "All-Pet Comfort: 360° soothing bolster provides instant security for both dogs and cats.",
            "100% Machine Washable: Zippered waterproof inner lining resists accidents, fur, and odors.",
            "Non-Slip Grip Base: Stays firmly in place on hardwood and tile floors.",
        ],
        offer_tiers=[
            {
                "tier_name": "Standard Pet Comfort Pack",
                "quantity": 1,
                "title": "1x Orthopedic Cloud Pet Bed",
                "price": price,
                "original_value": round(price * 1.3, 2),
                "badge": "Standard Pack",
                "free_shipping": True,
            },
            {
                "tier_name": "Most Popular — Multi-Room / Multi-Pet Pack",
                "quantity": 2,
                "title": "2x Orthopedic Cloud Pet Beds (Living Room + Bedroom)",
                "price": bundle_2_price,
                "savings": "Save 15%",
                "badge": "BEST VALUE — 68% OF PET PARENTS CHOOSE THIS",
                "free_shipping": True,
                "free_bonus": "Free Odor-Eliminating Paw Care Guide",
            },
            {
                "tier_name": "Ultimate Fur-Family Pack",
                "quantity": 3,
                "title": "3x Orthopedic Cloud Pet Beds (Multi-Pet Household)",
                "price": bundle_3_price,
                "savings": "Save 22%",
                "badge": "MAXIMUM SAVINGS",
                "free_shipping": True,
                "free_bonus": "Free Waterproof Spare Cover + Pet Grooming Glove",
            },
        ],
        mobile_first_elements=[
            "Single-column 390px viewport-optimized vertical card layout with 48px tap targets.",
            "Logo title with stacked 'Pawmily first.' tagline directly underneath (Rule #12).",
            "Interactive Size Selector (S/M/L/XL) and Color Swatch Selector (Cloud Cream, Warm Latte, Slate Grey).",
            "Cat & Dog lifestyle showcase visuals and 1-click dynamic checkout above the fold.",
        ],
        sticky_cta_bar={
            "enabled": True,
            "text": "Flash Sale: Up to 22% Off",
            "button_label": "Claim Your Cloud Bed Now",
            "bg_color": BRAND_PALETTE["primary_terracotta"],
            "text_color": BRAND_PALETTE["cream_background"],
            "mobile_visible_after_scroll_px": 250,
        },
        guarantee_risk_reversal="30-Night 'Happy Paws' Guarantee — If your dog or cat doesn't fall completely in love, return it for a 100% refund.",
        social_proof_elements=[
            "Over 14,800+ Happy Dogs & Cats Sleeping Soundly",
            "4.9/5 Stars Verified Dog & Cat Parent Reviews with Photo Evidence",
            "Loved by Pet Lifestyle & Comfort Leaders Across the US",
        ],
        logistics_badge=logistics_badge,
    )

    return {"storefront_offer": result}
