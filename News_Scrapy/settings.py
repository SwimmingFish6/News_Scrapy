# -*- coding: utf-8 -*-

# Scrapy settings for News_Scrapy project
import os

BASE_DIR = os.path.split(os.path.realpath(__file__))[0]

BOT_NAME = 'News_Scrapy'

SPIDER_MODULES = ['News_Scrapy.spiders']
NEWSPIDER_MODULE = 'News_Scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'News_Scrapy (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'News_Scrapy.pipelines.NewsScrapyPipeline':300,
}

LOG_LEVEL = 'DEBUG'

DOWNLOAD_TIMEOUT = 30
DOWNLOAD_DELAY = 1
COOKIES_ENABLED = False



CONCURRENT_REQUESTS=20
CONCURRENT_REQUESTS_PER_DOMAIN = 20
DEPTH_PRIORITY=0
DEPTH_STATS=True
DEPTH_STATS_VERBOSE=True
ROBOTSTXT_OBEY = False
RANDOMIZE_DOWNLOAD_DELAY = True

DEFAULT_REQUEST_HEADERS = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'no-cache',
'Connection': 'keep-alive'
}

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'python'
MONGODB_COLLECTION = 'news_data'

SAVED_URL_PATH = BASE_DIR + "/SAVED_URL.pkl"

REDIS_URL = 'redis://165.227.3.239:6379'
