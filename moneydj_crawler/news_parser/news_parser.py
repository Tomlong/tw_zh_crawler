import os
import re
import time
import json
import logging
import pymongo
import datetime
import requests
from threading import Thread
from bs4 import BeautifulSoup
from settings import MONGO_URI, URL_DB_NAME, DB_NAME, HTML_DB_NAME, ARTICLE_DB_NAME


logger = logging.getLogger(__name__)


def parse_datetime(datetime_str):
    try:
        datetime_str = "".join(datetime_str.rsplit(":", 1))
        parsed_datetime = datetime.datetime.strptime(
            datetime_str, "%Y-%m-%dT%H:%M:%S%z"
        )
    except Exception as e:
        raise Exception(f"Parse datetime error. datetime: {datetime_str}{e}")
    return parsed_datetime


def get_content(main_soup):
    return main_soup.find("article", {}).get_text().strip()


def execute_job(job, article_collection, html_collection):
    news_url = job["url"]
    logger.info(f"Parsing: {news_url}")
    res = requests.get(news_url)
    main_soup = BeautifulSoup(res.text, "html.parser")

    # Get meta
    try:
        meta_str = main_soup.find("script", type="application/ld+json").text
        # 接受 \r、\0、\t等字元
        meta = json.loads(meta_str, strict=False)
        meta["datetime"] = parse_datetime(meta["datePublished"])
        meta["content"] = get_content(main_soup)
    except:
        logger.info(f"url: {news_url} parse meta wrong!")
        raise

    article_collection.insert_one(
        {
            "title": meta["headline"],
            "content": meta["content"],
            "keywords": meta["keywords"],
            "category": meta["articleSection"],
            "datetime": meta["datetime"],
        }
    )

    # save html if finish job
    html_collection.insert_one({"html_text": res.text})


def parse_job(parse_interval=0.1):
    mongo_client = pymongo.MongoClient(MONGO_URI)
    try:
        mongo_client.server_info()
    except:
        logger.warning("MongoDB is not connected.")
        raise
    db = mongo_client[DB_NAME]
    url_collection = db[URL_DB_NAME]
    article_collection = db[ARTICLE_DB_NAME]
    html_collection = db[HTML_DB_NAME]

    logger.info("Starting news parser...")
    while True:
        try:
            job = url_collection.find_one_and_update(
                {"status": "pending"}, {"$set": {"status": "parsing"}}
            )
            if not job:
                logger.info("Waiting for new jobs...")
                time.sleep(parse_interval)
                continue
        except Exception as e:
            logger.exception(f"Get job error: {e}")
            url_collection.find_one_and_update(
                {"_id": job["_id"]}, {"$set": {"status": "error"}}
            )
            time.sleep(parse_interval)
            continue

        try:
            execute_job(job, article_collection, html_collection)
            url_collection.find_one_and_update(
                {"_id": job["_id"]}, {"$set": {"status": "finish"}}
            )
        except Exception as e:
            logger.exception(f"Parse error: {e}")
            url_collection.find_one_and_update(
                {"_id": job["_id"]}, {"$set": {"status": "error"}}
            )
            time.sleep(parse_interval)
            continue

        time.sleep(parse_interval)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parse_thread = Thread(target=parse_job, name="ParseJobWorker")
    parse_thread.start()
