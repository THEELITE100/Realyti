#Team Newbie Coders 
#Realyti-Let's have a Check!!!
from flask import Flask, render_template_string, request, redirect, url_for
import feedparser
from bs4 import BeautifulSoup
import csv
import ast
import random
import os

app = Flask(__name__)

# Define the path to your HTML file
desktop_path = r"C:\Users\Rudra Verma\Desktop\index.html.html"

# Define excluded words for each category
excluded_words = {
    'world': ['ukraine'],
}

# Function to determine whether a news article is likely fake or real
def is_news_real(headline):
    # Implement your logic here to determine if the news is real or fake
    # For demonstration purposes, let's assume any news containing the word "scandal" is likely fake
    if 'scandal' in headline.lower():
        return False
    else:
        return True

@app.route('/', methods=['GET', 'POST'])
def index():
    # Handle search form submission
    if request.method == 'POST':
        search_query = request.form.get('query', '')
        if search_query:
            return redirect(url_for('search_results', query=search_query))

    try:
        # Read the content of the HTML file
        with open(desktop_path, 'r') as file:
            template_content = file.read()
    except FileNotFoundError:
        # Handle the case when the file is not found
        template_content = "HTML file not found"

    # Fetch top headlines and latest articles from Google News RSS feed
    top_headlines_feed = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    top_headlines = parse_rss_feed(top_headlines_feed, limit=20)

    latest_articles_feed = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    latest_articles = parse_rss_feed(latest_articles_feed, limit=20)

    # Pass the fetched articles to the HTML template for rendering
    return render_template_string(template_content, top_headlines=top_headlines, latest_articles=latest_articles)

@app.route('/search', methods=['GET'])
def search_results():
    # Get the search query from the URL parameters
    search_query = request.args.get('query', '')

    # Fetch latest articles from Google News RSS feed
    latest_articles_feed = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    latest_articles = parse_rss_feed(latest_articles_feed, limit=20)

    # Filter articles based on search query
    searched_articles = filter_articles_by_search_query(latest_articles, search_query)

    try:
        # Read the content of the HTML file
        with open(desktop_path, 'r') as file:
            template_content = file.read()
    except FileNotFoundError:
        # Handle the case when the file is not found
        template_content = "HTML file not found"

    # Pass the fetched articles to the HTML template for rendering
    return render_template_string(template_content, top_headlines=[], latest_articles=searched_articles, search_query=search_query)

@app.route('/go_back', methods=['GET'])
def go_back():
    # Handle the back button functionality
    # You can implement your logic here to determine the previous page
    # For simplicity, let's just redirect to the main page
    return redirect(url_for('index'))

def parse_rss_feed(feed_url, limit=20):
    feed = feedparser.parse(feed_url)
    entries = []
    for entry in feed.entries[:limit]:  # Limit to specified number of entries
        entry_data = {
            'title': entry.title,
            'summary': extract_summary(entry),
            'link': entry.link,
            'image_url': extract_image_url(entry),
            'is_real': is_news_real(entry.title)  # Determine if the news is real or fake
        }
        entries.append(entry_data)
    return entries

def extract_summary(entry):
    soup = BeautifulSoup(entry.summary, 'html.parser')
    return soup.get_text()

def extract_image_url(entry):
    soup = BeautifulSoup(entry.summary, 'html.parser')
    img_tag = soup.find('img')
    if img_tag:
        return img_tag['src']
    return None

def filter_articles_by_search_query(articles, search_query):
    # Filtering articles based on search query logic
    return [article for article in articles if search_query.lower() in article['title'].lower()]

if __name__ == '_main_':
    app.run(debug=True)
