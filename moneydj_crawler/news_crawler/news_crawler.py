import time
import pymongo
import logging
import requests
from bs4 import BeautifulSoup
from settings import NEWS_URL, URL_PREFIX, MONGO_URI, URL_DB_NAME, DB_NAME

logger = logging.getLogger(__name__)


def is_over_page(soup, page):
    for page_soup in soup.find("table", class_="paging3").find_all("td"):
        try:
            now_page = int(page_soup.get_text().strip())
        except:
            continue

        if page == now_page:
            return False
    return True


def start_crawl(collection):
    page = 1
    while True:
        logger.info(f"Page: {page}")
        page_url = NEWS_URL.format(page)
        res = requests.get(page_url)
        soup = BeautifulSoup(res.content, "html.parser")

        # 確認是否為最後一頁
        if is_over_page(soup, page):
            logger.info("Finish crawl all pages")
            break
        try:
            # crawl page's urls
            for title_soup in soup.find("table", class_="forumgrid").find_all("a"):
                url = URL_PREFIX + title_soup.get("href")
                result = collection.find_one({"url": url})
                if result is None:
                    collection.insert_one({"url": url, "status": "pending"})
                    logger.info(f"save url: {url}")
        except Exception as e:
            logger.info(f"Crawl page_{page}: {e}")

        page += 1


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
