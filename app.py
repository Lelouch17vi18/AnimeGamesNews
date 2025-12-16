from flask import Flask, render_template
import feedparser
from datetime import datetime

app = Flask(__name__)

SITE_NAME = "Anime & Games News"
SITE_DESCRIPTION = "Latest Anime & Gaming news with proper credits from trusted sources like IGN and Crunchyroll."

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
    """Short, non-plagiarized, safe summary"""
    if not text:
        return "Read the full story on the official source."
    text = text.replace("\n", " ").strip()
    return text[:200] + "..." if len(text) > 200 else text

@app.route("/")
def home():
    news = []

    for src in RSS_SOURCES:
        feed = feedparser.parse(src["url"])
        for entry in feed.entries[:6]:
            # Try to get image safely
            image_url = ""
            if "media_thumbnail" in entry:
                image_url = entry.media_thumbnail[0]["url"]
            elif "media_content" in entry:
                image_url = entry.media_content[0]["url"]

            news.append({
                "title": entry.title,
                "summary": safe_summary(entry.get("summary", "")),
                "link": entry.link,
                "source": src["name"],
                "category": src["category"],
                "published": entry.get("published", ""),
                "image": image_url
            })

    return render_template(
        "index.html",
        site_name=SITE_NAME,
        description=SITE_DESCRIPTION,
        news=news,
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
