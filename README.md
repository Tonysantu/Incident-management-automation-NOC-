# Incident-management-automation-NOC-
Automated the assignation of tickets according to priority
# 🚨 Incident Automation (P1–P4 Workflow)

## 📌 Overview
This project automates incident management by integrating:
- **Google Sheets** → on-call schedule & resolver groups
- **Discord Bot** → DM engineers, wait for ACKs
- **ServiceNow** → auto-create & assign incidents

✅ Built as a portfolio project to showcase **DevOps / SRE automation skills**.  
✅ Handles **P1–P4** with escalation logic like a mini PagerDuty.  

---

## 🔹 Workflow
- **P1/P2**
  1. Bot looks up on-call engineer from Google Sheets
  2. Sends Discord DM: "Reply ACK to confirm"
  3. Waits 120s for ACK → if none, escalates
  4. On ACK → incident assigned in ServiceNow
- **P3/P4**
  - Auto-assign directly to resolver group (from Google Sheets)

---

## 🔹 Tech Stack
- Python 3.11
- discord.py
- gspread + Google Service Account
- ServiceNow REST API
- JSON queue for bot–script communication

## 🔹 Possible Improvements

This project already implements a full P1–P4 incident workflow using Discord, Google Sheets, and ServiceNow. Below are some optional improvements that can make it production-grade and even more impressive:

🔹 Twilio Escalation (Optional for P1)
Integrate Twilio API to make automated phone calls when no ACK is received in Discord.
Ensures that critical P1 incidents are never missed.
Configurable retries (e.g., 3 attempts per engineer).

🔹 Discord Channel Logging
In addition to DMing the on-call engineer, post all P1/P2 incidents in a team channel (e.g., #incidents).
Improves visibility for the whole team.
🔹 Centralized Logging

Add a logger.py that writes to incident.log.

Logs every alert, ACK, escalation, and ServiceNow assignment.

Helps in audits and post-incident reviews.

🔹 Config File
Move credentials and constants (Discord bot token, ServiceNow instance, Google Sheet name) into config.py.
Easier to maintain and avoids hardcoding in multiple files.

🔹 Web Dashboard (Optional)
Add a Streamlit dashboard to visualize alerts and ACKs in real time.
Example features:
List of current alerts from alerts.json.
ACK status (✅ or ⏳) from ack_status.json.
Resolver groups and ServiceNow incident numbers.

