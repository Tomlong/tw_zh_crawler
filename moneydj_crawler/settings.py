import os

NEWS_URL = "https://www.moneydj.com/KMDJ/News/NewsRealList.aspx?index1={}&a=MB010000"
URL_PREFIX = "https://www.moneydj.com"

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "moneydj_data")
URL_DB_NAME = os.getenv("URL_DB_NAME", "news_url")
ARTICLE_DB_NAME = os.getenv("ARTICLE_DB_NAME", "article_data")
HTML_DB_NAME = os.getenv("HTML_DB_NAME", "html_data")
