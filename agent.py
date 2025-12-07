from news_sources import fetch_market_news
from summarize import summarize_batch
from slack_client import format_for_slack, send_to_slack
from rss_sources import fetch_google_alerts, fetch_linkedin_posts



def run():
    print("Fetching NewsAPI articles...")
    articles = fetch_market_news()

    # If NewsAPI gives nothing → fetch Google Alerts
    if not articles:
        print("No NewsAPI results. Fetching Google Alerts...")
        articles = fetch_google_alerts()

    # If still nothing → fetch LinkedIn RSS posts
    if not articles:
        print("No Google Alerts. Fetching LinkedIn hashtag posts...")
        articles = fetch_linkedin_posts()

    print(f"Found {len(articles)} articles")

    summaries = summarize_batch(articles)

    formatted = format_for_slack(summaries)
    send_to_slack(formatted)

    print("Done")


if __name__ == "__main__":
    run()
