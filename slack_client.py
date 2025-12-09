# slack_client.py
import requests
from config import SLACK_WEBHOOK_URL

def send_to_slack(text):
    if not SLACK_WEBHOOK_URL:
        print("[Slack] No webhook configured — skipping Slack send.")
        return

    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json={"text": text})
        resp.raise_for_status()
        print("[Slack] Message sent.")
    except Exception as e:
        print("[Slack] Error sending message:", e)
