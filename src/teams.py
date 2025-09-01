import requests
from typing import Optional

def post_to_teams(webhook_url: Optional[str], text: str) -> bool:
    if not webhook_url:
        print("[teams] No webhook URL configured; skipping.")
        return False
    payload = {"text": text}
    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        if resp.status_code == 200:
            print("[teams] Message posted.")
            return True
        print(f"[teams] Failed ({resp.status_code}): {resp.text}")
        return False
    except Exception as e:
        print(f"[teams] Error: {e}")
        return False
