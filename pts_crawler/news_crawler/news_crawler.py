import time
import pymongo
import logging
import requests
from bs4 import BeautifulSoup
from settings import NEWS_URL, ARTICLE_URL_PREFIX, MONGO_URI, URL_DB_NAME, DB_NAME

logger = logging.getLogger(__name__)


def get_newest_article_id():
    res = requests.get(NEWS_URL)
    soup = BeautifulSoup(res.text, "html.parser")
    news_info_soups = soup.find_all("figure")
    for news_info_soup in news_info_soups:
        # 直到找到最新一篇 article_id 為止
        try:
            newest_article_id = news_info_soup.find("a").get("href").split("/")[-1]
        except:
            continue
    return newest_article_id

def start_crawl(collection):
    newest_article_id = get_newest_article_id()
    oldest_job = collection.find_one({}, sort=[("_id", pymongo.DESCENDING)])
    if oldest_job is None:
        oldest_article_id = newest_article_id
    else:
        oldest_article_id = oldest_job["url"].split("/")[-1]

    for article_id in range(int(newest_article_id), 0, -1):
        news_url = f"{ARTICLE_URL_PREFIX}/{str(article_id)}"
        result = collection.find_one({"url": news_url})
        if not result:
            collection.insert_one({"url": news_url, "status": "pending"})
        # url 已存在，且最舊的是第一篇新聞
        else:
            if oldest_article_id == "1":
                break


def execute_job(db, interval=1):
    collection = db[URL_DB_NAME]
    while True:
        try:
            start_crawl(collection)
        except Exception as e:
            logger.info(f"Crawl news url error: {e}")
            time.sleep(interval)

        logger.info("Waiting for newest news url.")
        time.sleep(interval)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mongo_client = pymongo.MongoClient(MONGO_URI)

    try:
        mongo_client.server_info()
    except:
        logger.warning("MongoDB is not connected.")
        exit()

    db = mongo_client[DB_NAME]
    execute_job(db)
