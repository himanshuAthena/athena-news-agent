# monitordaily_scraper.py

from datetime import datetime, date
from typing import Dict, Optional
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


def fetch_monitordaily_today() -> Optional[Dict]:
    print("🔍 Fetching MonitorDaily main article...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-sandbox",
            ],
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1400, "height": 900},
            ignore_https_errors=True,
        )

        page = context.new_page()

        # Load the homepage
        page.goto(MONITOR_HOME, wait_until="domcontentloaded", timeout=60000)

        # 🔥 IMPORTANT: Scroll to trigger lazy loading in headless mode
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)

        html = page.content()

        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # Find the main article block
    block = soup.select_one("div.jeg_postblock_content")
    if not block:
        print("⚠ Could not find article block (headless mode HTML differs).")
        return None

    # Extract title + URL
    title_link = block.select_one("h3.jeg_post_title a")
    if not title_link:
        print("⚠ Title not found.")
        return None

    title = title_link.get_text(strip=True)
    url = title_link.get("href")

    # Extract date
    date_span = block.select_one("div.jeg_meta_date")
    date_text = date_span.get_text(strip=True) if date_span else ""
    published_at = parse_date(date_text)

    # Extract excerpt
    excerpt_tag = block.select_one("div.jeg_post_excerpt p")
    excerpt = excerpt_tag.get_text(strip=True) if excerpt_tag else ""

    # Validate today
    if not published_at:
        print("⚠ Could not parse article date.")
        return None

    if published_at.date() != date.today():
        print("📅 No new MonitorDaily article today.")
        return None

    return {
        "title": title,
        "url": url,
        "excerpt": excerpt,
        "published_at": published_at,
        "source": "MonitorDaily",
    }
