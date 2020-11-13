import time
import random
import logging
import pymongo
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from settings import HEADERS, HTML_CONTENT_TYPES


logger = logging.getLogger(__name__)


def is_valid(url):
    """
    確認是否為合法 url
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url_response, domain_name, name, url_collection):
    soup = BeautifulSoup(url_response.text, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        href = urljoin(url_response.url, href)
        parsed_href = urlparse(href)
        url = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        result = url_collection.find_one({"url": url})

        # 非法 url
        if not is_valid(url):
            continue
        # 不存在 mongodb 的 bank_url
        if result is None:
            # 同個 domain 的 url
            if domain_name in url:
                url_collection.insert_one(
                    {
                        "url": url,
                        "domain_name": domain_name,
                        "name": name,
                        "status": "pending",
                    }
                )


def crawl_job(
    mongo_uri, db_name, main_collection_name, main_job,
):
    mongo_client = pymongo.MongoClient(mongo_uri)

    try:
        mongo_client.server_info()
    except:
        logger.warning("MongoDB is not connected.")
        exit()
    db = mongo_client[db_name]
    url_collection = db[main_job["url_collection_name"]]
    html_collection = db[main_job["html_collection_name"]]
    main_collection = db[main_collection_name]

    logger.info(
        "Start Scrapy {} in {}".format(main_job["name"], main_job["category_name"])
    )
    # Scrapy 指定 domain_name 的網站
    while True:
        job = url_collection.find_one_and_update(
            {"name": main_job["name"], "status": "pending"},
            {"$set": {"status": "scraping"}},
        )
        if not job:
            main_collection.update_one(
                {"name": main_job["name"], "category_name": main_job["category_name"]},
                {"$set": {"status": "finish"}},
            )
            logger.info(
                "Finish scrapy {} in {}.".format(
                    main_job["name"], main_job["category_name"]
                )
            )
            break

        url = job["url"]
        # ignore pdf
        if url.endswith(".pdf"):
            url_collection.find_one_and_update(
                {"url": job["url"]}, {"$set": {"status": "error"}}
            )
            continue

        # Record html content
        try:
            logger.info("Crawl url of {} - {}".format(main_job["name"], url))

            response = requests.get(url, headers=HEADERS, timeout=30)
            content_type = response.headers.get("Content-Type").replace(" ", "")
            # Only record the source Content-Type is text/html
            if content_type in HTML_CONTENT_TYPES:
                # windows-1254 不用轉換 encoding，會造成亂碼
                if response.apparent_encoding != "Windows-1254":
                    response.encoding = response.apparent_encoding
                html_collection.insert_one(
                    {"url": url, "html_text": response.text, "name": job["name"]}
                )
                # Finish scraping now url
                url_collection.update_one(
                    {"url": job["url"]}, {"$set": {"status": "finish"}}
                )
                # 爬取該頁面下的所有link
                get_all_website_links(
                    response, job["domain_name"], job["name"], url_collection
                )
            else:
                raise Exception(f"Ignore Content-Type of {content_type}.")

        except:
            url_collection.update_one(
                {"url": job["url"]}, {"$set": {"status": "error"}}
            )
            time.sleep(random.uniform(0.1, 0.2))
            continue

        time.sleep(random.uniform(0.1, 0.2))
