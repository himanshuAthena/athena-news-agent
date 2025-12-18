# agent.py
from __future__ import annotations

import re
from datetime import datetime
from typing import List, Dict

from monitor_daily import fetch_monitordaily
from efa import fetch_efa_headlines
from techcrunch import fetch_techcrunch_headlines
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
        msg += "\n_No MonitorDaily main article published today._\n"

    # Extra headlines
    if extra:
        msg += "\n*More MonitorDaily Headlines:*\n\n"
        top_n = 5
        shown = extra[:top_n]

        for art in shown:
            msg += f"👉 <{art['url']}|{art['title']}>\n\n"

        if len(extra) > top_n:
            remaining = len(extra) - top_n
            msg += f"_…and {remaining} more headlines not shown._\n"

    return msg.strip()


def slack_format_efa(articles: List[Dict]) -> str:
    if not articles:
        return "*Equipment Finance Today's Headlines*\n\n_No headlines found._"

    msg = "*Equipment Finance Today's Headlines*\n\n"

    for art in articles:
        msg += f"👉 <{art['url']}|{art['title']}>\n\n"

    return msg.strip()


def slack_format_techcrunch(articles: List[Dict]) -> str:
    if not articles:
        return "*🤖 Tech & AI — TechCrunch*\n\n_No headlines found._"

    msg = "*🤖 Tech & AI — TechCrunch*\n\n"

    for art in articles:
        msg += f"🧠 <{art['url']}|{art['title']}>\n\n"

    return msg.strip()


# --------------------------------------------------
# MAIN BOT
# --------------------------------------------------
def main():
    print("=== Equipment Finance News Bot (Playwright) ===")

    # 1️⃣ MonitorDaily
    md_data = fetch_monitordaily()

    # 2️⃣ EFA
    efa_articles = fetch_efa_headlines()

    # 3️⃣ TechCrunch
    tech_articles = fetch_techcrunch_headlines()

    # 4️⃣ Build Slack message
    md_section = slack_format_monitor(md_data)
    efa_section = slack_format_efa(efa_articles)
    tech_section = slack_format_techcrunch(tech_articles)

    final_message = (
        md_section
        + "\n\n"
        + efa_section
        + "\n\n"
        + tech_section
    )

    print("\n===== MESSAGE TO SEND =====\n")
    print(final_message)
    print("\n===========================\n")

    # 5️⃣ Send to Slack
    send_slack_message(final_message)


if __name__ == "__main__":
    main()
