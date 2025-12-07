from news_sources import fetch_market_news
from summarize import summarize_batch
from slack_client import format_for_slack, send_to_slack

def run():
    print("Fetching news...")
    articles = fetch_market_news()

    print(f"Found {len(articles)} articles")

    print("Summarizing...")
    summaries = summarize_batch(articles)

    print("Sending to Slack...")
    formatted = format_for_slack(summaries)
    send_to_slack(formatted)

    print("Done.")

if __name__ == "__main__":
    run()
