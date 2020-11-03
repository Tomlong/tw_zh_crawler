import time
import asyncio
import pymongo
import logging
import datetime
import requests
from pyppeteer import launch
from bs4 import BeautifulSoup
from settings import (
    ARTICLE_URL_PREFIX,
    MONGO_URI,
    URL_DB_NAME,
    DB_NAME,
    YEARS_RANGE,
    SCROLL_INTERVAL,
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
    # 是否 assign_datetime 介於最新與最舊資料的時間內
    return oldest_datetime < assign_datetime < latest_datetime


async def scroll_down(page, assign_datetime):
    last_elem = []
    # 下滑至超過指定日期，則停止
    while True:
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")
        elem = soup.select(".part_list_2")[0]

        page_last_news_item = elem.find_all("h3")[-1]
        last_date_string = page_last_news_item.find(class_="date").text.split(" ")[0]
        assign_date_string = (
            f"{assign_datetime.year}/{assign_datetime.month}/{assign_datetime.day}"
        )

        # 檢查最後一則是否超出指定日期
        if is_date_over(assign_date_string, last_date_string):
            break

        # elem 數量與上一個 loop 一樣，則代表 scroll 到底
        if len(elem) == len(last_elem):
            break

        # 頁面下滑
        await page.evaluate("""{window.scrollBy(0, document.body.scrollHeight);}""")
        time.sleep(SCROLL_INTERVAL)
        # 記錄上個 loop elem
        last_elem = elem


async def _start_crawl(collection, assign_datetime, page):
    await page.goto(
        f"https://www.ettoday.net/news/news-list-{assign_datetime.year}-{assign_datetime.month}-{assign_datetime.day}-0.htm"
    )
    # 頁面下滑至當日最後一篇新聞
    await scroll_down(page, assign_datetime)
    # 取得 urls 的區塊
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")
    elems = soup.select(".part_list_2")[0].find_all("h3")
    for elem in elems:
        now_date_string = elem.find(class_="date").text.split(" ")[0]
        assign_date_string = (
            f"{assign_datetime.year}/{assign_datetime.month}/{assign_datetime.day}"
        )
        if is_date_over(assign_date_string, now_date_string):
            break

        # 取得 news_url
        link = elem.find("a").get("href")
        news_url = f"{ARTICLE_URL_PREFIX}{link}"
        # 取得 news 時間
        datetime_string = elem.find(class_="date").text
        date_format = "%Y/%m/%d %H:%M"
        news_datetime = datetime.datetime.strptime(datetime_string, date_format)
        # 寫入 db
        logger.info(f"get url: {news_url}")
        collection.insert_one(
            {"url": f"{news_url}", "datetime": news_datetime, "status": "pending"}
        )
    # 關閉新聞 page
    await page.close()


async def start_crawl(collection, crawl_interval=0.5):
    start_datetime = datetime.datetime.now()
    assign_datetime = datetime.datetime.now()

    browser = await init_browser()
    logger.info("Init browser success")
    logger.info("Start crawl urls")
    latest_news_url_item = (
        collection.find().sort("datetime", pymongo.DESCENDING).limit(1)[0]
    )
    oldest_news_url_item = (
        collection.find().sort("datetime", pymongo.ASCENDING).limit(1)[0]
    )
    latest_datetime = latest_news_url_item["datetime"]
    oldest_datetime = oldest_news_url_item["datetime"]

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
            page = await browser.newPage()
            await _start_crawl(collection, assign_datetime, page)
            # 日期往回一天
            assign_datetime -= datetime.timedelta(1)
        except:
            await page.close()

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
