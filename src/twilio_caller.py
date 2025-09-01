"""
twilio_caller.py
Stub functions for Twilio phone call integration.
Replace with real Twilio API later.
"""

def call_engineer(engineer: dict, retries: int = 3) -> bool:
    """
    Stub: pretend to call engineer by phone.
    In real use, you'd use Twilio API to make the call.
    """
    for i in range(retries):
        print(f"[twilio] Calling {engineer['name']} ({engineer['phone']}) (attempt {i+1})...")
    # For now, simulate no answer
    return False
