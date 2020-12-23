import os

NEWS_URL = "http://finance.jrj.com.cn/xwk/{}/{}_{}.shtml"
DAY_RANGE = 1000

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "people_news_data")
URL_DB_NAME = os.getenv("URL_DB_NAME", "news_url")
ARTICLE_DB_NAME = os.getenv("ARTICLE_DB_NAME", "article_data")
HTML_DB_NAME = os.getenv("HTML_DB_NAME", "html_data")
