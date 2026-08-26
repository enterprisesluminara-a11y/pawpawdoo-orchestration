"""
Shopify Connection Verification Script.
Tests your Shopify Admin API credentials and verifies permissions.
"""

import os
import sys
from dotenv import load_dotenv

# Load fresh environment variables
load_dotenv(override=True)

from adapters.shopify_adapter import ShopifyAdapter
from config import SHOPIFY_ADMIN_ACCESS_TOKEN, SHOPIFY_STORE_URL


def main():
    print("=" * 60)
    print("[PawPawDoo] Shopify Admin API Connection Diagnostic")
    print("=" * 60)
    print(f"Store URL Configured : {SHOPIFY_STORE_URL}")
    token_preview = (
        f"{SHOPIFY_ADMIN_ACCESS_TOKEN[:10]}... ({len(SHOPIFY_ADMIN_ACCESS_TOKEN)} chars)"
        if SHOPIFY_ADMIN_ACCESS_TOKEN
        else "[NOT SET in .env]"
    )
    print(f"Admin Access Token   : {token_preview}")
    print("-" * 60)

    if not SHOPIFY_ADMIN_ACCESS_TOKEN:
        print("[!] SHOPIFY_ADMIN_ACCESS_TOKEN is missing in your .env file.")
        print("[*] Follow the step-by-step instructions in the chat to generate and paste your token.")
        sys.exit(1)

    adapter = ShopifyAdapter()
    print("Testing connection to Shopify Admin API...")
    result = adapter.test_connection()

    if result.get("success"):
        print("[+] SUCCESS: Successfully authenticated with Shopify Admin API!")
        print(f"   * Shop Name        : {result.get('shop_name')}")
        print(f"   * Primary Domain   : {result.get('domain')}")
        print(f"   * MyShopify Domain : {result.get('myshopify_domain')}")
        print(f"   * Currency         : {result.get('currency')}")
        print(f"   * Plan             : {result.get('plan_name')}")
        print(f"   * Timezone         : {result.get('timezone')}")
        print("-" * 60)
        print("[+] Guardrail Status: Rule #3 (Strict DRAFT Mode) is ACTIVE.")
        print("   All multi-agent generated products will be created safely in DRAFT status.")
    else:
        print(f"[-] Connection Failed: {result.get('error')}")
        if result.get("status_code") == 401:
            print("[?] Tip: Ensure the token begins with 'shpat_' and has not been revoked.")
        elif result.get("status_code") == 403:
            print("[?] Tip: Verify scopes in Shopify Custom App: read_products, write_products.")
        sys.exit(1)


if __name__ == "__main__":
    main()

