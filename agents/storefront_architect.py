"""
Storefront & Offer Architect Agent (Gemini API / Hybrid Personas).
Equipped with dedicated:
1. High-End UI/UX Design Taste & Brand Aesthetic Persona
2. Direct-Response E-Commerce Conversion Rate Optimization (CRO) Persona
3. Premium Multi-Pet Copywriter & E-Commerce SEO Persona

Strictly adheres to Rules 1-14 from AGENT_INSTRUCTIONS.md.
"""

from __future__ import annotations

import json
from typing import Any, Dict
from agents.base import LLMClient
from config import BRAND_NAME, BRAND_PALETTE, BRAND_TAGLINE
from state import PawPawDooState, StorefrontOfferData


def run_storefront_architect_agent(state: PawPawDooState) -> Dict[str, Any]:
    """
    Executes high-end Storefront & Offer Architecture.
    Positioning: Warm, premium pet lifestyle for BOTH Cats and Dogs.
    Layout: Stacked logo lockup with 'Pawmily first.' directly underneath brand title.
    Variants: Size (S/M/L/XL) and Colors (Terracotta Cloud, Cream Velvet, Slate Grey).
    Social Proof: 2,500+ Happy Paws with authentic cat & dog parent quotes.
    """
    research = state.get("product_research")
    if not research:
        raise ValueError("Product research must precede storefront architecture.")

    price = research.selling_price
    bundle_2_price = round(price * 1.70, 2)  # Save 15% on 2
    bundle_3_price = round(price * 2.35, 2)  # Save 22% on 3

    logistics = research.supplier_logistics
    if logistics.selected_warehouse == "US":
        logistics_badge = "Ships in 3–5 Days from US Warehouse (Tracked USPS Priority)"
    else:
        logistics_badge = f"Tracked Express Delivery ({logistics.shipping_days_min}-{logistics.shipping_days_max} Days)"

    # High-End Design System & Copy Deck
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
            "Single-column 390px viewport-optimized vertical card layout with 48px tap targets.",
            "Vertical brand lockup with 'Pawmily first.' placed directly underneath PawPawDoo (Rule #12).",
            "Interactive Size (S/M/L/XL) and Color (Terracotta Cloud, Cream Velvet, Slate Grey) selectors inside buy box (Rule #13).",
            "Cat & Dog lifestyle visual showcase with memory foam nesting bounce (Rule #11 & #13).",
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
