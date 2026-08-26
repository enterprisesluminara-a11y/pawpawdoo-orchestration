"""
RAG Brand Memory Layer for PawPawDoo Multi-Agent Swarm.
Centralized repository for:
- 14 Learned Rules (from AGENT_INSTRUCTIONS.md)
- Negative Constraints (Anti-patterns to avoid)
- Visual & Copy Guidelines (Palette, Typography, Logo Lockup)
- Historical Corrections & Review Feedback
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from config import BRAND_NAME, BRAND_PALETTE, BRAND_TAGLINE


class BrandMemoryItem:
    def __init__(
        self,
        id: str,
        category: str,
        title: str,
        content: str,
        negative_constraint: Optional[str] = None,
        keywords: Optional[List[str]] = None,
    ):
        self.id = id
        self.category = category  # BRAND, CRO, UX, FINANCE, PRICING, SUPPLIER, LOGISTICS, DATA
        self.title = title
        self.content = content
        self.negative_constraint = negative_constraint
        self.keywords = keywords or []

    def matches(self, query: str) -> float:
        query_words = set(re.findall(r"\w+", query.lower()))
        item_words = set(re.findall(r"\w+", f"{self.title} {self.content} {' '.join(self.keywords)}".lower()))
        overlap = query_words.intersection(item_words)
        return len(overlap) / max(1, len(query_words))


class BrandMemoryBank:
    """
    RAG Memory bank that agents must query before initiating tasks.
    """

    def __init__(self):
        self.items: List[BrandMemoryItem] = []
        self._load_seed_memory()

    def _load_seed_memory(self):
        # 1. Brand Identity & Palette
        self.items.append(
            BrandMemoryItem(
                id="RULE-01",
                category="BRAND",
                title="Brand Palette Specification",
                content=f"Primary Terracotta ({BRAND_PALETTE['primary_terracotta']}), Espresso Text ({BRAND_PALETTE['espresso_text']}), Warm Cream Background ({BRAND_PALETTE['cream_background']}).",
                negative_constraint="NEVER use generic pure black (#000000) or cold neon colors. Keep background warm cream (#FAF8F5).",
                keywords=["color", "palette", "terracotta", "espresso", "cream", "css", "theme", "design"],
            )
        )

        # 2. Tagline & Slogan
        self.items.append(
            BrandMemoryItem(
                id="RULE-02",
                category="BRAND",
                title="Official Tagline",
                content=f"Official slogan is '{BRAND_TAGLINE}'. Must appear in core value propositions, headers, and guarantees.",
                negative_constraint="NEVER omit the official tagline 'Pawmily first.' or alter its punctuation.",
                keywords=["tagline", "slogan", "pawmily", "first", "copy", "headline", "mission"],
            )
        )

        # 3. Draft Mode & Spend Guardrails
        self.items.append(
            BrandMemoryItem(
                id="RULE-03",
                category="PROCESS",
                title="Strict Draft Mode",
                content="All deliverables and products must be created as unpublished DRAFT records. No live ad budget triggers without human sign-off.",
                negative_constraint="NEVER publish products directly to live storefront or trigger paid social ad spend without explicit human confirmation.",
                keywords=["draft", "spend", "safety", "publish", "guardrail", "ad spend", "live"],
            )
        )

        # 4. Mobile CRO & Layout
        self.items.append(
            BrandMemoryItem(
                id="RULE-04",
                category="CRO",
                title="Mobile-First Viewport & Sticky CTA Bar",
                content="Design for 390px mobile viewports with 48px+ tap targets, single-column vertical flow, and a sticky bottom CTA bar appearing after 250px scroll.",
                negative_constraint="NEVER design desktop-only or cluttered multi-column layouts that break on mobile screens.",
                keywords=["mobile", "cro", "sticky", "cta", "viewport", "conversion", "button", "layout"],
            )
        )

        # 5. Financial Markup Threshold
        self.items.append(
            BrandMemoryItem(
                id="RULE-05",
                category="FINANCE",
                title="Minimum 3.0x Landed Markup",
                content="Every product must maintain at least a 3.0x landed markup multiplier (Retail Price / Landed COGS >= 3.0x) for CAC safety.",
                negative_constraint="NEVER accept products with < 3.0x markup unless flagged as High Potential Undercut Opportunity with bundle margin recovery.",
                keywords=["finance", "margin", "markup", "cogs", "profit", "cac", "pricing"],
            )
        )

        # 6. Marketplace Benchmark Undercut
        self.items.append(
            BrandMemoryItem(
                id="RULE-06",
                category="PRICING",
                title="Marketplace Price Undercut",
                content="Price slightly below top Amazon Buy Box and eBay US median listings while strictly keeping markup >= 3.0x.",
                negative_constraint="NEVER price higher than the dominant Amazon Buy Box listing without immense value add.",
                keywords=["amazon", "ebay", "undercut", "pricing", "competitor", "benchmark"],
            )
        )

        # 7. Supplier Vetting Standards
        self.items.append(
            BrandMemoryItem(
                id="RULE-07",
                category="SUPPLIER",
                title="Supplier Quality Verification",
                content="Suppliers must have >= 1.0 year operational history on AliExpress, >= 4.0 star rating, and end-to-end tracked shipping.",
                negative_constraint="NEVER partner with unrated suppliers, suppliers < 1 year old, or carriers without tracked dispatch.",
                keywords=["supplier", "aliexpress", "vetting", "rating", "dispute", "tracking"],
            )
        )

        # 8. US Warehouse Logistics Rule
        self.items.append(
            BrandMemoryItem(
                id="RULE-08",
                category="LOGISTICS",
                title="US Warehouse Priority",
                content="Default to US warehouse dispatch (3-5 business days delivery) if shipping cost delta between US and China is <= $3.00.",
                negative_constraint="NEVER choose slow 15-25 day China ePacket if fast 3-5 day US warehouse shipping is available for <= $3.00 extra.",
                keywords=["logistics", "warehouse", "shipping", "delivery", "usps", "fast", "us"],
            )
        )

        # 9. DSers & AliExpress SKU Mapping
        self.items.append(
            BrandMemoryItem(
                id="RULE-09",
                category="DATA",
                title="1-Click Auto-Fulfillment SKU Mapping",
                content="Always output mapped AliExpress Product ID and DSers SKU (e.g. DS-PPD-BED-001) in product tags and metadata.",
                negative_constraint="NEVER leave supplier SKU or product ID unmapped.",
                keywords=["dsers", "sku", "aliexpress", "fulfillment", "mapping", "tags"],
            )
        )

        # 10. Undercut Opportunity Recovery
        self.items.append(
            BrandMemoryItem(
                id="RULE-10",
                category="OPPORTUNITY",
                title="High-Potential Undercut Opportunity Recovery",
                content="When a viral product has high demand but <3.0x single unit markup, generate a multi-pack bundle strategy (2-pack and 3-pack) to recover margin.",
                negative_constraint="NEVER discard a viral breakout product without formulating an undercut recovery bundle model.",
                keywords=["opportunity", "viral", "recovery", "bundle", "multi-pack"],
            )
        )

        # 11. Multi-Pet Positioning (Cats & Dogs)
        self.items.append(
            BrandMemoryItem(
                id="RULE-11",
                category="BRAND",
                title="Warm Pet Lifestyle for BOTH Cats & Dogs",
                content="Position PawPawDoo as a warm, premium pet lifestyle brand equally welcoming to BOTH cats and dogs. Focus on calming comfort, nesting security, and anxiety relief.",
                negative_constraint="NEVER over-index solely on dogs. NEVER use cold, clinical or hospital-style medical jargon.",
                keywords=["cats", "dogs", "multi-pet", "calming", "lifestyle", "nesting", "cozy", "tone", "copy"],
            )
        )

        # 12. Vertical Brand Lockup
        self.items.append(
            BrandMemoryItem(
                id="RULE-12",
                category="UX",
                title="Vertical Tagline Placement",
                content="Position the official tagline 'Pawmily first.' directly underneath the PawPawDoo logo title in all headers, footers, and brand lockups.",
                negative_constraint="NEVER place tagline as a horizontal side pill or misalign it from the brand title stack.",
                keywords=["logo", "lockup", "header", "footer", "tagline", "brand", "stack", "underneath"],
            )
        )

        # 13. Product Assets & Variants Showcase
        self.items.append(
            BrandMemoryItem(
                id="RULE-13",
                category="CRO",
                title="Product Variant Selectors & Lifestyle Assets",
                content="Include interactive Size selectors (S/M/L/XL with cat/dog icons) and Color swatches (Terracotta Cloud, Cream Velvet, Slate Grey) embedded directly inside the buy box.",
                negative_constraint="NEVER show plain text without interactive size and color swatches in the offer box. Avoid standalone uncontextual stock photos.",
                keywords=["variant", "size", "color", "swatch", "gallery", "buy box", "assets", "selector"],
            )
        )

        # 14. Persona Skills & Taste
        self.items.append(
            BrandMemoryItem(
                id="RULE-14",
                category="SKILLS",
                title="UI/UX Design Taste & CRO Persona",
                content="Equip storefront architecture with top-tier DTC UI/UX taste, direct-response conversion rate optimization, and emotional pet lifestyle copywriting.",
                negative_constraint="NEVER produce low-effort or generic e-commerce templates.",
                keywords=["skills", "taste", "cro", "ui", "ux", "persona", "copywriting"],
            )
        )

    def query(self, query_text: str, category: Optional[str] = None, top_k: int = 4) -> List[BrandMemoryItem]:
        """
        Retrieves the most relevant brand rules and negative constraints for a given task.
        """
        filtered = self.items
        if category:
            filtered = [item for item in self.items if item.category.upper() == category.upper()]

        scored = []
        for item in filtered:
            score = item.matches(query_text)
            scored.append((score, item))

        # Sort by relevance score descending
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:top_k]]

    def get_negative_constraints(self, category: Optional[str] = None) -> List[str]:
        """
        Returns all critical negative constraints to inject into LLM system prompts.
        """
        constraints = []
        for item in self.items:
            if category and item.category.upper() != category.upper():
                continue
            if item.negative_constraint:
                constraints.append(f"• [{item.id}] {item.negative_constraint}")
        return constraints

    def get_formatted_context(self, task_name: str, query: str = "") -> str:
        """
        Generates a structured RAG context block ready for injection into agent prompts.
        """
        relevant_rules = self.query(f"{task_name} {query}", top_k=5)
        constraints = self.get_negative_constraints()

        rules_str = "\n".join(f"  - [{r.id} | {r.category}] {r.title}: {r.content}" for r in relevant_rules)
        constraints_str = "\n".join(f"  {c}" for c in constraints[:6])

        return f"""
=== 🧠 RAG BRAND MEMORY CONTEXT ({task_name.upper()}) ===
Relevant Brand Rules & Specifications:
{rules_str}

Critical Negative Constraints (ANTI-PATTERNS TO STRICTLY AVOID):
{constraints_str}
===========================================================
"""


# Global Singleton Instance
brand_memory = BrandMemoryBank()

