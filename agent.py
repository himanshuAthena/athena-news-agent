from news_sources import fetch_market_news
from rss_sources import fetch_google_alerts, fetch_linkedin_posts
from summarize import summarize_batch
from slack_client import format_for_slack, send_to_slack

def run():
    print("Fetching NewsAPI…")
    articles = fetch_market_news()
    print("NewsAPI returned:", len(articles))

    # 1️⃣ NewsAPI fallback
    if not articles:
        print("No NewsAPI results → Fetching Google Alerts RSS…")
        google_articles = fetch_google_alerts()
        print("Google Alerts returned:", len(google_articles))
        articles = google_articles

    # 2️⃣ Google Alerts fallback
    if not articles:
        print("No Google Alerts → Fetching LinkedIn RSS…")
        linkedin_articles = fetch_linkedin_posts()
        print("LinkedIn returned:", len(linkedin_articles))
        articles = linkedin_articles

    # 3️⃣ If STILL nothing, send default message
    if not articles:
        articles = [{
            "title": "No major news detected today.",
            "description": "But the agent is running correctly.",
            "url": "",
            "source": "System"
        }]

    print("Total final articles:", len(articles))

    summaries = summarize_batch(articles)
    msg = format_for_slack(summaries)
    send_to_slack(msg)

    print("DONE")
