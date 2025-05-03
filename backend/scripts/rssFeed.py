# Routes: /rssfeed (GET)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, request, jsonify
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# List of RSS feed URLs
feed_urls = [
    "https://88bamboo.co/blogs/news.atom",  # Latest News
    "https://88bamboo.co/blogs/brand-spotlights.atom",  # Spotlight
    "https://88bamboo.co/blogs/whisky-reviews.atom",  # Whiskey Reviews
    "https://88bamboo.co/blogs/features.atom",  # Features
    "https://88bamboo.co/blogs/interviews.atom",  # Interviews
    "https://88bamboo.co/blogs/escapades.atom",  # Escapades
    "https://88bamboo.co/blogs/whats-on.atom",  # What's Happening
]

reviews_url = [
    "https://88bamboo.co/blogs/whisky-reviews.atom",  # Whiskey Reviews
    "https://88bamboo.co/blogs/craft-beer-reviews.atom",  # Craft Beer Reviews
    "https://88bamboo.co/blogs/wine-reviews.atom",  # Wine Reviews
    "https://88bamboo.co/blogs/sake-reviews.atom",  # Sake Reviews
    "https://88bamboo.co/blogs/rum-reviews.atom",  # Rum Reviews
]

@blueprint.route("/rssfeed", methods= ['GET'])
def fetchRSS():
    # Define category names for each feed (same order as feed_urls)
    categories = ["latest_news", "spotlight", "reviews", "features", "interviews", "escapades", "whats_on"]

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

@blueprint.route("/rssfeedreviews", methods=['GET'])
def fetchRSSReviews():
    # Define category names for each feed (same order as feed_urls)
    categories = ["whiskey", "craft_beer", "wine", "sake", "rum"]

    # Flat list to store all articles
    news_data = []

    # Iterate through each RSS feed URL and category
    for i, feed_url in enumerate(reviews_url):
        # Parse the RSS feed
        feed = feedparser.parse(feed_url)

        # Get feed category (fallback to 'general_news' if index out of range)
        category = categories[i] if i < len(categories) else "general_news"

        # Ensure there are entries in the feed
        num_entries = min(5, len(feed.entries))  # Limit to 5 articles per source

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

            # Parse the published date
            published_date = entry.get("published", "Unknown date")
            
            # Try to convert string date to datetime object for sorting
            try:
                # Attempt to parse the date (feedparser often provides standard format)
                published_datetime = datetime.strptime(published_date, "%a, %d %b %Y %H:%M:%S %z")
            except (ValueError, TypeError):
                try:
                    # Try a different common format if the first fails
                    published_datetime = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S%z")
                except (ValueError, TypeError):
                    # If parsing fails, use current time as fallback
                    published_datetime = datetime.now()

            # Store article in dictionary format with category
            article_data = {
                "title": entry.get("title", "No title"),
                "published": published_date,
                "published_datetime": published_datetime,  # For sorting
                "link": entry.get("link", "No link"),
                "image_url": image_url,
                "category": category
            }

            # Append article to the list
            news_data.append(article_data)

    # Sort all articles by published date (newest first)
    news_data.sort(key=lambda x: x["published_datetime"], reverse=True)
    
    # Remove the datetime objects used for sorting before returning the JSON
    for article in news_data:
        article.pop("published_datetime", None)

    return jsonify(news_data)