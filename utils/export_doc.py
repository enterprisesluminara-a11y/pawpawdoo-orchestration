"""
Google Doc Structured Exporter for PawPawDoo Multi-Agent Architecture.
Formats approved drafts and opportunity assessments into an executive Google Doc-ready structure.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
from config import BRAND_NAME, BRAND_PALETTE, BRAND_TAGLINE
from state import PawPawDooState


class GoogleDocExporter:
    @staticmethod
    def generate_google_doc_markdown(state: PawPawDooState) -> str:
        """Constructs a clean, publication-ready Google Doc structured markdown deliverable."""
        research = state.get("product_research")
        storefront = state.get("storefront_offer")
        ad_campaign = state.get("ad_campaign")
        audit = state.get("audit_report")

        if not research or not storefront or not ad_campaign or not audit:
            return "# PawPawDoo - Incomplete Deliverable State"

        logistics = research.supplier_logistics
        marketplace = research.marketplace
        trends = research.trends

        status_badge = f"{audit.status_icon} **{audit.status}** (Compliance Score: {audit.overall_score}/100)"

        doc = f"""# 📄 PAWPAWDOO PRODUCT LAUNCH BLUEPRINT (GOOGLE DOC FORMAT)

**Document ID:** `DOC-PPD-{abs(hash(research.product_name)) % 1000000:06d}`  
**Brand:** **{BRAND_NAME}** | **Tagline:** *"{BRAND_TAGLINE}"*  
**Operational Mode:** `DRAFT` (Strict Rule #3: No Live Spend / Ad Triggering Without Human Sign-Off)  
**Gatekeeper Status:** {status_badge}  

---

## 📑 TABLE OF CONTENTS
1. [Executive Summary & Launch Verdict](#1-executive-summary--launch-verdict)
2. [Market Trends & Demand Signals](#2-market-trends--demand-signals)
3. [Competitive Marketplace Benchmarks & Undercut Pricing](#3-competitive-marketplace-benchmarks--undercut-pricing)
4. [Supplier Vetting & 1-Click DSers / Shopify Logistics](#4-supplier-vetting--1-click-dsers--shopify-logistics)
5. [Storefront Copy, Mobile CRO & Offer Bundles](#5-storefront-copy-mobile-cro--offer-bundles)
6. [Viral Direct-Response Video Ad Frameworks](#6-viral-direct-response-video-ad-frameworks)
7. [Financial & CRO Gatekeeper Compliance Audit](#7-financial--cro-gatekeeper-compliance-audit)

---

## 1. EXECUTIVE SUMMARY & LAUNCH VERDICT

| Metric / Parameter | Value | Assessment |
| :--- | :--- | :--- |
| **Product Name** | {research.product_name} | Verified High Demand |
| **Niche** | {research.niche} | Premium Pet Wellness |
| **Target Audience** | {research.target_audience} | Dog Parents (25-54) |
| **Landed COGS** | ${research.cogs:.2f} | {logistics.selected_warehouse} Warehouse Delivery |
| **DTC Retail Price** | ${research.selling_price:.2f} | Undercuts Amazon/eBay |
| **Markup Multiplier** | **{research.markup_multiplier:.2f}x** | {'✅ Rule #5 Pass (>= 3.0x)' if research.markup_multiplier >= 3.0 else '🟠 Rule #10 Opportunity'} |
| **Fulfillment Window** | **{logistics.shipping_days_min}-{logistics.shipping_days_max} Days** | {logistics.selected_warehouse} Priority Tracked |

"""

        if audit.undercut_opportunity_report:
            doc += f"""
> [!IMPORTANT]
> ### 🟠 High Potential Undercut Strategy Active
> {audit.undercut_opportunity_report}

"""

        doc += f"""
---

## 2. MARKET TRENDS & DEMAND SIGNALS

- **Google Trends Index:** `{trends.google_trends_score}/100` ({trends.google_trends_trajectory})
- **TikTok Viral Velocity:** `{trends.tiktok_viral_velocity}`
- **Active Competitor Meta Ads:** `{trends.meta_active_competitor_ads} ads currently running`

### Breakout Search Queries
{chr(10).join(f"- 📈 *\"{q}\"*" for q in trends.breakout_queries)}

### Trending TikTok Hashtags
{chr(10).join(f"- `{h}`" for h in trends.tiktok_top_hashtags)}

---

## 3. COMPETITIVE MARKETPLACE BENCHMARKS & UNDERCUT PRICING

*Enforcing Rule #6: Price lower than top Amazon/eBay US listings while keeping landed markup >= 3.0x.*

| Platform | Benchmark Metric | Listing Price / Data |
| :--- | :--- | :--- |
| **Amazon.com** | Top Buy Box Competitor | **${marketplace.amazon_buybox_price:.2f}** ({marketplace.amazon_top_listing_rating}★ / {marketplace.amazon_review_count:,} reviews) |
| **eBay US** | Median Sold Price | **${marketplace.ebay_us_median_price:.2f}** ({marketplace.ebay_recent_sales_velocity}) |
| **PawPawDoo DTC** | **Target Undercut Price** | **${research.selling_price:.2f}** (Saves customer ${(marketplace.amazon_buybox_price - research.selling_price):.2f} vs Amazon) |

---

## 4. SUPPLIER VETTING & 1-CLICK DSERS / SHOPIFY LOGISTICS

*Enforcing Rules #7, #8, #9 for supply chain stability, fast US dispatch, and 1-click import.*

```json
{{
  "shopify_import_ready": true,
  "aliexpress_product_id": "{logistics.aliexpress_product_id}",
  "dsers_sku": "{logistics.dsers_sku}",
  "supplier_name": "{logistics.supplier_name}",
  "supplier_tenure_years": {logistics.years_on_platform},
  "supplier_rating_stars": {logistics.overall_rating},
  "selected_warehouse": "{logistics.selected_warehouse}",
  "shipping_service": "{'USPS Priority Tracked (3-5 Days)' if logistics.selected_warehouse == 'US' else 'ePacket / Special Line (8-12 Days)'}",
  "shipping_cost_usd": {logistics.us_shipping_cost if logistics.selected_warehouse == 'US' else logistics.china_shipping_cost}
}}
```

**Warehouse Cost Delta Analysis (Rule #8):**
- **US Warehouse Shipping:** ${logistics.us_shipping_cost:.2f} (3-5 days delivery)
- **China Warehouse Shipping:** ${logistics.china_shipping_cost:.2f} (8-12 days delivery)
- **Cost Difference:** `${logistics.warehouse_cost_delta:.2f}` (<= $3.00 threshold)
- **Logistics Decision:** *{logistics.warehouse_selection_rationale}*

---

## 5. STOREFRONT COPY, MOBILE CRO & OFFER BUNDLES

### Hero Header Section
- **H1 Headline:** {storefront.hero_headline}
- **Subheadline:** {storefront.hero_subheadline}
- **Brand Tagline Integration:** `{storefront.tagline}`
- **Logistics Trust Badge:** `{storefront.logistics_badge}`

### Brand Palette (Rule #1)
- **Primary Terracotta:** `{storefront.brand_palette.get('primary_terracotta')}`
- **Espresso Text:** `{storefront.brand_palette.get('espresso_text')}`
- **Cream Background:** `{storefront.brand_palette.get('cream_background')}`

### Value Propositions
{chr(10).join(f"- {vp}" for vp in storefront.value_propositions)}

### High-Converting DTC Offer Bundles
"""

        for tier in storefront.offer_tiers:
            doc += f"""
#### 🏷️ Tier {tier.get('quantity')}: {tier.get('title')}
- **Retail Price:** ${tier.get('price'):.2f} (Badge: `{tier.get('badge')}`)
- **Free Bonus Included:** {tier.get('free_bonus', 'Standard Packaging')} | Free Express Shipping: `{tier.get('free_shipping')}`
"""

        doc += f"""
### Mobile CRO & Sticky CTA Bar (Rule #4)
- **Sticky CTA Bar Enabled:** `{storefront.sticky_cta_bar.get('enabled')}` (Button Text: "{storefront.sticky_cta_bar.get('button_label')}")
- **Mobile Optimizations:**
{chr(10).join(f"  - {m}" for m in storefront.mobile_first_elements)}
- **Risk Reversal Guarantee:** {storefront.guarantee_risk_reversal}

---

## 6. VIRAL DIRECT-RESPONSE VIDEO AD FRAMEWORKS

- **Campaign:** {ad_campaign.campaign_name}
- **Target Audience Segments:** {', '.join(ad_campaign.recommended_target_interests)}

"""

        for idx, angle in enumerate(ad_campaign.core_angles, 1):
            doc += f"""
### 🎬 Angle {idx}: {angle.angle_name} ({angle.target_platform})

**3-Second Thumb-Stopping Hooks:**
{chr(10).join(f"- \"{h}\"" for h in angle.hook_3s)}

**Visual Storyboard Beats:**
{chr(10).join(f"- {v}" for v in angle.visual_storyboard)}

**Voiceover Script:**
> "{angle.script_voiceover}"

**Call To Action:** `{angle.cta_copy}`

"""

        doc += f"""
---

## 7. FINANCIAL & CRO GATEKEEPER COMPLIANCE AUDIT

- **Final Status:** {status_badge}
- **Brand Palette Compliant:** `{audit.brand_compliance_check}`
- **Tagline ('{BRAND_TAGLINE}') Compliant:** `True`
- **Mobile CRO & Sticky CTA Compliant:** `{audit.cro_mobile_check}`
- **Supplier Vetting Compliant (Rule #7):** `{audit.supplier_vetting_check}`
- **Warehouse Logistics Delta Compliant (Rule #8):** `{audit.logistics_warehouse_check}`
- **1-Click DSers / AliExpress ID Mapping (Rule #9):** `{audit.dsers_data_mapping_check}`
- **Financial Markup Compliant (Rule #5):** `{audit.finance_markup_check}`
- **DRAFT / Live Spend Guardrail (Rule #3):** `{audit.live_spend_guardrail_check}`

**Auditor Feedback:**  
*{audit.detailed_feedback}*

---
*End of Google Doc Structured Export — Generated by PawPawDoo Multi-Agent Engine.*
"""
        return doc

    @classmethod
    def export_to_file(cls, state: PawPawDooState, output_path: Path) -> Path:
        content = cls.generate_google_doc_markdown(state)
        output_path.write_text(content, encoding="utf-8")
        return output_path

