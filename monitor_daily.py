# monitordaily_scraper.py

from datetime import datetime, date
from typing import Dict, Optional, List
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

MONITOR_HOME = "https://www.monitordaily.com/"


def parse_date(text: str) -> Optional[datetime]:
    """Convert strings like 'December 11, 2025' into datetime."""
    text = text.strip()
    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(text, fmt)
        except:
            pass
    return None


def fetch_monitordaily() -> Dict:
    """
    Returns:
    {
      "main_article": {...} OR None,
      "extra_articles": [ {...}, {...}, ... ]
    }
    """

    print("🔍 Fetching MonitorDaily articles...")

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

        page.goto(MONITOR_HOME, wait_until="domcontentloaded", timeout=60000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # ============================================
    # 1️⃣ MAIN DAILY ARTICLE
    # ============================================
    block = soup.select_one("div.jeg_postblock_content")

    main_article = None

    if block:
        title_link = block.select_one("h3.jeg_post_title a")
        if title_link:
            title = title_link.get_text(strip=True)
            url = title_link["href"]

            date_span = block.select_one("div.jeg_meta_date")
            date_text = date_span.get_text(strip=True) if date_span else ""
            published_at = parse_date(date_text)

            excerpt_tag = block.select_one("div.jeg_post_excerpt p")
            excerpt = excerpt_tag.get_text(strip=True) if excerpt_tag else ""

            if published_at and published_at.date() == date.today():
                main_article = {
                    "title": title,
                    "url": url,
                    "excerpt": excerpt,
                    "published_at": published_at,
                    "source": "MonitorDaily",
                }

    # ============================================
    # 2️⃣ EXTRA HEADLINES (below main article)
    # ============================================
    extra_articles: List[Dict] = []

    posts_container = soup.select_one("div.jeg_posts.jeg_load_more_flag")
    if posts_container:
        for post in posts_container.select("article.jeg_post"):
            a = post.select_one("h3.jeg_post_title a")
            if not a:
                continue

            title = a.get_text(strip=True)
            url = a["href"]

            extra_articles.append({"title": title, "url": url})

    print(f"✔ Main article: {'found' if main_article else 'none today'}")
    print(f"✔ Extra headlines found: {len(extra_articles)}")

    return {
        "main_article": main_article,
        "extra_articles": extra_articles
    }
