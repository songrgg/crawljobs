# -*- coding: utf-8 -*-

# Scrapy settings for crawljobs project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawljobs'

SPIDER_MODULES = ['crawljobs.spiders']
NEWSPIDER_MODULE = 'crawljobs.spiders'


# Crawl responsibly by identifying yourself (and your website) on the
# user-agent
# USER_AGENT = 'crawljobs (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#\
# download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN=16
# CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
# COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED=False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
#   , 'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#     'crawljobs.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     'crawljobs.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#     'scrapy.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'crawljobs.pipelines.mongodb.SingleMongodbPipeline': 300,
   'crawljobs.pipelines.mysql.MySQLPipeline': 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and \
# delay
# AUTOTHROTTLE_ENABLED=True
# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# #httpcache-middleware-settings
# HTTPCACHE_ENABLED=True
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.contrib.httpcache.FilesystemCacheStorage'

# SingleMongoDBPipeline settings
MONGO_URI = "localhost"
MONGO_PORT = 27017
MONGO_DB = "jobs"

# MySQLPipeline settings
MYSQL_URI = "yongwuapi_mysql_1"
MYSQL_PORT = 3306
MYSQL_DB = "yongwu"
MYSQL_USER = "root"
MYSQL_PASSWD = "yongwu"

# Add a custom filter passing the json-API url
# DUPEFILTER_CLASS = 'crawljobs.config.filter.CustomURLFilter'
DUPEFILTER_CLASS = 'crawljobs.config.filter.RedisURLFilter'

# Add a queue based on redis
SCHEDULER = 'crawljobs.schedule.redisshed.RedisShed'
SCHEDULER_REDIS_QUEUE = 'crawljobs.schedule.redisqueue.PriorityQueue'
DEPTH_PRIORITY = 0

# Schedule redis
REDIS_HOST = 'yongwuapi_redis_1'
REDIS_PORT = 6379
