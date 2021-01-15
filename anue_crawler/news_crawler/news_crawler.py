import time
import pymongo
import logging
import requests
import datetime
from settings import API_URL, MONGO_URI, ARTICLE_DB_NAME, DB_NAME, DAY_RANGE, START_DATE

logger = logging.getLogger(__name__)


def get_datetime_end():
    today = datetime.datetime.now()
    datetime_str = "{}/{}/{}".format(today.year, today.month, today.day)
    datetime_end = datetime.datetime.strptime(datetime_str, "%Y/%m/%d")
    if START_DATE:
        try:
            datetime_end = datetime.datetime.strptime(START_DATE, "%Y/%m/%d")
        except:
            logger.info(
                f'start_date "{START_DATE}" format is not match %Y/%m/%d, so set start_date from today.'
            )
    return datetime_end


def _start_crawl(collection, datetime_end):
    datetime_start = datetime_end - datetime.timedelta(days=1)
    page = 1
    while True:
        query_data = {
            "startAt": int(datetime_start.timestamp()),
            "endAt": int(datetime_end.timestamp()),
            "limit": 30,
            "page": page,
        }
        response = requests.get(API_URL, params=query_data)
        try:
            result = response.json()
            datas = result["items"]["data"]
        except:
            logger.info("Get data from api failed.")
            break

        for data in datas:
            if collection.find_one({"news_id": data["newsId"]}):
                continue
            logger.info("Crawl title: {}".format(data["title"]))
            try:
                collection.insert_one(
                    {
                        "news_id": data["newsId"],
                        "title": data["title"],
                        "content": data["content"],
                        "category": data["categoryName"],
                        "market": data["market"],
                        "datetime": datetime.datetime.fromtimestamp(data["publishAt"]),
                    }
                )
            except Exception as e:
                logger.info(f"Parse detail failed, exception: {e}")
        if result["items"]["next_page_url"] is None:
            break
        page += 1
        time.sleep(0.5)


def start_crawl(collection):
    datetime_crawl_start = datetime.datetime.now()
    datetime_end = get_datetime_end()

    while True:
        if (datetime_end - datetime_crawl_start).days > DAY_RANGE:
            logger.info(
                f"Crawl over {DAY_RANGE} days, so stop and wait for newest news."
            )
            break

        _start_crawl(collection, datetime_end)
        # crawl date to previous day
        datetime_end = datetime_end - datetime.timedelta(days=1)
        time.sleep(1)


def execute_job(db, interval=300):
    collection = db[ARTICLE_DB_NAME]
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
