#!/usr/bin/python
import redis
import time
from scrapy.utils.project import get_project_settings

# Get the one-week-ago crawled pages' urls , and send them to the next_urls_queue.

settings = get_project_settings()
host = settings.get('REDIS_HOST', 'localhost')
port = settings.get('REDIS_PORT', 6379)
server = redis.Redis(host, port)
one_week_ago = time.time() - 24*60*60*7

for crawled_urls_key in server.keys('*crawled_urls'):
    next_urls_key = crawled_urls_key.replace('crawled_urls', 'next_urls')
    print("Move crawled_urls from `%s` to `%s`" % (crawled_urls_key, next_urls_key))
    crawled_urls = server.zrangebyscore(crawled_urls_key, 0, one_week_ago)
    for crawled_url in crawled_urls:
        server.zadd(next_urls_key, {crawled_url: -10})
