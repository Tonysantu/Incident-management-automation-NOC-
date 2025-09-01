import discord
import asyncio
import json
import os

BOT_TOKEN = "DISCORD_BOT_TOKEN"
QUEUE_FILE = "../alerts/discord_queue.json"
ACK_FILE = "../alerts/ack_status.json"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

ack_status = {}

@client.event
async def on_ready():
    print(f"[discord] Bot logged in as {client.user}")
    client.loop.create_task(process_queue())

async def process_queue():
    """Continuously check for new alerts to send."""
    while True:
        if os.path.exists(QUEUE_FILE):
            with open(QUEUE_FILE, "r+") as f:
                try:
                    alerts = json.load(f)
                except json.JSONDecodeError:
                    alerts = []
                f.truncate(0)
            if alerts:
                for item in alerts:
                    await send_incident(item)
        await asyncio.sleep(5)  # check every 5s

async def send_incident(alert):
    """Send DM to engineer from alert data."""
    try:
        user_id = int(alert["discord_id"])
        user = await client.fetch_user(user_id)
        dm = await user.create_dm()
        await dm.send(
            f"🚨 Incident {alert['alert_id']} ({alert['severity']}): {alert['message']}\n"
            f"Reply 'ACK' within 120s to confirm."
        )
        print(f"[discord] Sent alert {alert['alert_id']} to {alert['name']}")
    except Exception as e:
        print(f"[discord] ❌ Failed to DM {alert['name']}: {e}")

@client.event
async def on_message(message):
    """Listen for ACK replies."""
    if message.author == client.user:
        return
    if message.content.strip().upper() == "ACK":
        ack_status[str(message.author.id)] = True
        with open(ACK_FILE, "w") as f:
            json.dump(ack_status, f)
        await message.channel.send("✅ ACK received! Incident acknowledged.")

client.run(BOT_TOKEN)
