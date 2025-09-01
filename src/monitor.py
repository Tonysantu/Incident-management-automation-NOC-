import json
from pathlib import Path
from typing import List, Dict

ALERTS_FILE = Path(__file__).resolve().parent.parent / "alerts" / "alerts.json"

def load_alerts() -> List[Dict]:
    if not ALERTS_FILE.exists():
        raise FileNotFoundError(f"Alerts file not found: {ALERTS_FILE}")
    with open(ALERTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("alerts.json should contain a list of alerts")
        return data
