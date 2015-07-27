# -*-coding:utf-8-*-
import redis
import time

from scrapy.dupefilters import RFPDupeFilter
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint


class CustomURLFilter(RFPDupeFilter):
    def __init__(self, path=None, debug=False):
        self.urls_seen = set()
        RFPDupeFilter.__init__(self, path=path, debug=debug)

    # pass the [POST] method requests
    def request_seen(self, request):
        if (request.method == 'POST'):
            return False

        if (request.url in self.urls_seen):
            return True
        else:
            self.urls_seen.add(request.url)

        return False


class RedisURLFilter(BaseDupeFilter):
    """Redis-based request duplication filter"""

    def __init__(self, server, key):
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('REDIS_HOST', 'localhost')
        port = settings.get('REDIS_PORT', 6379)
        server = redis.Redis(host, port)
        # create one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        key = "dupefilter:%s" % int(time.time())
        return cls(server, key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        """
            use sismember judge whether fp is duplicate.
        """
        fp = request_fingerprint(request)
        if self.server.sismember(self.key, fp):
            return True
        self.server.sadd(self.key, fp)
        return False

    def close(self, reason):
        """Delete data on close. Called by scrapy's scheduler"""
        self.clear()

    def clear(self):
        """Clears fingerprints data"""
        self.server.delete(self.key)
