import feedparser
from config import GOOGLE_ALERT_FEEDS, LINKEDIN_HASHTAG_FEEDS

def fetch_google_alerts(max_items=10):
    items = []

    print("Fetching Google Alerts RSS feeds…")
    print("Feed URLs:", GOOGLE_ALERT_FEEDS)

    for url in GOOGLE_ALERT_FEEDS:
        try:
            feed = feedparser.parse(url)

            print(f"Parsed feed: {url} — Entries: {len(feed.entries)}")

            for entry in feed.entries[:max_items]:
                items.append({
                    "title": entry.title,
                    "description": entry.summary if "summary" in entry else "",
                    "url": entry.link,
                    "source": "Google Alerts"
                })

        except Exception as e:
            print("Google Alerts RSS error:", e)

    print("Total Google Alerts articles:", len(items))
    return items


def fetch_linkedin_posts(max_items=5):
    items = []

    print("Fetching LinkedIn Hashtag RSS feeds…")
    print("Feed URLs:", LINKEDIN_HASHTAG_FEEDS)

    for url in LINKEDIN_HASHTAG_FEEDS:
        try:
            feed = feedparser.parse(url)

            print(f"Parsed LinkedIn feed: {url} — Entries: {len(feed.entries)}")

            for entry in feed.entries[:max_items]:
                items.append({
                    "title": entry.title,
                    "description": entry.summary,
                    "url": entry.link,
                    "source": "LinkedIn RSS"
                })

        except Exception as e:
            print("LinkedIn RSS error:", e)

    print("Total LinkedIn articles:", len(items))
    return items
