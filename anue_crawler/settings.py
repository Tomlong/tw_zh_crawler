import os

API_URL = "https://api.cnyes.com/media/api/v1/newslist/category/tw_stock_news"

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "anue_data")
ARTICLE_DB_NAME = os.getenv("ARTICLE_DB_NAME", "article_data")
DAY_RANGE = int(os.getenv("DAY_RANGE", 100))
START_DATE = os.getenv("START_DATE", None)
