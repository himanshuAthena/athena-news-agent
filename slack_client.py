import requests
from collections import defaultdict
from config import SLACK_WEBHOOK_URL

def format_for_slack(summaries):
    if not summaries:
        return "No relevant industry news found in the last 24 hours."

    grouped = defaultdict(list)
    for s in summaries:
        grouped[s["tag"]].append(s)

    lines = []
    lines.append("*Athena Daily Market Intelligence* :newspaper:")
    lines.append("_Automated report for the last 24 hours_\n")

    for tag, items in grouped.items():
        lines.append(f"*{tag}*")
        for s in items[:4]:
            bullets = "\n".join(f"• {b}" for b in s["summary_bullets"])
            comp = f" _(Competitor: {s['competitor_name']})_" if s.get("is_competitor") else ""
            lines.append(
                f"*<{s['url']}|{s['title']}>*{comp}\n{bullets}\n_Action idea:_ {s['action_idea']}\n"
            )
        lines.append("")

    return "\n".join(lines)

def send_to_slack(text, channel=None):
    payload = {"text": text}
    resp = requests.post(SLACK_WEBHOOK_URL, json=payload)
    resp.raise_for_status()
