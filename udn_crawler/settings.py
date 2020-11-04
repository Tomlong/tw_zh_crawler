import os

ARTICLE_URL_PREFIX = "https://udn.com/"
API_BASE_URL = "https://udn.com/api/more"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
}

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "udn_data")
URL_DB_NAME = os.getenv("URL_DB_NAME", "news_url")
ARTICLE_DB_NAME = os.getenv("ARTICLE_DB_NAME", "article_data")
HTML_DB_NAME = os.getenv("HTML_DB_NAME", "html_data")
