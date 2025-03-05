import os
from flask import Blueprint, g, request, jsonify
import feedparser
from bs4 import BeautifulSoup

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# List of RSS feed URLs
feed_urls = [
    "https://88bamboo.co/blogs/news.atom",  # Latest News
    "https://88bamboo.co/blogs/whisky-rum-gin-vodka-distillery-spotlight.atom",  # Spotlight
    "https://88bamboo.co/blogs/whisky-reviews.atom",  # Reviews
]

@blueprint.route("/rssfeed", methods= ['GET'])
def fetchRSS():
    # Define category names for each feed (same order as feed_urls)
    categories = ["latest_news", "spotlight", "reviews"]

    # List to store nested articles
    news_data = []

    # Iterate through each RSS feed URL and category
    for i, feed_url in enumerate(feed_urls):
        # Parse the RSS feed
        feed = feedparser.parse(feed_url)

        # Get feed category (fallback to 'general_news' if index out of range)
        category = categories[i] if i < len(categories) else "general_news"

        # Ensure there are entries in the feed
        num_entries = min(4, len(feed.entries))  # Limit to 4 articles per source

        # List to store articles from this feed
        articles = []

        for j in range(num_entries):
            entry = feed.entries[j]

            # Extract content safely
            content = None
            if "content" in entry:
                content = entry.content[0].value
            elif "summary" in entry:
                content = entry.summary
            elif "description" in entry:
                content = entry.description
            else:
                content = "No content available"

            # Extract image from content
            image_url = None
            if content:
                soup = BeautifulSoup(content, "html.parser")
                img = soup.find("img")
                if img and "src" in img.attrs:
                    image_url = img["src"]

            # Store article in dictionary format
            article_data = {
                "title": entry.get("title", "No title"),
                "published": entry.get("published", "Unknown date"),
                "link": entry.get("link", "No link"),
                "image_url": image_url,
            }

            # Append article to the list
            articles.append(article_data)

        # Append category-wise articles to news_data
        news_data.append({category: articles})
    return jsonify(news_data)
