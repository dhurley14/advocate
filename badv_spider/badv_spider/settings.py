# -*- coding: utf-8 -*-

# Scrapy settings for badv_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'badv_spider'

SPIDER_MODULES = ['badv_spider.spiders']
NEWSPIDER_MODULE = 'badv_spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'badv_spider (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 0.5
