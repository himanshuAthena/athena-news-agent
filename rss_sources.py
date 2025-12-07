import feedparser
from config import GOOGLE_ALERT_FEEDS, LINKEDIN_HASHTAG_FEEDS

def fetch_google_alerts(max_items=10):
    items = []
    for url in GOOGLE_ALERT_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:max_items]:
                items.append({
                    "title": entry.title,
                    "description": entry.summary if "summary" in entry else "",
                    "url": entry.link,
                    "source": "Google Alerts",
                    "is_competitor": False
                })
        except Exception as e:
            print("Google Alerts RSS error:", e)
    return items

def fetch_linkedin_posts(max_items=5):
    items = []
    for url in LINKEDIN_HASHTAG_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:max_items]:
                items.append({
                    "title": entry.title,
                    "description": entry.summary,
                    "url": entry.link,
                    "source": "LinkedIn Hashtag",
                    "is_competitor": False
                })
        except Exception as e:
            print("LinkedIn RSS error:", e)
    return items
