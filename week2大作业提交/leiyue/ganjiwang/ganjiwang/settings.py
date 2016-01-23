# -*- coding: utf-8 -*-

# Scrapy settings for ganjiwang project
BOT_NAME = 'ganjiwang'

SPIDER_MODULES = ['ganjiwang.spiders']
NEWSPIDER_MODULE = 'ganjiwang.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 3

# Configure item pipelines
ITEM_PIPELINES = {
    'ganjiwang.pipelines.DuplicatesPipeline': 300,
    'scrapy_mongodb.MongoDBPipeline': 800,
}

# Scrapy mongodb databse configuration
MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'bj_ganji_com_lmsj'
