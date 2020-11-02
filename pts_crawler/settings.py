import os

NEWS_URL = "https://news.pts.org.tw/dailynews"
ARTICLE_URL_PREFIX = "https://news.pts.org.tw/article"
USELESS_CATEGORIES = ["Foreign"]

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "pts_data")
URL_DB_NAME = os.getenv("URL_DB_NAME", "news_url")
ARTICLE_DB_NAME = os.getenv("ARTICLE_DB_NAME", "article_data")
HTML_DB_NAME = os.getenv("HTML_DB_NAME", "html_data")
