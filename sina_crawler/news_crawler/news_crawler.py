import time
import asyncio
import pymongo
import logging
import datetime
import requests
from pyppeteer import launch
from bs4 import BeautifulSoup
from settings import (
    START_URL,
    MONGO_URI,
    URL_DB_NAME,
    DB_NAME,
    YEARS_RANGE,
)

logger = logging.getLogger(__name__)


async def init_browser():
    # driver setup
    launch_kwargs = {"headless": True, "args": ["--no-sandbox"]}
    browser = await launch(options=launch_kwargs)
    return browser


def is_date_over(assign_date_string, date_string):
    date_format = "%Y/%m/%d"
    return datetime.datetime.strptime(
        assign_date_string, date_format
    ) > datetime.datetime.strptime(date_string, date_format)


def is_date_between_crawled(assign_datetime, latest_datetime, oldest_datetime):
    if assign_datetime and latest_datetime:
        # 是否 assign_datetime 介於最新與最舊資料的時間內
        return oldest_datetime < assign_datetime < latest_datetime
    # 沒有 latest_datetime 和 oldest_datetime，意指 db 還是空的
    return False


async def get_max_page_num(url, browser):
    page = await browser.newPage()
    await page.goto(url)
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")
    page_num_list = soup.find_all("span", class_="pagebox_num")
    return int(page_num_list[-1].text)


async def _start_crawl(collection, assign_datetime, browser):
    date_str = (
        f"{assign_datetime.year}-{assign_datetime.month:02}-{assign_datetime.day:02}"
    )
    today = datetime.datetime.fromisoformat(date_str)
    last_day = today - datetime.timedelta(days=1)

    # 從第一頁取得當日 max_page_num
    page_url = START_URL.format(
        int(last_day.timestamp()),
        int(today.timestamp()),
        int(today.timestamp()),
        date_str,
        1,
    )
    max_page_number = await get_max_page_num(page_url, browser)

    for page_num in range(1, max_page_number + 1):
        page_url = START_URL.format(
            int(last_day.timestamp()),
            int(today.timestamp()),
            int(today.timestamp()),
            date_str,
            page_num,
        )
        page = await browser.newPage()
        await page.goto(page_url, {"timeout": 0})
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        news_soup_list = soup.find_all("span", class_="c_tit")
        time_soup_list = soup.find_all("span", class_="c_time")
        for news_soup, time_soup in zip(news_soup_list, time_soup_list):
            # 從 time_soup 取得 timestamp，轉換成 datetime
            news_datetime = datetime.datetime.fromtimestamp(int(time_soup["s"]))
            news_url = news_soup.a["href"]
            # 必須是當天的新聞才寫入
            if news_datetime.date() == assign_datetime.date():
                collection.update_one(
                    {"url": news_url},
                    {"$set": {"datetime": news_datetime, "status": "pending"}},
                    upsert=True,
                )
        await page.close()


async def start_crawl(collection, crawl_interval=0.5):
    start_datetime = datetime.datetime.now()
    assign_datetime = datetime.datetime.now()

    browser = await init_browser()
    logger.info("Init browser success")
    logger.info("Start crawl urls")

    try:
        latest_news_url_item = (
            collection.find().sort("datetime", pymongo.DESCENDING).limit(1)[0]
        )
        oldest_news_url_item = (
            collection.find().sort("datetime", pymongo.ASCENDING).limit(1)[0]
        )
        latest_datetime = latest_news_url_item["datetime"]
        oldest_datetime = oldest_news_url_item["datetime"]
    except:
        latest_datetime = None
        oldest_datetime = None

    while True:
        logger.info(f"assign_datetime: {assign_datetime}")
        diff_datetime = start_datetime - assign_datetime
        # 超過指定時限
        if diff_datetime.days > (YEARS_RANGE * 365):
            logger.info(
                f"Crawl over {YEARS_RANGE} years, so stop and wait for newest news."
            )
            break

        # 該日期是否介於 db 最新與最舊資料的 datetime，是的話，則從最舊開始爬
        if is_date_between_crawled(assign_datetime, latest_datetime, oldest_datetime):
            assign_datetime = oldest_datetime
            continue
        try:
            await _start_crawl(collection, assign_datetime, browser)
            # 日期往回一天
            assign_datetime -= datetime.timedelta(1)
        except Exception as e:
            logger.info(f"exception: {e}")
            pass

        time.sleep(crawl_interval)
    # close browser
    await browser.close()


def execute_job(db, interval=120):
    collection = db[URL_DB_NAME]
    while True:
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(start_crawl(collection))
        try:
            loop.run_until_complete(task)
        except Exception as e:
            logger.info(f"Crawl news url error: {e}")

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
