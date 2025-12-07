import requests
from collections import defaultdict
from config import SLACK_WEBHOOK_URL

def format_for_slack(summaries):
    if not summaries:
        return "No relevant industry news found."

    lines = []
    lines.append("*Athena Daily Market Intelligence* :newspaper:")
    
    # Add this:
    if len(summaries) < 3:
        lines.append("_Showing latest recent articles (no new updates in last 24h)_\n")
    else:
        lines.append("_Automated report for the last 24 hours_\n")


def send_to_slack(text, channel=None):
    payload = {"text": text}
    resp = requests.post(SLACK_WEBHOOK_URL, json=payload)
    resp.raise_for_status()
