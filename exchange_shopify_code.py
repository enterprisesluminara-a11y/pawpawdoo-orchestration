"""
Shopify OAuth Code Exchange Script.
Exchanges authorization code from Shopify OAuth redirect into a permanent Admin Access Token.
"""

import os
import sys
import urllib.parse
import requests
from dotenv import load_dotenv

load_dotenv(override=True)


def exchange_code(raw_input_code_or_url: str):
    raw_input_code_or_url = raw_input_code_or_url.strip()
    
    # Extract code if full URL was pasted
    if "code=" in raw_input_code_or_url:
        parsed = urllib.parse.urlparse(raw_input_code_or_url)
        query_params = urllib.parse.parse_qs(parsed.query)
        code = query_params.get("code", [None])[0]
    else:
        code = raw_input_code_or_url

    if not code:
        print("[-] Error: Could not extract authorization code.")
        return False

    client_id = os.getenv("SHOPIFY_CLIENT_ID")
    client_secret = os.getenv("SHOPIFY_CLIENT_SECRET")
    store_url = os.getenv("SHOPIFY_STORE_URL", "04mhqd-6w.myshopify.com")

    print("=" * 60)
    print("[PawPawDoo] Exchanging OAuth Code for Admin Access Token...")
    print("=" * 60)
    print(f"Store        : {store_url}")
    print(f"Client ID    : {client_id}")
    print(f"Auth Code    : {code[:12]}...")

    endpoint = f"https://{store_url}/admin/oauth/access_token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access_token")
            scopes = data.get("scope")
            print("[+] SUCCESS! Permanent Shopify Admin Access Token generated!")
            print(f"   * Token  : {access_token[:12]}... (length: {len(access_token)})")
            print(f"   * Scopes : {scopes}")
            
            # Update .env file automatically
            env_path = os.path.join(os.path.dirname(__file__), ".env")
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            updated = False
            new_lines = []
            for line in lines:
                if line.startswith("SHOPIFY_ADMIN_ACCESS_TOKEN="):
                    new_lines.append(f"SHOPIFY_ADMIN_ACCESS_TOKEN={access_token}\n")
                    updated = True
                elif line.startswith("SHOPIFY_STORE_URL="):
                    new_lines.append(f"SHOPIFY_STORE_URL={store_url}\n")
                else:
                    new_lines.append(line)

            if not updated:
                new_lines.append(f"\nSHOPIFY_ADMIN_ACCESS_TOKEN={access_token}\n")

            with open(env_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            print("[+] .env file successfully updated with new SHOPIFY_ADMIN_ACCESS_TOKEN and SHOPIFY_STORE_URL!")
            return True
        else:
            print(f"[-] Token exchange failed (Status {response.status_code}): {response.text}")
            return False
    except Exception as e:
        print(f"[-] Request error during exchange: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        exchange_code(sys.argv[1])
    else:
        user_code = input("Paste your authorization code or redirected URL: ")
        exchange_code(user_code)

