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
)


logger = logging.getLogger(__name__)


def get_content(main_soup):
    elem = main_soup.select(".story")
    texts = []
    for e in elem:
        texts.extend([p.text for p in e.select("p") if len(p.text) > 0])
    return "\n".join(texts)

def execute_job(job, article_collection, html_collection):
    news_url = job["url"]
    res = requests.get(news_url)
    main_soup = BeautifulSoup(res.text, "html.parser")

    # Get meta
    try:
        meta = json.loads(main_soup.find("script", type="application/ld+json").text)
        content = get_content(main_soup)
        meta["content"] = content
    except:
        logger.info(f"url: {news_url} parse meta wrong!")
        raise
   
    article_collection.insert_one(
        {
            "title": meta["headline"],
            "content": meta["content"],
            "category": meta["articleSection"],
            "keywords": meta["keywords"],
            "datetime": job["datetime"]
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
        except:
            logger.exception("Parse error")
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
