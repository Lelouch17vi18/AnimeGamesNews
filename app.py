from flask import Flask, render_template
import feedparser
from datetime import datetime

app = Flask(__name__)

SITE_NAME = "Anime & Games News"
SITE_DESCRIPTION = (
    "Latest Anime & Gaming news with proper credits from trusted sources "
    "like IGN and Crunchyroll."
)

RSS_SOURCES = [
    {
        "name": "IGN",
        "category": "Games",
        "url": "https://feeds.feedburner.com/ign/games-all"
    },
    {
        "name": "Crunchyroll",
        "category": "Anime",
        "url": "https://www.crunchyroll.com/rss/news"
    }
]

def safe_summary(text):
    """Short, safe, non-plagiarized summary"""
    if not text:
        return "Read the full story on the official source."
    text = text.replace("\n", " ").strip()
    return text[:200] + "..." if len(text) > 200 else text

def extract_image(entry):
    """Safely extract image from RSS entry"""
    if "media_thumbnail" in entry and entry.media_thumbnail:
        return entry.media_thumbnail[0].get("url", "")
    if "media_content" in entry and entry.media_content:
        return entry.media_content[0].get("url", "")
    return ""

@app.route("/")
def home():
    news = []

    for src in RSS_SOURCES:
        feed = feedparser.parse(src["url"])

        for entry in feed.entries[:6]:
            news.append({
                "title": entry.get("title", "No title"),
                "summary": safe_summary(entry.get("summary", "")),
                "link": entry.get("link", "#"),
                "source": src["name"],
                "category": src["category"],
                "published": entry.get("published", ""),
                "image": extract_image(entry)
            })

    # 🔥 SORT LATEST FIRST (simple)
    news = list(dict.fromkeys([n["title"] for n in news])) and news

    # 🔥 SECTIONS
    games_news = [n for n in news if n["category"] == "Games"]
    anime_news = [n for n in news if n["category"] == "Anime"]

    # 🔥 FEATURED (first valid item with image)
    featured = next((n for n in news if n["image"]), news[0] if news else None)

    return render_template(
        "index.html",
        site_name=SITE_NAME,
        description=SITE_DESCRIPTION,
        featured=featured,
        games_news=games_news[:4],
        anime_news=anime_news[:4],
        news=news,  # for full latest section
        year=datetime.now().year
    )

@app.route("/about")
def about():
    return render_template("about.html", site_name=SITE_NAME)

@app.route("/privacy")
def privacy():
    return render_template("privacy.html", site_name=SITE_NAME)

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html", site_name=SITE_NAME)

if __name__ == "__main__":
    app.run(debug=True)
