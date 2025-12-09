# agent.py
from monitor_daily import fetch_monitor_daily
from summarize import summarize_batch
from slack_client import send_to_slack

def format_message(summaries):
    if not summaries:
        return "No MonitorDaily highlights found today."

    lines = []
    lines.append("*MonitorDaily – Latest Equipment Finance News*\n")

    for i, art in enumerate(summaries, 1):
        title = art["title"]
        url = art["url"]
        bullets = art.get("bullets", [])

        # Headline
        lines.append(f"*{i}. {title}*")

        # Bullets
        for b in bullets:
            lines.append(b)

        # Link
        lines.append(url)
        lines.append("")  # blank line

    return "\n".join(lines)



def run():
    print("=== MonitorDaily News Bot ===")

    articles = fetch_monitor_daily(max_items=5)
    print("Fetched:", len(articles))

    summaries = summarize_batch(articles)
    print("Summaries:", len(summaries))

    msg = format_message(summaries)

    print("\n===== DAILY HIGHLIGHTS =====\n")
    print(msg)
    print("\n============================\n")

    send_to_slack(msg)


if __name__ == "__main__":
    run()
