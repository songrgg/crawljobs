# -*-coding:utf-8-*-
import redis
import time

from scrapy.dupefilters import RFPDupeFilter
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint


class RedisURLFilter(BaseDupeFilter):
    """Redis-based request duplication filter"""

    CRAWLJOBS_DUPEFILTER = 'crawljobs_dupefilter'

    def __init__(self, server, key):
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('REDIS_HOST', 'localhost')
        port = settings.get('REDIS_PORT', 6379)
        server = redis.Redis(host, port)
        # Create a duplicate url checker for crawljobs
        return cls(server, RedisURLFilter.CRAWLJOBS_DUPEFILTER)

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
        # self.server.delete(self.key)
