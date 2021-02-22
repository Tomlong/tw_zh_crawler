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
    TITLE_IGNORE_TEXT,
)


logger = logging.getLogger(__name__)


def get_content(main_soup):
    content_soup_list = main_soup.find("div", class_="article").find_all("p")
    texts = [
        content_soup.text.strip()
        for content_soup in content_soup_list
        if len(content_soup.text) > 0 and TITLE_IGNORE_TEXT not in content_soup.text
    ]
    return "\n".join(texts)


def get_title(main_soup):
    title_soup = main_soup.find("h1", class_="main-title")
    title = title_soup.text
    title = title.strip().replace(TITLE_IGNORE_TEXT, "")
    return title


def get_keywords(main_soup):
    try:
        keyword_soup_list = main_soup.find("div", class_="keywords").find_all("a")
        keywords = [keyword_soup.text for keyword_soup in keyword_soup_list]
    except:
        return []
    return keywords


def execute_job(job, article_collection, html_collection):
    news_url = job["url"]
    res = requests.get(news_url)
    res.encoding = "utf-8"
    main_soup = BeautifulSoup(res.text, "html.parser")

    # Get meta
    try:
        meta = {}
        meta["content"] = get_content(main_soup)
        meta["title"] = get_title(main_soup)
        meta["keywords"] = get_keywords(main_soup)
        meta["datetime"] = job["datetime"]
    except:
        logger.info(f"url: {news_url} parse meta wrong!")
        raise

    article_collection.insert_one(
        {
            "title": meta["title"],
            "content": meta["content"],
            "category": "finance",
            "keywords": meta["keywords"],
            "datetime": meta["datetime"],
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
