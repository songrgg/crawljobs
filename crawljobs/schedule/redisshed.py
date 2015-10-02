# -*-coding:utf-8-*-
import redis
import logging
from crawljobs.schedule.redisqueue import CrawledUrlsQueue
from scrapy.utils.misc import load_object
from scrapy.utils.job import job_dir
from scrapy.core.scheduler import Scheduler

logger = logging.getLogger(__name__)


class RedisShed(Scheduler):

    CRAWL_TIMES = 'crawl_times'

    def __init__(self, server, rqclass, next_urls_queue_key,
                 crawled_urls_queue_key,*args, **wargs):
        super(RedisShed, self).__init__(*args, **wargs)
        self.server = server
        self.rqclass = rqclass
        self.next_urls_queue_key = next_urls_queue_key
        self.next_urls_rqs = None
        self.crawled_urls_queue_key = crawled_urls_queue_key
        self.crawled_urls_rqs = None
        self.spider = None

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        host = settings.get('REDIS_HOST', 'localhost')
        port = settings.get('REDIS_PORT', 6379)
        server = redis.Redis(host, port)
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = dupefilter_cls.from_settings(settings)
        dqclass = load_object(settings['SCHEDULER_DISK_QUEUE'])
        mqclass = load_object(settings['SCHEDULER_MEMORY_QUEUE'])
        rqclass = load_object(settings['SCHEDULER_REDIS_QUEUE'])
        next_urls_queue_key = settings.get('NEXT_URLS_QUEUE_KEY',
                                           '%(spider)s:next_urls')
        crawled_urls_queue_key = settings.get('CRAWLED_URLS_QUEUE_KEY',
                                              '%(spider)s:crawled_urls')
        logunser = settings.getbool('LOG_UNSERIALIZABLE_REQUESTS')
        return cls(server, rqclass, next_urls_queue_key, crawled_urls_queue_key,
                   dupefilter, job_dir(settings), dqclass, mqclass, logunser,
                   crawler.stats)

    def has_pending_requests(self):
        return len(self) > 0

    def open(self, spider):
        self.spider = spider
        self.next_urls_rqs = self.rqclass(self.server, self.spider,
                                          self.next_urls_queue_key)
        self.crawled_urls_rqs = CrawledUrlsQueue(self.server, self.spider,
                                                 self.crawled_urls_queue_key)
        return self.df.open()

    def close(self, reason):
        return self.df.close(reason)

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        self.next_urls_rqs.push(request)
        self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        return True

    def next_request(self):
        request = self.next_urls_rqs.pop()
        if request:
            self.stats.inc_value('scheduler/dequeued/redis',
                                 spider=self.spider)
            if RedisShed.CRAWL_TIMES in request.meta:
                request.meta[RedisShed.CRAWL_TIMES] += 1
            else:
                request.meta[RedisShed.CRAWL_TIMES] = 1
            self.crawled_urls_rqs.push(request)
        return request

    def __len__(self):
        return len(self.next_urls_rqs)
