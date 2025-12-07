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

    for q in MARKET_QUERIES:
        all_articles.extend(_search(q, from_date))

    for c in COMPETITORS:
        articles = _search(c, from_date)
        for a in articles:
            a["is_competitor"] = True
            a["competitor_name"] = c
        all_articles.extend(articles)

    unique = []
    seen = set()
    for a in all_articles:
        url = a.get("url")
        if url and url not in seen:
            seen.add(url)
            unique.append(a)

    return unique
