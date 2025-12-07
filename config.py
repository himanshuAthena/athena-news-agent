import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

MARKET_QUERIES = [
    "equipment leasing software",
    "lease management SaaS",
    "asset finance software",
    "IFRS 16 lessor accounting",
    "rental management platform",
    "loan and lease management system",
    "fintech lending platform"
]

COMPETITORS = [
    "LeaseQuery",
    "Odessa leasing software",
    "ALFA Systems",
    "LTIMindtree leasing platform"
]

GOOGLE_ALERT_FEEDS = [
    # paste your Google Alerts RSS feed links here
    "https://www.google.com/alerts/feeds/13018807204136963696/10644736879458580239",
    "https://www.google.com/alerts/feeds/13018807204136963696/17538092041713281154",
    "https://www.google.com/alerts/feeds/13018807204136963696/2049279242957894042",
    "https://www.google.com/alerts/feeds/13018807204136963696/10644736879458578683",
    "https://www.google.com/alerts/feeds/13018807204136963696/17538092041713280107",
    "https://www.google.com/alerts/feeds/13018807204136963696/10644736879458579010",
    "https://www.google.com/alerts/feeds/13018807204136963696/2049279242957897225",
        
]

LINKEDIN_HASHTAG_FEEDS = [
    "https://rsshub.app/linkedin/hashtag/leasing",
    "https://rsshub.app/linkedin/hashtag/fintech",
    "https://rsshub.app/linkedin/hashtag/assetfinance",
    "https://rsshub.app/linkedin/hashtag/saas",
]

