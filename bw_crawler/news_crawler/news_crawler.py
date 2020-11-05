import time
import random
import pymongo
import logging
import requests
from bs4 import BeautifulSoup
from settings import (
    HEADERS,
    ARTICLE_URL_PREFIX,
    API_BASE_URL,
    MONGO_URI,
    URL_DB_NAME,
    DB_NAME,
)

logger = logging.getLogger(__name__)


def start_crawl(collection):
    logger.info("Start crawl urls")

    current_page = 0
    while True:
        data = {"CurPage": current_page}
        res = requests.post(API_BASE_URL, headers=HEADERS, data=data)
        html_content = res.json()["Content"]
        if html_content is None:
            logger.info("Finish crawl all today's news.")
            break
        
        soup = BeautifulSoup(html_content, "html.parser")
        article_soups = soup.find_all("figcaption", class_="Article-img-caption")
        
        for article_soup in article_soups:
            news_link = article_soup.a["href"]
            url = f"{ARTICLE_URL_PREFIX}{news_link}"
            # 雜誌類忽略，因為內容格式不同
            if "magazine" in news_link:
                continue

            result = collection.find_one({"url": url})
            if result:
                continue

            logger.info(f"get url: {url}")
            collection.insert_one(
                {
                    "url": url,
                    "status": "pending"
                }
            )

        current_page += len(article_soups)
        time.sleep(random.uniform(0.1, 0.2))


def execute_job(db, interval=60):
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
