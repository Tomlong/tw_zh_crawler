import os

ARTICLE_URL_PREFIX = "https://www.businessweekly.com.tw"
API_BASE_URL = "https://www.businessweekly.com.tw/latest/SearchList"

HEADERS = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.businessweekly.com.tw',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.businessweekly.com.tw/latest?p=1',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "udn_data")
URL_DB_NAME = os.getenv("URL_DB_NAME", "news_url")
ARTICLE_DB_NAME = os.getenv("ARTICLE_DB_NAME", "article_data")
HTML_DB_NAME = os.getenv("HTML_DB_NAME", "html_data")
