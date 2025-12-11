# config.py
import os

# Slack Incoming Webhook (optional)
# Set this in your environment:
#   Windows PowerShell:  $env:SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/...."
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "").strip() or None

# Keywords / companies you care about
KEYWORDS = [
    "Solifi",
    "Odessa",
    "LTi",
    "Netsol",
    "LeasePath",
    "ALS",
    "Dominion",
    "Turbo Lease",
]

# Common User-Agent to make Playwright look more like a browser
USER_AGENT = os.getenv(
    "NEWSBOT_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36",
)

# How many articles to consider from each site
MAX_ARTICLES_PER_SOURCE = 30
