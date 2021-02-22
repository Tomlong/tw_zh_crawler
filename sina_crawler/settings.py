import os

START_URL = "https://news.sina.com.cn/roll/#pageid=153&lid=2516&etime={}&stime={}&ctime={}&date={}&k=&num=50&page={}"
TITLE_IGNORE_TEXT = "原标题："

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "sina_data")
URL_DB_NAME = os.getenv("URL_DB_NAME", "news_url")
ARTICLE_DB_NAME = os.getenv("ARTICLE_DB_NAME", "article_data")
HTML_DB_NAME = os.getenv("HTML_DB_NAME", "html_data")

YEARS_RANGE = int(os.getenv("YEARS_RANGE", 3))
