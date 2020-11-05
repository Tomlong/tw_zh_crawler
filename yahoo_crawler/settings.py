import os

ARTICLE_URL_PREFIX = "https://tw.news.yahoo.com"
API_BASE_URL = "https://tw.news.yahoo.com/_td-news/api/resource/IndexDataService.getExternalMediaNewsList;;start={};count={};loadMore=true;mrs=%7B%22size%22%3A%7B%22w%22%3A220%2C%22h%22%3A128%7D%7D;newsTab=all;tag=null;usePrefetch=false"

HEADERS = {
    'authority': 'tw.news.yahoo.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://tw.news.yahoo.com/',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'B=9j84oc5fm60ke&b=3&s=qi; A1=d=AQABBI4CY18CEPAL0a0htpr_SaN_jGGYoJkFEgEBAgHzbl89YL3Lb2UB_SMAAAcIjgJjX2GYoJk&S=AQAAAnkin89pPiN2JBplrPXZj0s; A3=d=AQABBI4CY18CEPAL0a0htpr_SaN_jGGYoJkFEgEBAgHzbl89YL3Lb2UB_SMAAAcIjgJjX2GYoJk&S=AQAAAnkin89pPiN2JBplrPXZj0s; A1S=d=AQABBI4CY18CEPAL0a0htpr_SaN_jGGYoJkFEgEBAgHzbl89YL3Lb2UB_SMAAAcIjgJjX2GYoJk&S=AQAAAnkin89pPiN2JBplrPXZj0s&j=WORLD; GUC=AQEBAgFfbvNgPUIb9AQg; thamba=1; yvapF=%7B%22vl%22%3A12.151952000000001%2C%22rvl%22%3A11.151952000000001%2C%22rcc%22%3A4%2C%22ac%22%3A1%2C%22al%22%3A0.144%2C%22cc%22%3A4%7D; cmp=t=1604547778&j=0',
    'if-none-match': 'W/"23e2-x7+87mduHYDCZsNgX/pGet1HcWs"',
}
API_PARAMS = (
    ('bkt', 'news-TW-zh-Hant-TW-def'),
    ('device', 'desktop'),
    ('ecma', 'modern'),
    ('feature', 'oathPlayer,videoDocking'),
    ('intl', 'tw'),
    ('lang', 'zh-Hant-TW'),
    ('partner', 'none'),
    ('prid', 'fn220q5fq6t69'),
    ('region', 'TW'),
    ('site', 'news'),
    ('tz', 'Asia/Taipei'),
    ('ver', '2.3.1528'),
    ('returnMeta', 'true'),
)

QUERY_COUNT = int(os.getenv("QUERY_COUNT", 200))
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "yahoo_data")
URL_DB_NAME = os.getenv("URL_DB_NAME", "news_url")
ARTICLE_DB_NAME = os.getenv("ARTICLE_DB_NAME", "article_data")
HTML_DB_NAME = os.getenv("HTML_DB_NAME", "html_data")
