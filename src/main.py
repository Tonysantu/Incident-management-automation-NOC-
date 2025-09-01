"""
main.py
Incident automation entry point
- P1, P2: DM engineer via Discord bot, wait for ACK, then assign
- P3, P4: Direct resolver assignment
"""

import json
import time
from sheets import get_resolver_mapping, get_oncall_list
from servicenow import assign_to_group

QUEUE_FILE = "../alerts/discord_queue.json"
ACK_FILE = "../alerts/ack_status.json"


def enqueue_discord_alert(engineer, alert):
    """Write alert to queue for Discord bot to pick up."""
    try:
        with open(QUEUE_FILE, "r") as f:
            queue = json.load(f)
    except Exception:
        queue = []

    queue.append({
        "alert_id": alert["alert_id"],
        "severity": alert["severity"],
        "message": alert["message"],
        "name": engineer["name"],
        "discord_id": engineer["discord_id"],
        "resolver_group": engineer["resolver_group"]
    })

    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f)

    print(f"[main] Queued alert {alert['alert_id']} for {engineer['name']}")


def wait_for_ack(engineer, alert, timeout=120):
    """Check ack_status.json for ACK reply."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with open(ACK_FILE, "r") as f:
                ack_status = json.load(f)
        except Exception:
            ack_status = {}

        if ack_status.get(str(engineer["discord_id"]), False):
            print(f"[main] ✅ {engineer['name']} acknowledged alert {alert['alert_id']}")
            return True

        time.sleep(5)  # poll every 5s
    print(f"[main] ❌ Timeout: No ACK from {engineer['name']} for alert {alert['alert_id']}")
    return False


def handle_p1_p2(alert):
    """Handle P1 and P2 incidents via Discord bot + ACK check."""
    engineers = get_oncall_list(alert)
    if not engineers:
        print(f"[main] ❌ No engineers in oncall_schedule for {alert['severity']}")
        return False

    for engineer in engineers:
        enqueue_discord_alert(engineer, alert)
        if wait_for_ack(engineer, alert, timeout=120):
            assign_to_group(alert, engineer["resolver_group"])
            print(f"[main] Incident {alert['alert_id']} assigned to {engineer['resolver_group']}")
            return True
        else:
            print(f"[main] Escalating alert {alert['alert_id']} to next engineer...")

    print(f"[main] ❌ Escalation exhausted for {alert['severity']} alert {alert['alert_id']}")
    return False


def handle_p3_p4(alert):
    """Handle P3/P4 incidents with direct resolver group mapping."""
    mapping = get_resolver_mapping()
    message = alert.get("message", "")
    server_name = message.split()[-1]  # simple extraction
    group = mapping.get(server_name, "DefaultOpsGroup")
    assign_to_group(alert, group)


def handle_alert(alert):
    """Dispatch handler based on severity."""
    severity = alert.get("severity")
    if severity in ["P1", "P2"]:
        handle_p1_p2(alert)
    elif severity in ["P3", "P4"]:
        handle_p3_p4(alert)
    else:
        print(f"[main] Unknown severity {severity}, skipping.")


if __name__ == "__main__":
    with open("../alerts/alerts.json", "r") as f:
        alerts = json.load(f)

    for alert in alerts:
        print(f"\n[main] Processing alert {alert['alert_id']} with severity {alert['severity']}")
        handle_alert(alert)
