# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.spiders import Rule
from News_Scrapy.items import NewsScrapyItem
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings
from scrapy.http import Request
import os, pickle, json
from bs4 import BeautifulSoup
import jieba.analyse


## MySelf define the Global Variable
SAVED_URL = set()
if os.path.isfile(settings["SAVED_URL_PATH"]):
    with open(settings["SAVED_URL_PATH"], "rb") as handle:
        SAVED_URL = pickle.load(handle)


class NetEaseSpider(RedisSpider):
    name = "News_Scrapy"

    redis_key = 'myspider:start_urls'


    rules = [
        Rule(LinkExtractor(allow=(r'1[0-9]/[0-9][0-9][0-9][0-9]/[0-9][0-9]/[a-zA-Z0-9]_0+.html')),
             callback="parse_item"),
    ]


    def parse_item(self, response):

        if response.url not in SAVED_URL:
            SAVED_URL.add(response.url)


        jsonItem = response.meta['json']
        news_type = response.meta['type']

        news_item = NewsScrapyItem()

        news_item['news_title'] = jsonItem['title']
        news_item['news_date'] = jsonItem['ptime']
        news_item['news_digest'] = jsonItem['digest']
        news_item['news_image'] = jsonItem['imgsrc']
        news_item['news_source'] = jsonItem['source']
        news_item['news_type'] = news_type

        soup = BeautifulSoup(response.body.decode(response.encoding), "lxml")

        data =soup.find("div", {"class": "content"})

        if type(data) == type(None):
            return

        news_item['news_content'] = str(data)

        img_data = data.find_all("img")

        for item in img_data:
            item.decompose()

        a_data = data.find_all("a")

        for item in a_data:
            item.decompose()


        contents = ""
        for item in data:
            test = str(item)
            contents = contents + test

        key_map = {}
        for x, w in jieba.analyse.extract_tags(contents, withWeight=True):
            key_map[x] = w
        news_item["news_key"] = json.dumps(key_map)

        return news_item

    def parse(self, response):
        if response.url not in SAVED_URL:
            SAVED_URL.add(response.url)

        news_type = self.searchForType(response.url)

        Item = json.loads(response.body.decode(response.encoding)[29:-2])

        for jsonItem in Item:
            if "url" not in jsonItem:
                continue

            url = jsonItem['url']
            if url == "" or url == "null":
                continue

            news_item = NewsScrapyItem()

            if 'modelmode' in jsonItem:
                if jsonItem['modelmode'] == 'u':
                    continue

            url = url[:-5] + "_0" + url[-5:]

            if url not in SAVED_URL:
               yield Request(url, meta={'json': jsonItem, 'type': news_type}, callback=self.parse_item)


    def searchForType(self, url):
        if "BBM54PGAwangning" in url:
            news_type = "新闻"
        elif "BA10TA81wangning" in url:
            news_type = "娱乐"
        elif "BA8E6OEOwangning" in url:
            news_type = "体育"
        elif "BA8EE5GMwangning" in url:
            news_type = "财经"
        elif "BA8F6ICNwangning" in url:
            news_type = "时尚"
        elif "BAI67OGGwangning" in url:
            news_type = "军事"
        elif "BAI6I0O5wangning" in url:
            news_type = "手机"
        elif "BA8D4A3Rwangning" in url:
            news_type = "科技"
        elif "BAI6RHDKwangning" in url:
            news_type = "游戏"
        elif "BAI6JOD9wangning" in url:
            news_type = "数码"
        elif "BA8FF5PRwangning" in url:
            news_type = "教育"
        elif "BDC4QSV3wangning" in url:
            news_type = "健康"
        elif "BA8DOPCSwangning" in url:
            news_type = "汽车"
        elif "BAI6P3NDwangning" in url:
            news_type = "家居"
        elif "BAI6MTODwangning" in url:
            news_type = "房产"
        elif "BEO4GINLwangning" in url:
            news_type = "旅游"
        elif "BEO4PONRwangning" in url:
            news_type = "亲子"
        return news_type
