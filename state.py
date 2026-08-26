"""
LangGraph State Definitions and Pydantic Schemas for PawPawDoo Team.
Enhanced with Market Adapters, Supplier Vetting, Logistics, and 3-Tier Statuses.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field


class TrendIntelligence(BaseModel):
    google_trends_score: int = Field(description="Google Trends interest index (0-100)")
    google_trends_trajectory: str = Field(description="RISING, BREAKOUT, STABLE, DECLINING")
    breakout_queries: List[str]
    tiktok_viral_velocity: str = Field(description="HIGH, MEDIUM, LOW")
    tiktok_top_hashtags: List[str]
    meta_active_competitor_ads: int
    meta_top_angles: List[str]


class MarketplaceBenchmark(BaseModel):
    amazon_buybox_price: float
    amazon_top_listing_rating: float
    amazon_review_count: int
    ebay_us_median_price: float
    ebay_recent_sales_velocity: str
    target_undercut_price: float = Field(
        description="Priced lower than top Amazon/eBay US listings while keeping landed markup >= 3.0x"
    )


class SupplierVettingData(BaseModel):
    aliexpress_product_id: str
    dsers_sku: str
    supplier_name: str
    years_on_platform: float = Field(description="Years active on AliExpress (Rule #7 >= 1.0 year)")
    overall_rating: float = Field(description="Overall star rating (Rule #7 >= 4.0 stars)")
    shipping_days_min: int
    shipping_days_max: int
    has_tracked_shipping: bool
    china_warehouse_cost: float
    china_shipping_cost: float
    china_delivery_days: str
    us_warehouse_cost: float
    us_shipping_cost: float
    us_delivery_days: str
    selected_warehouse: Literal["US", "CHINA"]
    warehouse_cost_delta: float = Field(description="US shipping diff vs China")
    warehouse_selection_rationale: str
    vetting_passed: bool
    vetting_issues: List[str] = []


class UndercutStrategy(BaseModel):
    is_applicable: bool = False
    opportunity_flag: Optional[str] = None  # "HIGH_POTENTIAL_UNDERCUT_OPPORTUNITY"
    amazon_price: float = 0.0
    ebay_price: float = 0.0
    recommended_entry_price: float = 0.0
    single_unit_markup: float = 0.0
    bundle_margin_recovery: List[Dict[str, Any]] = []
    strategic_rationale: str = ""


class CompetitorResearchData(BaseModel):
    product_name: str
    niche: str
    target_audience: str
    pain_points: List[str]
    unique_selling_points: List[str]
    trends: TrendIntelligence
    marketplace: MarketplaceBenchmark
    supplier_logistics: SupplierVettingData
    cogs: float = Field(description="Cost of Goods Sold (Product + Tracked Landed Shipping)")
    selling_price: float = Field(description="Recommended DTC retail price")
    markup_multiplier: float = Field(description="Selling Price / COGS")
    undercut_strategy: Optional[UndercutStrategy] = None
    research_summary: str


class StorefrontOfferData(BaseModel):
    hero_headline: str
    hero_subheadline: str
    tagline: str
    brand_palette: Dict[str, str]
    value_propositions: List[str]
    offer_tiers: List[Dict[str, Any]]
    mobile_first_elements: List[str]
    sticky_cta_bar: Dict[str, Any]
    guarantee_risk_reversal: str
    social_proof_elements: List[str]
    logistics_badge: str = Field(description="e.g. 'Ships Fast in 3-5 Days from US Warehouse'")


class AdCreative(BaseModel):
    angle_name: str
    target_platform: str
    hook_3s: List[str]
    visual_storyboard: List[str]
    script_voiceover: str
    cta_copy: str


class AdCampaignData(BaseModel):
    campaign_name: str
    core_angles: List[AdCreative]
    ad_copy_variations: List[Dict[str, str]]
    recommended_target_interests: List[str]


class AuditViolation(BaseModel):
    category: str
    description: str
    rule_reference: Optional[str] = None
    suggested_fix: str
    suggested_learned_rule: Optional[str] = None
    reason: Optional[str] = None


class GatekeeperAuditData(BaseModel):
    passed: bool
    status: Literal["DRAFT_APPROVED", "HIGH_POTENTIAL_UNDERCUT_OPPORTUNITY", "HARD_REJECT"]
    status_icon: str  # 🟢, 🟠, 🔴
    violations: List[AuditViolation]
    overall_score: int  # 0 to 100
    brand_compliance_check: bool
    cro_mobile_check: bool
    finance_markup_check: bool
    supplier_vetting_check: bool
    logistics_warehouse_check: bool
    live_spend_guardrail_check: bool
    dsers_data_mapping_check: bool
    detailed_feedback: str
    undercut_opportunity_report: Optional[str] = None


class PawPawDooState(TypedDict, total=False):
    # Inputs
    product_request: Dict[str, Any]
    
    # Agent Outputs
    product_research: Optional[CompetitorResearchData]
    storefront_offer: Optional[StorefrontOfferData]
    ad_campaign: Optional[AdCampaignData]
    audit_report: Optional[GatekeeperAuditData]
    
    # Orchestration & Self-Healing Feedback
    iteration_count: int
    max_iterations: int
    feedback_history: List[str]
    self_healing_rules_added: List[str]
    is_draft: bool
    final_output: Optional[Dict[str, Any]]
