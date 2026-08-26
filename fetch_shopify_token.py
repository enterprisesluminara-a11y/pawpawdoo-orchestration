"""
Shopify Auto-Token Fetcher.
Exchanges verified Client ID and Client Secret for an Admin API Access Token.
"""

import os
import re
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv(override=True)


def fetch_token():
    client_id = os.getenv("SHOPIFY_CLIENT_ID", "")
    client_secret = os.getenv("SHOPIFY_CLIENT_SECRET", "")
    store = os.getenv("SHOPIFY_STORE_URL", "yprdke-mi.myshopify.com")

    print(f"Target Store : {store}")
    print(f"Client ID    : {client_id}")
    print(f"Secret       : {client_secret[:12]}...")

    r = requests.post(
        f"https://{store}/admin/oauth/access_token",
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
        token = data.get("access_token")
        print("=" * 60)
        print("[+] SUCCESS! Token exchange completed!")
        print(f"   * Admin Access Token : {token[:12]}... (length: {len(token)})")
        print(f"   * Granted Scopes     : {data.get('scope')}")
        print("=" * 60)

        # Update .env
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        with open(env_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(r"SHOPIFY_ADMIN_ACCESS_TOKEN=.*", f"SHOPIFY_ADMIN_ACCESS_TOKEN={token}", content)
        content = re.sub(r"SHOPIFY_STORE_URL=.*", f"SHOPIFY_STORE_URL={store}", content)

        with open(env_path, "w", encoding="utf-8") as f:
            f.write(content)

        print("[+] .env file successfully updated with SHOPIFY_ADMIN_ACCESS_TOKEN!")
        return token
    else:
        if "<title>" in r.text:
            match = re.search(r"<title>(.*?)</title>", r.text)
            err_title = match.group(1) if match else "Error"
            print(f"[-] Status {r.status_code}: {err_title}")
        else:
            print(f"[-] Status {r.status_code}: {r.text[:200]}")
        return None


if __name__ == "__main__":
    fetch_token()

