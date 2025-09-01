"""
sheets.py
Google Sheets integration for resolver mapping & on-call escalation.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---- CONFIG ----
SHEET_NAME = "IncidentConfig"             # name of your Google Spreadsheet
CREDENTIALS_FILE = "gcp-key.json"         # updated name for your key file

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

def connect_sheets():
    """Authorize and return gspread client."""
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client

def get_resolver_mapping():
    """
    Fetch server_name → resolver_group mapping from Google Sheets.
    Used for P3/P4.
    """
    try:
        client = connect_sheets()
        sheet = client.open(SHEET_NAME).worksheet("resolver_mapping")
        records = sheet.get_all_records()
        mapping = {row["server_name"]: row["resolver_group"] for row in records}
        return mapping
    except Exception as e:
        print("[sheets] ⚠️ Falling back to dummy resolver mapping. Error:", e)
        return {
            "serverX": "LinuxOpsGroup",
            "serverY": "StorageTeam",
            "serverZ": "DBTeam"
        }

def get_oncall_list(alert):
    """
    Fetch escalation list for P1/P2 from Google Sheets.
    Returns list of dicts.
    """
    severity = alert.get("severity")

    try:
        client = connect_sheets()
        sheet = client.open(SHEET_NAME).worksheet("oncall_schedule")
        records = sheet.get_all_records()

        engineers = [
            {
                "name": row["name"],
                "discord_id": row["discord_id"],
                "phone": row["phone_number"],   # optional for Twilio later
                "resolver_group": row["resolver_group"],
                "order": int(row["order"])
            }
            for row in records if row["priority"] == severity
        ]
        engineers.sort(key=lambda x: x["order"])   # ✅ fixed sorting
        return engineers

    except Exception as e:
        print("[sheets] ⚠️ Falling back to dummy oncall list. Error:", e)
        dummy = {
            "P1": [
                {"name": "Alice", "discord_id": "alice#1234", "phone": "+15551234567", "resolver_group": "DBTeam", "order": 1},
                {"name": "Bob", "discord_id": "bob#5678", "phone": "+15559876543", "resolver_group": "DBTeam", "order": 2}
            ],
            "P2": [
                {"name": "Charlie", "discord_id": "charlie#2222", "phone": "+15553456789", "resolver_group": "LinuxOpsGroup", "order": 1},
                {"name": "Dave", "discord_id": "dave#3333", "phone": "+15557654321", "resolver_group": "LinuxOpsGroup", "order": 2}
            ]
        }
        return dummy.get(severity, [])
