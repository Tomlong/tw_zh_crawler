import os
import re
import time
import random
import asyncio
import pymongo
import logging
import binascii
import datetime
import requests
import subprocess
from io import BytesIO
from minio import Minio
from pyppeteer import launch
from bs4 import BeautifulSoup
from settings import (
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME,
    ENTRYURL,
    INVALID_CATEGORIES,
    URL_PREFIX,
    DOWNLOAD_PATH,
    DOWNLOAD_URL,
    MINIO_HOST,
    MINIO_PORT,
    MINIO_SECRET_KEY,
    MINIO_ACCESS_KEY,
    MINIO_BUCKET,
)

logger = logging.getLogger(__name__)


def gen_id():
    return binascii.b2a_hex(os.urandom(15)).decode()[:24]


async def init_browser():
    # driver setup
    launch_kwargs = {"headless": True, "args": ["--no-sandbox"]}
    browser = await launch(options=launch_kwargs)
    return browser


def is_valid_category(category):
    # 任一非法的類別出現在 category 字串內，則當作不合法
    for invalid_c in INVALID_CATEGORIES:
        if invalid_c in category:
            return False
    return True


class RawCrawler:
    def __init__(self, collection, minio_client, minio_bucket):
        self.collection = collection
        self.minio_client = minio_client
        self.minio_bucket = minio_bucket

    def get_category_urls(self):
        response = requests.get(ENTRYURL)
        soup = BeautifulSoup(response.text, "html.parser")
        category_soup = soup.find("div", class_="well leftCategory")

        category_urls = []
        for now_soup in category_soup.find_all("a"):
            href = now_soup.get("href")
            # 不屬於法條 url
            if "LawSearchLaw" not in href:
                continue
            # 爬取 valid 的法規，目前不爬取憲法
            if is_valid_category(now_soup.get_text().strip()):
                category_urls.append(f"{URL_PREFIX}/Law/{href}")

        return category_urls

    async def download_pdf(self, url, page):
        # parse pcode and assemble download_url
        pcode_search = re.search("PCode=(.*)", url).group()
        pcode = pcode_search.split("=")[-1]
        download_url = DOWNLOAD_URL.format(pcode)

        await page.goto(download_url)
        # wait for file downlaod
        await page._client.send(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": f"./{DOWNLOAD_PATH}"},
        )
        # press download
        await page.click("#btnNoSDown")
        # total wait 5 seconds
        for i in range(5):
            dir_files = os.listdir(f"./{DOWNLOAD_PATH}")
            if (len(dir_files) == 1) and (dir_files[0].endswith(".pdf")):
                await page.close()
                return dir_files[0]
            time.sleep(1)

        return ""

    def save_pdf_to_db(self, url, filename, category_string):
        # 1. save to minio and get data_id
        data_id = gen_id()
        with open(f"./{DOWNLOAD_PATH}/{filename}", "rb") as f:
            bio = BytesIO(f.read())
            bio.seek(0)
        self.minio_client.put_object(
            self.minio_bucket, data_id, bio, bio.getbuffer().nbytes
        )
        # 2. write url, filename, and data_id to db
        self.collection.insert_one(
            {
                "url": url,
                "category": category_string,
                "filename": filename,
                "data_id": data_id,
            }
        )

    def delete_local_pdf(self, filename):
        command_line = f"rm -f ./{DOWNLOAD_PATH}/{filename}"
        p = subprocess.Popen(command_line.split(" "))
        try:
            p.wait(5)
        except:
            p.kill()
            raise Exception(f"Delete {filename} failed.")

    async def crawl_pdfs(self, category_url):
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, "html.parser")
        url_soups = soup.find_all("a", id="hlkLawName")
        # process category_string
        category_string = soup.find(class_="law-result").get_text()
        category_string = ",".join(category_string.strip().split(" ＞ "))

        for url_soup in url_soups:
            href = url_soup.get("href").replace("..", "")
            url = f"{URL_PREFIX}/{href}"

            try:
                result = self.collection.find_one({"url": url})
                if result:
                    continue

                page = await self.browser.newPage()
                filename = await self.download_pdf(url, page)
                logger.info(f"filename: {filename}")
                if filename:
                    self.save_pdf_to_db(url, filename, category_string)
                    self.delete_local_pdf(filename)
            except Exception as e:
                logger.info(f"Crawl {filename} failed: {e}")
                await page.close()
            time.sleep(0.5)
        logger.info(f"Finish crawl category: {category_string}")

    async def execute_job(self):
        self.browser = await init_browser()
        category_urls = self.get_category_urls()
        for category_url in category_urls:
            await self.crawl_pdfs(category_url)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # connet to mongodb
    mongo_client = pymongo.MongoClient(MONGO_URI)
    try:
        mongo_client.server_info()
    except:
        logger.warning("MongoDB is not connected.")
        exit()
    db = mongo_client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # connect to Minio
    minio_client = Minio(
        "%s:%s" % (MINIO_HOST, MINIO_PORT),
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False,
    )
    if not minio_client.bucket_exists(MINIO_BUCKET):
        logger.info(f"Make bucket: {MINIO_BUCKET}")
        minio_client.make_bucket(MINIO_BUCKET)

    crawler = RawCrawler(collection, minio_client, MINIO_BUCKET)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(crawler.execute_job())
    try:
        loop.run_until_complete(task)
    except Exception as e:
        logger.info(f"Run execute job wrong: {e}")
