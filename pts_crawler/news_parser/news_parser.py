import os
import re
import time
import json
import logging
import pymongo
import requests
from threading import Thread
from bs4 import BeautifulSoup
from settings import (
    MONGO_URI,
    URL_DB_NAME,
    DB_NAME,
    HTML_DB_NAME,
    ARTICLE_DB_NAME,
    USELESS_CATEGORIES,
)


logger = logging.getLogger(__name__)


def execute_job(job, article_collection, html_collection):
    news_url = job["url"]
    res = requests.get(news_url)
    main_soup = BeautifulSoup(res.text, "html.parser")

    # Get meta
    try:
        meta = json.loads(main_soup.find("script", type="application/ld+json").text)
    except:
        logger.info(f"url: {news_url} parse meta wrong!")
        raise

    # Get category
    try:
        category_soups = main_soup.find("ol", class_="breadcrumb").find_all("li")
        category = category_soups[1].text
        # get subcategory
        if len(category_soups) == 3:
            subcategory = category_soups[2].text
        else:
            subcategory = ""
    except:
        logger.info(f"url: {news_url} parse category wrong!")
        raise

    # 不需要的分類新聞 (目前只有Foreign類)
    if category not in USELESS_CATEGORIES:
        article_collection.insert_one(
            {
                "title": meta["headline"],
                "content": meta["articleBody"],
                "category": category,
                "subcategory": subcategory,
            }
        )

    # save html if finish job
    html_collection.insert_one({"html_text": res.text})


def parse_job(parse_interval=0.5):
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
            time.sleep(parse_interval)
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
