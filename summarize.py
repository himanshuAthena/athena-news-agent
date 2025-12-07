from openai import OpenAI
import json
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an analyst for a B2B SaaS startup called Athena Fintech.
You summarize fintech, leasing, lending, rental, and accounting industry news.

For each article:
- Give 2–3 bullet summary points.
- Assign one tag:
  Competitor / Regulation / Market / Technology / AI / Funding / Other
- Suggest 1 short action idea for Athena Fintech.

Return valid JSON with:
summary_bullets, tag, action_idea
"""

def summarize_article(article):
    title = article.get("title", "")
    desc = article.get("description", "")
    url = article.get("url", "")

    user_prompt = f"Title: {title}\nDescription: {desc}\nURL: {url}"

    response = client.responses.create(
        model="gpt-4.1-mini",
        reasoning={"effort": "low"},
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )

    data = json.loads(response.output[0].content[0].text)

    return {
        "title": title,
        "url": url,
        "summary_bullets": data.get("summary_bullets", []),
        "tag": data.get("tag", "Other"),
        "action_idea": data.get("action_idea", ""),
        "is_competitor": article.get("is_competitor", False),
        "competitor_name": article.get("competitor_name"),
    }

def summarize_batch(list_of_articles):
    results = []
    for article in list_of_articles:
        try:
            results.append(summarize_article(article))
        except Exception as e:
            print("Error:", e)
    return results
