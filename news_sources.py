import requests
from datetime import datetime, timedelta
from config import NEWS_API_KEY, MARKET_QUERIES, COMPETITORS

BASE_URL = "https://newsapi.org/v2/everything"

def _search(query, from_date):
    params = {
        "q": query,
        "from": from_date.isoformat(),
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY,
    }
    resp = requests.get(BASE_URL, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json().get("articles", [])

def fetch_market_news():
    from_date = datetime.utcnow() - timedelta(days=1)

    all_articles = []

    # normal 24h search
    for q in MARKET_QUERIES:
        all_articles.extend(_search(q, from_date))

    for c in COMPETITORS:
        articles = _search(c, from_date)
        for a in articles:
            a["is_competitor"] = True
            a["competitor_name"] = c
        all_articles.extend(articles)

    # dedupe
    unique = []
    seen = set()
    for a in all_articles:
        url = a.get("url")
        if url and url not in seen:
            seen.add(url)
            unique.append(a)

    # if no news found → get fallback recent articles
    if not unique:
        print("No 24h news. Fetching fallback recent articles.")
        return fetch_recent_backup()

    return unique



def fetch_recent_backup():
    params = {
        "q": "equipment leasing OR lease accounting OR asset finance OR rental management OR fintech lending",
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY,
    }
    
    resp = requests.get(BASE_URL, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json().get("articles", [])


    return unique
