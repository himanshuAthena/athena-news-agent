# efa_scraper.py

from typing import List, Dict
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

EFA_HOME = "https://www.equipmentfa.com/"


def fetch_efa_headlines() -> List[Dict]:
    """
    Scrape Equipment Finance Advisor homepage and return a list of:
    { title, url, source }
    """
    print("🔍 Fetching EFA homepage headlines...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(EFA_HOME, wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(2000)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    articles = []

    # Select all <div class="newsContent"> blocks
    blocks = soup.select("div.newsContent")
    for block in blocks:
        text_div = block.select_one("div.text")
        if not text_div:
            continue

        # Extract title & URL from first <a>
        a = text_div.find("a")
        if not a:
            continue

        title = a.get_text(strip=True)
        url = a.get("href", "").strip()

        if not title or not url:
            continue

        articles.append({
            "title": title,
            "url": url,
            "source": "Equipment Finance Advisor",
        })

    print(f"  ✅ EFA headlines found: {len(articles)}")
    return articles
