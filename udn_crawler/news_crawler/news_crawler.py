import time
import random
import pymongo
import logging
import datetime
import requests
from settings import HEADERS, ARTICLE_URL_PREFIX, API_BASE_URL, MONGO_URI, URL_DB_NAME, DB_NAME

logger = logging.getLogger(__name__)


def _start_crawl(collection, news_list):
    for news_item in news_list:
        news_link = news_item["titleLink"]
        url = f"{ARTICLE_URL_PREFIX}{news_link}"
        news_datetime = datetime.datetime.strptime(news_item["time"]["date"], "%Y-%m-%d %H:%M")
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
        

def start_crawl(collection, crawl_interval=0.5):
    logger.info("Start crawl urls")

    page = 1
    while True:
        channelId = 1
        # 不分類
        cate_id = 99
        # 即時新聞
        news_type = "breaknews"
        query = f"page={page}&channelId={channelId}&cate_id={cate_id}&type={news_type}"
        news_list_url = API_BASE_URL + '?' + query

        r = requests.get(news_list_url, headers=HEADERS)
        news_data = r.json()
        if "lists" not in news_data:
            logger.info(f"Crawl to last page: {page}")
            break

        news_list = news_data["lists"]
        _start_crawl(collection, news_list)
        page += 1

        time.sleep(random.uniform(0.1, 0.2))


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
