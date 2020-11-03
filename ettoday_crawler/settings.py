import os

ARTICLE_URL_PREFIX = "https://www.ettoday.net"

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "ettoday_data")
URL_DB_NAME = os.getenv("URL_DB_NAME", "news_url")
ARTICLE_DB_NAME = os.getenv("ARTICLE_DB_NAME", "article_data")
HTML_DB_NAME = os.getenv("HTML_DB_NAME", "html_data")

YEARS_RANGE = int(os.getenv("YEARS_RANGE", 2))
SCROLL_INTERVAL = 0.5
