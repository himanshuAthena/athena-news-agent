# agent.py
from __future__ import annotations

import re
from datetime import datetime
from typing import List, Dict

from monitor_daily import fetch_monitordaily   # UPDATED IMPORT
from efa import fetch_efa_headlines
from slack_client import send_slack_message


# --------------------------------------------------
# CLEAN TITLE LOGIC (MonitorDaily only)
# --------------------------------------------------
def clean_title(full_title: str) -> str:
    """Cleans MonitorDaily article titles by removing prefixes."""
    parts = re.split(r"\?|-|:|\u2013|\u2014", full_title)
    clean = parts[-1].strip()
    return clean if clean else full_title.strip()


# --------------------------------------------------
# Slack Formatters
# --------------------------------------------------
def slack_format_monitor(md: Dict) -> str:
    today_str = datetime.now().strftime("%B %d, %Y")

    main = md.get("main_article")
    extra = md.get("extra_articles", [])

    msg = f"*Monitor Daily Today — {today_str}*\n"

    # Main headline
    if main:
        title = clean_title(main["title"])
        url = main["url"]
        msg += f"\n👉 <{url}|{title}>\n"
    else:
        msg += "\nNo MonitorDaily main article published today.\n"

    # Extra headlines
    if extra:
        msg += "\n*More MonitorDaily Headlines:*\n\n"
        top_n = 5
        shown = extra[:top_n]
        for art in shown:
            msg += f"👉 <{art['url']}|{art['title']}>\n\n"

        if len(extra) > top_n:
            remaining = len(extra) - top_n
            msg += f"_...and {remaining} more headlines not shown._\n"

    return msg.strip()


def slack_format_efa(articles: List[Dict]) -> str:
    if not articles:
        return "*Equipment Finance Today's Headlines*\n\nNo headlines found."

    msg = "*Equipment Finance Today's Headlines*\n\n"

    for art in articles:
        msg += f"👉 <{art['url']}|{art['title']}>\n\n"

    return msg.strip()



# --------------------------------------------------
# MAIN BOT
# --------------------------------------------------
def main():
    print("=== Equipment Finance News Bot (Playwright) ===")

    # 1️⃣ Fetch MonitorDaily data (main + extra)
    md_data = fetch_monitordaily()

    # 2️⃣ Fetch EFA headlines
    efa_articles = fetch_efa_headlines()

    # 3️⃣ Build Slack message
    md_section = slack_format_monitor(md_data)
    efa_section = slack_format_efa(efa_articles)

    final_message = md_section + "\n\n" + efa_section

    print("\n===== MESSAGE TO SEND =====\n")
    print(final_message)
    print("\n===========================\n")

    # 4️⃣ Send to Slack
    send_slack_message(final_message)


if __name__ == "__main__":
    main()
