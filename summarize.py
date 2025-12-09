# summarize.py
import requests
from textwrap import shorten
from config import HUGGINGFACE_API_TOKEN

HF_MODEL_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"


def _hf_summarize(text: str) -> str:
    """Call HuggingFace summarizer API."""
    if not text:
        return ""

    headers = {"Content-Type": "application/json"}
    if HUGGINGFACE_API_TOKEN:
        headers["Authorization"] = f"Bearer {HUGGINGFACE_API_TOKEN}"

    payload = {
        "inputs": text,
        "parameters": {
            "min_length": 40,
            "max_length": 120,
            "do_sample": False
        }
    }

    try:
        resp = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=40)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, list) and "summary_text" in data[0]:
            return data[0]["summary_text"].strip()

        return shorten(text, width=350, placeholder="…")

    except Exception as e:
        print("[Summarizer] Error:", e)
        return shorten(text, width=350, placeholder="…")


def summarize_article(article: dict) -> dict:
    """Summarize a single article into bullet points."""
    title = article.get("title", "").strip()
    desc = article.get("description", "").strip()
    url = article.get("url", "")

    combined = f"{title}. {desc}" if desc else title
    combined = combined.strip()

    summary_text = _hf_summarize(combined)

    # convert summary → bullet points (max 3)
    bullets = []
    for sentence in summary_text.split(". "):
        s = sentence.strip(" .")
        if len(s) > 20:
            bullets.append(f"• {s}")

        if len(bullets) >= 3:
            break

    return {
        "title": title,
        "url": url,
        "bullets": bullets
    }


def summarize_batch(articles):
    """Summarize a list of articles."""
    results = []
    for i, article in enumerate(articles, start=1):
        print(f"[Summarizer] Processing {i}/{len(articles)}")
        try:
            results.append(summarize_article(article))
        except Exception as e:
            print("[Summarizer] Skipping article due to error:", e)
    return results
