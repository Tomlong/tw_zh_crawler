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


def get_datetime(soup):
    datetime_str = soup.find("meta", property="og:release_date").attrs["content"]
    try:
        parsed_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        raise Exception(f"Parse datetime error. datetime: {datetime_str}{e}")
    return parsed_datetime


def get_title(soup):
    return soup.find("meta", property="og:title").attrs["content"]


def get_content(soup):
    return soup.find("div", class_="texttit_m1").get_text().replace("\u3000", "")


def execute_job(job, article_collection, html_collection):
    news_url = job["url"]
    try:
        logger.info(f"Parsing: {news_url}")
        res = requests.get(news_url, timeout=5)
        main_soup = BeautifulSoup(res.text, "html.parser")
    except:
        logger.info(f"url: {news_url} requests over timeout!")
        raise

    # Get meta
    try:
        meta = dict()
        meta["title"] = get_title(main_soup)
        meta["content"] = get_content(main_soup)
        meta["datetime"] = get_datetime(main_soup)
    except:
        logger.info(f"url: {news_url} parse meta wrong!")
        raise

    article_collection.insert_one(
        {
            "title": meta["title"],
            "content": meta["content"],
            "datetime": meta["datetime"],
        }
    )

    # save html if finish job
    html_collection.insert_one({"html_text": res.text})


def parse_job(parse_interval=0.01):
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
