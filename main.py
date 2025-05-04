import requests
import datetime
from bs4 import BeautifulSoup
from pathlib import Path

TODAY = datetime.datetime.now().strftime("%B_%d")
DATE_DISPLAY = datetime.datetime.now().strftime("%B %d, %Y")

OUTPUT_DIR = Path("_posts")
OUTPUT_DIR.mkdir(exist_ok=True)

def get_cricket_history():
    url = f"https://en.wikipedia.org/wiki/{TODAY}_in_sport"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    events = []

    for li in soup.select('ul > li'):
        if 'cricket' in li.text.lower():
            events.append("- " + li.text.strip())
    return events or ["- No cricket events found."]

def get_latest_news():
    return [
        "- BCCI to announce World Cup squad tomorrow.",
        "- Pat Cummins named SRH captain for 2025."
    ]

def generate_post():
    history = get_cricket_history()
    news = get_latest_news()

    content = f\"\"\"---
title: \"Cricket Daily - {DATE_DISPLAY}\"
date: {datetime.datetime.now().isoformat()}
---

## 🏏 On this day in Cricket History
{chr(10).join(history)}

## 📰 Latest Cricket News
{chr(10).join(news)}
\"\"\"

    filename = OUTPUT_DIR / f\"{datetime.datetime.now().strftime('%Y-%m-%d')}-cricket-daily.md\"
    with open(filename, \"w\") as f:
        f.write(content.strip())

    print(f\"✅ Post generated: {filename}\")

if __name__ == \"__main__\":
    generate_post()
