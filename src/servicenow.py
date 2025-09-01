import requests
from requests.auth import HTTPBasicAuth

# ---- CONFIG: update these ----
INSTANCE = "https://dev249430.service-now.com"   # your instance
USER = "admin"                                   # your ServiceNow API user
PASSWORD = "+qdd2StP@1ZK"                        # your ServiceNow API password

def assign_to_group(alert: dict, group: str):
    """Create & assign incident in ServiceNow for P3/P4 alerts."""

    url = f"{INSTANCE}/api/now/table/incident"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Map P3/P4 to ServiceNow numeric priorities
    priority_map = {"P3": "3", "P4": "4"}
    priority = priority_map.get(alert.get("severity"), "4")

    data = {
        "short_description": alert.get("message", "Auto-generated alert"),
        "assignment_group": group,    # group must exist in ServiceNow
        "priority": priority,
        "caller_id": USER
    }

    try:
        response = requests.post(
            url,
            auth=HTTPBasicAuth(USER, PASSWORD),
            headers=headers,
            json=data
        )

        if response.status_code == 201:
            inc_number = response.json()["result"]["number"]
            print(f"[servicenow] ✅ Incident created: {inc_number}, assigned to {group}")
            return inc_number
        else:
            print(f"[servicenow] ❌ Failed: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print("[servicenow] Exception:", e)
        return None
