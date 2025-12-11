# slack_client.py
import json
import requests
from typing import Optional
from config import SLACK_WEBHOOK_URL


def send_slack_message(text: str) -> None:
    """
    Send a simple text message to Slack using an incoming webhook.
    If no webhook is configured, just print to console.
    """
    if not SLACK_WEBHOOK_URL:
        print("⚠ No SLACK_WEBHOOK_URL configured. Message that would be sent:")
        print("-------------------------------------------------------------")
        print(text)
        print("-------------------------------------------------------------")
        return

    payload = {"text": text}

    try:
        resp = requests.post(
            SLACK_WEBHOOK_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        if resp.status_code != 200:
            print(f"Slack returned non-200 status: {resp.status_code} {resp.text}")
    except Exception as exc:
        print(f"Error sending message to Slack: {exc}")
