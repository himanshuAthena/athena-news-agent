# agent.py
from __future__ import annotations

import re
from datetime import datetime, date
from typing import List, Dict

from monitor_daily import fetch_monitordaily_today
from efa import fetch_efa_headlines
from slack_client import send_slack_message


# --------------------------------------------------
# CLEAN TITLE LOGIC (MonitorDaily only)
# --------------------------------------------------
def clean_title(full_title: str) -> str:
    """
    Extracts the clean readable part of a MonitorDaily title.
    Example:
    "What Will Shape EF in 2026? Mitsubishi HC Capital America Identifies Four Key Trends"
        --> "Mitsubishi HC Capital America Identifies Four Key Trends"
    """
    parts = re.split(r"\?|-|:|\u2013|\u2014", full_title)
    clean = parts[-1].strip()
    return clean if clean else full_title.strip()


# --------------------------------------------------
# Slack Message Formatters
# --------------------------------------------------
def slack_format_monitor(md_article: Dict) -> str:
    """Format MonitorDaily into Slack message with clickable clean title."""
    today_str = datetime.now().strftime("%B %d, %Y")

    if not md_article:
        return f"*Monitor Daily Today — {today_str}*\n\nNo MonitorDaily article found today."

    title = md_article.get("title", "Untitled Article").strip()
    title = clean_title(title)

    url = md_article.get("url", "").strip()
    clickable = f"<{url}|{title}>"

    return f"*Monitor Daily Today — {today_str}*\n\n{clickable}"


def slack_format_efa(articles: List[Dict]) -> str:
    """Format EFA headlines."""
    if not articles:
        return "*EFA Today's Headlines*\n\nNo headlines found."

    lines = ["*EFA Today's Headlines*\n"]

    for art in articles:
        title = art["title"]
        url = art["url"]
        link = f"<{url}|{title}>"
        lines.append(link)

    return "\n".join(lines)


# --------------------------------------------------
# MAIN BOT
# --------------------------------------------------
def main():
    print("=== Equipment Finance News Bot (Playwright) ===")

    # 1️⃣ MonitorDaily (single daily article)
    md_article = fetch_monitordaily_today()

    # 2️⃣ EFA headlines (multiple)
    efa_articles = fetch_efa_headlines()

    # 3️⃣ Build Slack message
    md_section = slack_format_monitor(md_article)
    efa_section = slack_format_efa(efa_articles)

    final_message = md_section + "\n\n" + efa_section

    print("\n===== MESSAGE TO SEND =====\n")
    print(final_message)
    print("\n===========================\n")

    # 4️⃣ Send to Slack
    # send_slack_message(final_message)


if __name__ == "__main__":
    main()
