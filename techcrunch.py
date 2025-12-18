# techcrunch.py
from typing import List, Dict
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

TECHCRUNCH_LATEST = "https://techcrunch.com/"


def fetch_techcrunch_headlines(limit: int = 6) -> List[Dict]:
    """
    Fetch latest TechCrunch headlines (title + url).
    Works in headless mode & GitHub Actions.
    """
    print("🤖 Fetching TechCrunch latest news...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ],
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1500, "height": 1000},
            ignore_https_errors=True,
        )

        page = context.new_page()
        page.goto(TECHCRUNCH_LATEST, wait_until="domcontentloaded", timeout=60000)

        # Scroll to ensure lazy-loaded cards appear
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2500)

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    articles: List[Dict] = []

    # TechCrunch story cards
    cards = soup.select("li.wp-block-post")

    for card in cards:
        a = card.select_one("a.loop-card__title-link")
        if not a:
            continue

        title = a.get_text(strip=True)
        url = a.get("href")

        # Basic sanity check
        if not title or not url:
            continue

        articles.append({
            "title": title,
            "url": url,
            "source": "TechCrunch",
        })

        if len(articles) >= limit:
            break

    print(f"✅ TechCrunch headlines found: {len(articles)}")
    return articles
