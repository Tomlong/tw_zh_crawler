import re
import time
import pymongo
import logging
import datetime
import requests
from bs4 import BeautifulSoup
from settings import NEWS_URL, MONGO_URI, URL_DB_NAME, DB_NAME, DAY_RANGE

logger = logging.getLogger(__name__)


def record_news_urls(collection, hrefs):
    for href in hrefs:
        url = href.get("href")
        if collection.find_one({"url": url}):
            continue

        logger.info(f"Record url: {url}")
        collection.insert_one({"url": url, "status": "pending"})


def _start_crawl(collection, assign_datetime):
    year = str(assign_datetime.year)
    month = "{:02d}".format(assign_datetime.month)
    day = "{:02d}".format(assign_datetime.day)

    year_month = year + month
    today = year_month + day
    href_pattern = "^http://finance.jrj.com.cn/{}/{}\/{}[0-9]+\.shtml$".format(
        year, month, day
    )

    page = 1
    while True:
        page_url = NEWS_URL.format(year_month, today, page)
        try:
            res = requests.get(page_url)
            res.raise_for_status()

            soup = BeautifulSoup(res.text, "html.parser")
            hrefs = soup.find_all("a", href=re.compile(href_pattern))
            record_news_urls(collection, hrefs)
        except:
            break
        page += 1


def start_crawl(collection):
    start_datetime = datetime.datetime.now()
    assign_datetime = datetime.datetime.now()
    while True:
        diff_datetime = start_datetime - assign_datetime
        # 超過指定時限
        if diff_datetime.days > DAY_RANGE:
            logger.info(
                f"Crawl over {DAY_RANGE} days, so stop and wait for newest news."
            )
            break
        try:
            _start_crawl(collection, assign_datetime)

        except Exception as e:
            logger.info(f"Crawl {assign_datetime} error: {e}")

        assign_datetime -= datetime.timedelta(1)


def execute_job(db, interval=300):
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
