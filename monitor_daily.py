# monitordaily_scraper.py

from datetime import datetime, date
from typing import Dict, Optional
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

MONITOR_HOME = "https://www.monitordaily.com/"


def parse_date(text: str) -> Optional[datetime]:
    """Convert 'December 11, 2025' into datetime."""
    text = text.strip()
    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(text, fmt)
        except:
            pass
    return None


def fetch_monitordaily_today() -> Optional[Dict]:
    """
    Scrape MonitorDaily home page and return ONLY today's main article:
    {
        "title": "...",
        "url": "...",
        "excerpt": "...",
        "published_at": datetime,
    }
    """
    print("🔍 Fetching MonitorDaily main article...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(MONITOR_HOME, wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(2000)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # The first main article block
    block = soup.find("div", class_="jeg_postblock_content")
    if not block:
        print("⚠ Could not find article block.")
        return None

    # Title + URL
    title_tag = block.find("h3", class_="jeg_post_title")
    title_link = title_tag.find("a") if title_tag else None

    if not title_link:
        print("⚠ Title not found.")
        return None

    title = title_link.get_text(strip=True)
    url = title_link.get("href")

    # Date
    date_div = block.find("div", class_="jeg_meta_date")
    date_text = date_div.get_text(strip=True).replace("", "") if date_div else ""
    # Example: "December 11, 2025"
    published_at = parse_date(date_text)

    # Excerpt
    excerpt_div = block.find("div", class_="jeg_post_excerpt")
    excerpt_p = excerpt_div.find("p") if excerpt_div else None
    excerpt = excerpt_p.get_text(strip=True) if excerpt_p else ""

    # Verify date is today
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
