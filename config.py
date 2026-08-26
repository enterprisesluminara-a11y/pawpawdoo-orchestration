"""
Configuration and Brand Constants for PawPawDoo Multi-Agent Architecture.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).parent.resolve()
AGENT_INSTRUCTIONS_PATH = BASE_DIR / "AGENT_INSTRUCTIONS.md"

# PawPawDoo Brand Specifications
BRAND_NAME = "PawPawDoo"
BRAND_TAGLINE = "Pawmily first."
BRAND_PALETTE = {
    "primary_terracotta": "#C86432",
    "espresso_text": "#37281D",
    "cream_background": "#FAF8F5",
}

# Financial & CRO Guardrails
MIN_MARKUP_MULTIPLIER = 3.0
DRAFT_MODE = True  # Strict guardrail: Never publish live changes or spend live budget without confirmation

# LLM Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Shopify Admin API Configuration
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL", "pawpawdoo.store")
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN", "")
SHOPIFY_CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID", "")
SHOPIFY_CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET", "")
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2024-10")

