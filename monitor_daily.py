# monitor_daily.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

URL = "https://www.monitordaily.com/news/"

def apply_stealth(page):
    """
    Injects JavaScript to remove Playwright fingerprints.
    Similar to puppeteer-extra-stealth.
    """
    page.add_init_script("""
        // Remove playwright detection
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

        // Fake plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3],
        });

        // Fake languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });

        // Fake Chrome object
        window.chrome = {
            runtime: {},
            loadTimes: () => {},
            csi: () => {},
        };

        // WebGL fingerprint patch
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(param) {
            if (param === 37445) return 'Intel Inc.';
            if (param === 37446) return 'Intel Iris OpenGL Engine';
            return getParameter(param);
        };
    """)


def fetch_monitor_daily(max_items=8):
    print("Fetching MonitorDaily using Playwright (custom stealth)…")

    with sync_playwright() as p:
        # Launch real-like browser
        browser = p.chromium.launch(
            headless=True,   # TURN ON WINDOW FIRST FOR DEBUG — will switch later
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--window-size=1400,900"
            ]
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1400, "height": 900},
            screen={"width": 1400, "height": 900},
            device_scale_factor=1,
            java_script_enabled=True
        )

        page = context.new_page()

        # Apply stealth before navigation
        apply_stealth(page)

        page.goto(URL, wait_until="networkidle", timeout=120000)

        # Allow Cloudflare JS challenge to complete
        page.wait_for_timeout(5000)

        html = page.content()

        context.close()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # Try known article selectors
    selectors = [
        "article.post",
        "div.story",
        ".post-item",
        "article",
        ".entry",
    ]

    articles_html = []
    for sel in selectors:
        items = soup.select(sel)
        if items:
            print(f"Found articles using selector: {sel}")
            articles_html = items
            break

    if not articles_html:
        print("❌ NO ARTICLES — here is the first part of page:")
        print(html[:800])
        return []

    results = []
    cutoff = datetime.utcnow() - timedelta(days=2)

    for block in articles_html:
        title_tag = block.select_one("h3 a, h2 a, a")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        url = title_tag.get("href", "")

        summary_tag = block.select_one("p, .entry-summary, .summary")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""

        date_tag = block.select_one("time, .date")
        date_str = date_tag.get_text(strip=True) if date_tag else ""

        published_dt = None
        try:
            published_dt = datetime.strptime(date_str, "%B %d, %Y")
        except:
            pass

        if not published_dt or published_dt >= cutoff:
            results.append({
                "title": title,
                "description": summary,
                "url": url,
                "published_at": published_dt.isoformat() if published_dt else None
            })

        if len(results) >= max_items:
            break

    print(f"MonitorDaily articles selected: {len(results)}")
    return results
