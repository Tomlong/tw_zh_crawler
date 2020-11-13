import time
import random
import logging
import pymongo
import requests
import threading
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from settings import (
    MONGO_URI,
    DB_NAME,
    MAIN_COLLECTION_NAME,
    MAIN_URL_INFOS,
)
from worker.crawl_worker import crawl_job

logger = logging.getLogger(__name__)


def init_job(db, main_url_info, interval=5):
    main_url_collection = db[MAIN_COLLECTION_NAME]

    # for main_url_info in MAIN_URL_INFOS:
    category_name = main_url_info["category_name"]
    url_collection_name = main_url_info["url_collection_name"]
    html_collection_name = main_url_info["html_collection_name"]
    for url_data in main_url_info["url_datas"]:
        result = main_url_collection.find_one(
            {
                "url": url_data["url"],
                "category_name": category_name,
                "status": {"$in": ["pending", "finish"]},
            }
        )
        if result is None:
            main_url_collection.update_one(
                {"url": url_data["url"], "category_name": category_name},
                {
                    "$set": {
                        "name": url_data["name"],
                        "domain_name": url_data["domain_name"],
                        "url_collection_name": url_collection_name,
                        "html_collection_name": html_collection_name,
                        "status": "pending",
                    }
                },
                upsert=True,
            )

    jobs = list(main_url_collection.find({"status": "pending"}))

    for job in jobs:
        # 開始 scrapy 主要網站
        main_url_collection.update_one(
            {"_id": job["_id"]}, {"$set": {"status": "scraping"}}
        )

        url_collection_name = job["url_collection_name"]
        url_collection = db[url_collection_name]
        # 將起始頁面寫入對應的 url collection
        url_collection.update_one(
            {"url": job["url"]},
            {
                "$set": {
                    "domain_name": job["domain_name"],
                    "name": job["name"],
                    "status": "pending",
                }
            },
            upsert=True,
        )

    return jobs


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mongo_client = pymongo.MongoClient(MONGO_URI)

    try:
        mongo_client.server_info()
    except:
        logger.warning("MongoDB is not connected.")
        exit()

    db = mongo_client[DB_NAME]

    for main_url_info in MAIN_URL_INFOS:
        jobs = init_job(db, main_url_info)

        # start each bank's crawler in each thread
        threads = []
        for i, job in enumerate(list(jobs)):
            crawl_thread = threading.Thread(
                target=crawl_job,
                name="CrawlWorker",
                args=(MONGO_URI, DB_NAME, MAIN_COLLECTION_NAME, job),
            )
            threads.append(crawl_thread)
            threads[i].start()

        for i in range(len(jobs)):
            threads[i].join()

        logger.info("Finish scrapy all {} page.".format(main_url_info["category_name"]))
