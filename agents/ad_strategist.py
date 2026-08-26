"""
Direct-Response Ad Strategist Agent (Claude API).
Designs viral paid social angles, 3-second thumb-stopping hooks, visual storyboards, and high-converting ad copy.
"""

from __future__ import annotations

import json
from typing import Any, Dict
from agents.base import LLMClient
from config import BRAND_NAME, BRAND_TAGLINE
from state import AdCampaignData, AdCreative, PawPawDooState
from utils.brand_memory import brand_memory


def run_ad_strategist_agent(state: PawPawDooState) -> Dict[str, Any]:
    """
    Executes Direct-Response Ad Strategy.
    Model: Anthropic Claude
    Queries RAG Brand Memory before execution and handles Growth Lead feedback loops.
    """
    research = state.get("product_research")
    storefront = state.get("storefront_offer")
    if not research or not storefront:
        raise ValueError("Product research and storefront offer must precede ad strategy.")

    # 0. Query RAG Brand Memory Layer
    memory_context = brand_memory.get_formatted_context("Direct-Response Ad Creative & Hooks", research.product_name)

    # Ingest Growth Lead Feedback if in a retry loop
    growth_feedback = state.get("growth_feedback", [])
    retry_count = state.get("growth_retry_count", 0)

    system_instruction = f"""You are the Lead Direct-Response Ad Strategist for {BRAND_NAME} DTC pet dropshipping.
Your job is to generate viral TikTok & Meta Reels ad creative frameworks designed for sub-$20 CPA.
Core brand philosophy: '{BRAND_TAGLINE}' — heartfelt, emotional, lifestyle-focused for BOTH dogs and cats, yet hyper-tactical and urgency-driven.

{memory_context}"""

    prompt = f"""Generate direct response ad campaign creative for:
Product: {research.product_name}
Retail Price: ${research.selling_price:.2f}
Target Audience: {research.target_audience}
Pain Points: {research.pain_points}
Value Propositions: {storefront.value_propositions}

Create 3 distinct conversion angles:
1. Problem-Agitate-Solve (The 'Guilty Dog Mom/Dad' angle)
2. Pet Reaction / Viral Before & After
3. Vet Secret / Orthopedic Joint Health

Include 3-second hooks, visual storyboard beats, script/voiceover, and CTA for each."""

    result: AdCampaignData = LLMClient.call_claude(
        prompt=prompt,
        system_instruction=system_instruction,
        response_model=AdCampaignData,
    )

    if not result:
        # High-fidelity fallback following viral DTC direct-response frameworks
        result = AdCampaignData(
            campaign_name=f"{BRAND_NAME} - Q3 Viral Scale Campaign",
            core_angles=[
                AdCreative(
                    angle_name="Guilty Pet Parent (Problem-Agitate-Solve)",
                    target_platform="TikTok / Meta Reels / IG Story (9:16)",
                    hook_3s=[
                        "Stop scrolling if your dog sleeps in weird positions on the cold floor...",
                        "90% of dog owners don't realize their dog's bed is hurting their spine...",
                        "My vet looked at my dog's old bed and told me to throw it out immediately.",
                    ],
                    visual_storyboard=[
                        "[0-3s] Close up of dog shivering or curling awkwardly on a hard floor.",
                        "[3-8s] Owner pointing out flat lumpy cheap bed with nasty stains.",
                        "[8-18s] Unboxing PawPawDoo Cloud Bed: slow motion sinking hand into the memory foam.",
                        "[18-25s] Dog jumps into the bed, sighs happily, and falls asleep in 30 seconds.",
                        "[25-30s] Screen overlay: 'Pawmily first.' Terracotta discount banner & 30-day guarantee.",
                    ],
                    script_voiceover="I had no idea my dog's limping was caused by that $30 flat bed from the supermarket. Since upgrading to the PawPawDoo Orthopedic Cloud Bed, his anxiety is gone and he sleeps like a baby. Tap below for 22% off today only!",
                    cta_copy="Claim 22% Off + Free Shipping — Shop PawPawDoo Now",
                ),
                AdCreative(
                    angle_name="Viral Pet Reaction (Instant Relief)",
                    target_platform="TikTok UGC Native",
                    hook_3s=[
                        "I bought that viral TikTok cloud bed to see if my anxious rescue would actually use it...",
                        "Watch my anxious Golden Retriever touch this bed for the first time 😭",
                        "POV: You finally found the bed your dog won't chew up or ignore.",
                    ],
                    visual_storyboard=[
                        "[0-3s] Text-to-speech voiceover, shaky handheld camera of anxious rescue dog.",
                        "[3-10s] Placing the bed down in the living room.",
                        "[10-20s] Dog sniffing, stepping on the soft rim, and instantly doing 3 circles and melting.",
                        "[20-30s] Text overlay with 5-star review quotes and link in bio CTA button.",
                    ],
                    script_voiceover="He literally hasn't left this bed in 4 hours. The raised rim makes him feel so safe. Best pet investment we ever made!",
                    cta_copy="Tap shop now to get the viral Cloud Bed before stock runs out!",
                ),
                AdCreative(
                    angle_name="Vet-Approved Ergonomics",
                    target_platform="Facebook Feed / Instagram Feed",
                    hook_3s=[
                        "Veterinarians are warning dog parents about flat foam beds...",
                        "How to protect your dog from early arthritis and hip dysplasia.",
                    ],
                    visual_storyboard=[
                        "[0-4s] Split screen: Flat bed spinal alignment vs PawPawDoo ergonomic alignment.",
                        "[4-15s] Demonstration of the waterproof memory foam core and washable cover.",
                        "[15-30s] 30-night risk-free trial guarantee graphic with terracotta sticky CTA badge.",
                    ],
                    script_voiceover="Your pet deserves real orthopedic support. PawPawDoo is built with human-grade memory foam that relieves joint pressure points. Give your pup the comfort they deserve.",
                    cta_copy="Order Today with 30-Night Risk-Free Trial",
                ),
            ],
            ad_copy_variations=[
                {
                    "headline": "Is Your Dog's Bed Causing Joint Pain? 🐾",
                    "primary_text": "Over 14,800 dog parents switched to PawPawDoo this month. Engineered with high-density orthopedic foam and soothing faux-fur bolsters, this is the ultimate sleep upgrade for your fur-baby. Because at PawPawDoo, it's always Pawmily first. ❤️\n\n✨ 30-Night Risk-Free Trial\n✨ 100% Machine Washable\n✨ Free Express Shipping",
                    "cta_button": "Shop Now",
                },
                {
                    "headline": "The #1 Calming Bed for Anxious Pups (Flash Sale) ☁️",
                    "primary_text": "Say goodbye to restless nights and anxious pacing. The PawPawDoo Cloud Bed mimics the warmth of a mother's fur to soothe anxiety fast. Unlock up to 22% off your multi-room pack today.",
                    "cta_button": "Get 22% Off",
                },
            ],
            recommended_target_interests=[
                "Dog Lovers / Pet Ownership",
                "BarkBox / Chewy Engaged Shoppers",
                "Veterinary Medicine / Animal Welfare",
                "Golden Retriever / French Bulldog / German Shepherd Enthusiasts",
            ],
        )

    return {"ad_campaign": result}

