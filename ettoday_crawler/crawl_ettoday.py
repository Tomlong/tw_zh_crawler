import os
import requests
import json
import random
from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing import cpu_count


user_agents = [
 "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
 "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
 "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
 "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
 "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
 "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
 "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
 "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
 "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]


headers = {
    "user-agent":random.choice(user_agents)
}


def craw_content(link):
    prefix = "https://www.ettoday.net"
    resp_ = requests.get(prefix + link, headers = headers)
    soup_ = BeautifulSoup(resp_.text, "lxml")
    elem_ = soup_.select(".story")
    texts = []
    for e_ in elem_:
        texts.extend([title.text for title in e_.select("p") if len(title.text) > 0])
    return texts


def craw_meta():
    """
    https://www.ettoday.net/news/news-list-2017-07-15-5.htm
    1 政治 
    17 財經
    2 國際
    6 社會
    9 影劇
    10 體育
    20 3c
    30 時尚 
    24 遊戲
    5 生活
    """
    title_list = []
    date_list = []
    cate_list = []
    link_list = []
    
    # which catecory
    for tt in [5]:
        
        # which date to crawl
        for year in [2019]:
            for month in range(12, 13):
                for day in range(31, 32):
                    url = f"https://www.ettoday.net/news/news-list-{year}-{month}-{day}-{tt}.htm"
                    res = requests.get(url, headers = headers)
                    soup = BeautifulSoup(res.content, "lxml")
                    elem = soup.select(".part_list_2")
                    for e in elem:
                        title_list.extend([title.text for title in e.select("a")])
                        link_list.extend([i.get('href') for i in e.select("a")])
                        date_list.extend([date.text for date in e.select(".date")])
                        cate_list.extend([cate.text for cate in e.select("em")])
    return title_list, date_list, cate_list, link_list


if __name__ == "__main__":
    save_path = "ettoday_life"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    
    title_list, date_list, cate_list, link_list = craw_meta()
    pool = Pool(cpu_count())
    results = pool.map(craw_content, link_list)
    print(f"num articals: {len(results)}")
    
    output = []
    for i in range(len(results)):
        item = {}
        item["title"] = title_list[i]
        item["link"] = date_list[i]
        item["date"] = link_list[i]
        item["category"] = cate_list[i]
        item["text"] = "\n".join(results[i])
        output.append(item)
        if i % 3000 == 0:  # 每3000篇存一個檔案
            with open(f'{save_path}/ettoday_{i}.json', 'w') as outfile:
                json.dump(output, outfile, ensure_ascii=False)
            output = []
    if len(output) > 0:
        with open(f'{save_path}/ettoday_{i}.json', 'w') as outfile:
                json.dump(output, outfile, ensure_ascii=False)
        
