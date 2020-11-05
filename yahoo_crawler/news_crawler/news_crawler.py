import time
import random
import pymongo
import logging
import datetime
import requests
from settings import (
    HEADERS,
    API_PARAMS,
    ARTICLE_URL_PREFIX,
    API_BASE_URL,
    MONGO_URI,
    URL_DB_NAME,
    DB_NAME,
    QUERY_COUNT,
)

logger = logging.getLogger(__name__)


def start_crawl(collection):
    logger.info("Start crawl urls")

    start = 0
    while True:
        res = requests.get(API_BASE_URL.format(start, QUERY_COUNT), headers=HEADERS, params=API_PARAMS)
        news_list = res.json()["data"]
        if len(news_list) == 0:
            logger.info("Finish crawl all today's news.")
            break
        
        for news_item in news_list:
            if "url" not in news_item:
                continue
            news_link = news_item["url"]
            url = f"{ARTICLE_URL_PREFIX}{news_link}"
            news_datetime = datetime.datetime.fromtimestamp(news_item["published_at"])
            result = collection.find_one({"url": url})
            if result:
                continue

            logger.info(f"get url: {url}")
            collection.insert_one(
                {
                    "url": url,
                    "datetime": news_datetime,
                    "status": "pending"
                }
            )

        start += QUERY_COUNT
        time.sleep(random.uniform(0.1, 0.2))


def execute_job(db, interval=120):
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
