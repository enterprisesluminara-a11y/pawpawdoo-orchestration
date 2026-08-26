"""
Shopify Admin API Adapter for PawPawDoo.
Handles Shopify Admin REST/GraphQL authentication, connection verification,
and 1-click draft product creation with strict Rule #3 (Draft Mode) guardrails.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional
import requests

from config import (
    BRAND_NAME,
    BRAND_TAGLINE,
    DRAFT_MODE,
    SHOPIFY_ADMIN_ACCESS_TOKEN,
    SHOPIFY_API_VERSION,
    SHOPIFY_STORE_URL,
)

logger = logging.getLogger("pawpawdoo.shopify")


class ShopifyAdapter:
    """Shopify Admin API Client with strict draft safety guardrails."""

    def __init__(
        self,
        store_url: Optional[str] = None,
        access_token: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        raw_url = store_url or SHOPIFY_STORE_URL or os.getenv("SHOPIFY_STORE_URL", "")
        self.store_url = self._normalize_store_url(raw_url)
        self.access_token = access_token or SHOPIFY_ADMIN_ACCESS_TOKEN or os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN", "")
        self.api_version = api_version or SHOPIFY_API_VERSION or "2024-10"

    @staticmethod
    def _normalize_store_url(url: str) -> str:
        """Removes protocol and trailing slashes to format the store domain."""
        url = url.strip()
        url = url.replace("https://", "").replace("http://", "")
        url = url.split("/")[0]
        return url

    @property
    def base_api_url(self) -> str:
        return f"https://{self.store_url}/admin/api/{self.api_version}"

    def ensure_access_token(self) -> str:
        """Ensures a valid access token is present, auto-refreshing via client credentials if needed."""
        if self.access_token:
            return self.access_token

        client_id = os.getenv("SHOPIFY_CLIENT_ID")
        client_secret = os.getenv("SHOPIFY_CLIENT_SECRET")
        if client_id and client_secret:
            try:
                r = requests.post(
                    f"https://{self.store_url}/admin/oauth/access_token",
                    data={
                        "grant_type": "client_credentials",
                        "client_id": client_id,
                        "client_secret": client_secret,
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=10,
                )
                if r.status_code == 200:
                    data = r.json()
                    self.access_token = data.get("access_token")
                    return self.access_token
            except Exception as e:
                logger.error(f"Failed to auto-refresh Shopify access token: {e}")
        return self.access_token

    @property
    def headers(self) -> Dict[str, str]:
        token = self.ensure_access_token()
        return {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": token,
        }

    def test_connection(self) -> Dict[str, Any]:
        """
        Tests connection to Shopify Admin API using the access token.
        Fetches basic shop details (name, email, domain, currency).
        """
        if not self.access_token:
            return {
                "success": False,
                "error": "SHOPIFY_ADMIN_ACCESS_TOKEN is missing. Please provide the Admin API access token (starts with shpat_...)",
            }
        
        if not self.store_url:
            return {
                "success": False,
                "error": "SHOPIFY_STORE_URL is missing. Please set your Shopify store domain.",
            }

        endpoint = f"{self.base_api_url}/shop.json"
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json().get("shop", {})
                return {
                    "success": True,
                    "shop_name": data.get("name"),
                    "shop_id": data.get("id"),
                    "email": data.get("email"),
                    "myshopify_domain": data.get("myshopify_domain"),
                    "domain": data.get("domain"),
                    "currency": data.get("currency"),
                    "timezone": data.get("iana_timezone"),
                    "plan_name": data.get("plan_name"),
                }
            elif response.status_code == 401:
                return {
                    "success": False,
                    "status_code": 401,
                    "error": "Authentication failed (401 Unauthorized). Verify that your SHOPIFY_ADMIN_ACCESS_TOKEN is valid and the app is installed.",
                }
            elif response.status_code == 403:
                return {
                    "success": False,
                    "status_code": 403,
                    "error": "Forbidden (403). Check that your Custom App has the required Admin API scopes (e.g. read_products, write_products).",
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text,
                }
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

    def create_draft_product(
        self,
        title: str,
        body_html: str,
        price: float,
        compare_at_price: Optional[float] = None,
        vendor: str = BRAND_NAME,
        product_type: str = "Pet Supplies",
        tags: Optional[List[str]] = None,
        sku: Optional[str] = None,
        aliexpress_id: Optional[str] = None,
        images: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Creates a product in Shopify strictly in DRAFT status (Rule #3 compliance).
        """
        if not self.access_token:
            return {
                "success": False,
                "error": "Cannot create product: SHOPIFY_ADMIN_ACCESS_TOKEN is missing.",
            }

        endpoint = f"{self.base_api_url}/products.json"
        
        all_tags = list(tags or [])
        all_tags.append("PawPawDoo-AI-Generated")
        if aliexpress_id:
            all_tags.append(f"AliExpress-ID:{aliexpress_id}")
        if sku:
            all_tags.append(f"DSers-SKU:{sku}")

        # Construct single or multi-variant product payload
        variant_payload: Dict[str, Any] = {
            "price": f"{price:.2f}",
            "requires_shipping": True,
        }
        if compare_at_price:
            variant_payload["compare_at_price"] = f"{compare_at_price:.2f}"
        if sku:
            variant_payload["sku"] = sku

        product_data = {
            "product": {
                "title": title,
                "body_html": body_html,
                "vendor": vendor,
                "product_type": product_type,
                "status": "draft",  # Strict DRAFT mode (Rule #3)
                "published": False,  # Never publish live without confirmation
                "tags": ", ".join(all_tags),
                "variants": [variant_payload],
            }
        }

        if images:
            product_data["product"]["images"] = images

        try:
            response = requests.post(endpoint, headers=self.headers, json=product_data, timeout=15)
            if response.status_code in (200, 201):
                created = response.json().get("product", {})
                return {
                    "success": True,
                    "product_id": created.get("id"),
                    "title": created.get("title"),
                    "status": created.get("status"),
                    "admin_graphql_api_id": created.get("admin_graphql_api_id"),
                    "shopify_admin_edit_url": f"https://admin.shopify.com/store/yprdke-mi/products/{created.get('id')}",
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text,
                }
        except Exception as e:
            return {"success": False, "error": f"Failed to create draft product: {str(e)}"}

    def push_approved_draft_product(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes the multi-agent state and publishes a complete, high-converting
        product draft to Shopify Admin (Rule #3 compliant).
        """
        research = state.get("product_research")
        storefront = state.get("storefront_offer")
        
        if not research or not storefront:
            return {"success": False, "error": "State is missing product_research or storefront_offer."}

        logistics = research.supplier_logistics
        marketplace = research.marketplace

        # Generate rich DTC HTML description
        value_props_html = "".join(f"<li>🐾 <strong>{vp}</strong></li>" for vp in storefront.value_propositions)
        
        bundles_html = ""
        for tier in storefront.offer_tiers:
            bonus = tier.get("free_bonus", "")
            bonus_html = f" | <em>Bonus: {bonus}</em>" if bonus else ""
            bundles_html += f"""
            <div style="border: 1px solid #C86432; border-radius: 8px; padding: 12px; margin-bottom: 10px; background-color: #FAF8F5;">
                <h4 style="color: #37281D; margin: 0 0 5px 0;">{tier.get('title')} — <strong>${tier.get('price'):.2f}</strong></h4>
                <p style="margin: 0; color: #555; font-size: 14px;">Badge: <strong>{tier.get('badge')}</strong>{bonus_html}</p>
            </div>
            """

        body_html = f"""
        <div class="pawpawdoo-product-description" style="font-family: Arial, sans-serif; color: #37281D; line-height: 1.6;">
            <div style="background-color: #C86432; color: #FAF8F5; padding: 12px 16px; border-radius: 6px; font-weight: bold; margin-bottom: 16px;">
                🚀 {storefront.logistics_badge}
            </div>

            <h2 style="color: #C86432; font-size: 24px; margin-bottom: 8px;">{storefront.hero_headline}</h2>
            <p style="font-size: 16px; margin-bottom: 16px;">{storefront.hero_subheadline}</p>

            <hr style="border: none; border-top: 1px solid #E5E0D8; margin: 20px 0;" />

            <h3 style="color: #37281D; font-size: 20px;">Why Pet Parents Choose PawPawDoo:</h3>
            <ul style="list-style-type: none; padding-left: 0; margin-bottom: 20px;">
                {value_props_html}
            </ul>

            <hr style="border: none; border-top: 1px solid #E5E0D8; margin: 20px 0;" />

            <h3 style="color: #37281D; font-size: 20px;">🔥 Limited-Time Bundle Packs:</h3>
            {bundles_html}

            <hr style="border: none; border-top: 1px solid #E5E0D8; margin: 20px 0;" />

            <div style="background-color: #FAF8F5; border-left: 4px solid #C86432; padding: 16px; border-radius: 4px;">
                <h4 style="color: #C86432; margin-top: 0;">🛡️ 30-Night 'Tail-Wagging' Guarantee</h4>
                <p style="margin-bottom: 0;">{storefront.guarantee_risk_reversal}</p>
            </div>
        </div>
        """

        tags = [
            "PawPawDoo",
            "Hero-Product",
            "Pet-Comfort",
            "Orthopedic-Bed",
            f"Warehouse-{logistics.selected_warehouse}",
            f"AliExpress-ID:{logistics.aliexpress_product_id}",
            f"DSers-SKU:{logistics.dsers_sku}",
            "30-Day-Guarantee",
        ]

        return self.create_draft_product(
            title=research.product_name,
            body_html=body_html,
            price=research.selling_price,
            compare_at_price=round(research.selling_price * 1.30, 2),
            vendor=BRAND_NAME,
            product_type="Pet Comfort & Sleep Wellness",
            tags=tags,
            sku=logistics.dsers_sku,
            aliexpress_id=logistics.aliexpress_product_id,
        )

    def create_or_update_page(
        self,
        title: str,
        body_html: str,
        handle: str = "cloud-dog-bed-landing",
        published: bool = False,
    ) -> Dict[str, Any]:
        """
        Creates or updates a custom landing page in Shopify Pages.
        Respects Rule #3 (Draft/unpublished by default).
        """
        endpoint = f"{self.base_api_url}/pages.json"
        payload = {
            "page": {
                "title": title,
                "body_html": body_html,
                "handle": handle,
                "published": published,
            }
        }

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload, timeout=15)
            if response.status_code in (200, 201):
                created = response.json().get("page", {})
                return {
                    "success": True,
                    "page_id": created.get("id"),
                    "title": created.get("title"),
                    "handle": created.get("handle"),
                    "shopify_admin_edit_url": f"https://admin.shopify.com/store/yprdke-mi/pages/{created.get('id')}",
                    "public_url": f"https://{self.store_url}/pages/{created.get('handle')}",
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text,
                }
        except Exception as e:
            return {"success": False, "error": f"Failed to sync Shopify page: {str(e)}"}

