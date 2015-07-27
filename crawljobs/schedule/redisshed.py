# -*-coding:utf-8-*-

import os
import json
import redis
import logging

from queuelib import PriorityQueue
from scrapy.utils.misc import load_object
from scrapy.utils.job import job_dir
from scrapy.core.scheduler import Scheduler

logger = logging.getLogger(__name__)


class RedisShed(Scheduler):

    def __init__(self, server, rqclass, queue_key, *args, **wargs):
        super(RedisShed, self).__init__(*args, **wargs)
        self.server = server
        self.rqclass = rqclass
        self.queue_key = queue_key

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
        queue_key = settings.get('SCHEDULER_QUEUE_KEY', '%(spider)s:requests')
        logunser = settings.getbool('LOG_UNSERIALIZABLE_REQUESTS')
        return cls(server, rqclass, queue_key, dupefilter, job_dir(settings),
                   dqclass, mqclass, logunser, crawler.stats)

    def has_pending_requests(self):
        return len(self) > 0

    def open(self, spider):
        self.spider = spider
        self.rqs = self.rqclass(self.server, self.spider, self.queue_key)
        self.mqs = PriorityQueue(self._newmq)
        self.dqs = self._dq() if self.dqdir else None
        return self.df.open()

    def close(self, reason):
        if self.dqs:
            prios = self.dqs.close()
            with open(join(self.dqdir, 'active.json'), 'w') as f:
                json.dump(prios, f)
        return self.df.close(reason)

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        self.rqs.push(request)
        self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        return True

    def next_request(self):
        request = self.rqs.pop()
        if request:
            self.stats.inc_value('scheduler/dequeued/redis',
                                 spider=self.spider)
        return request

    def __len__(self):
        return len(self.rqs)

    def _dqpush(self, request):
        if self.dqs is None:
            return
        try:
            reqd = request_to_dict(request, self.spider)
            self.dqs.push(reqd, -request.priority)
        except ValueError as e:  # non serializable request
            if self.logunser:
                logger.error("Unable to serialize request: %(request)s - reason\
                    : %(reason)s",
                             {'request': request, 'reason': e},
                             exc_info=True, extra={'spider': self.spider})
            return
        else:
            return True

    def _mqpush(self, request):
        self.mqs.push(request, -request.priority)

    def _dqpop(self):
        if self.dqs:
            d = self.dqs.pop()
            if d:
                return request_from_dict(d, self.spider)

    def _newmq(self, priority):
        return self.mqclass()

    def _newdq(self, priority):
        return self.dqclass(join(self.dqdir, 'p%s' % priority))

    def _dq(self):
        activef = join(self.dqdir, 'active.json')
        if exists(activef):
            with open(activef) as f:
                prios = json.load(f)
        else:
            prios = ()
        q = PriorityQueue(self._newdq, startprios=prios)
        if q:
            logger.info("Resuming crawl (%(queuesize)d requests scheduled)",
                        {'queuesize': len(q)}, extra={'spider': self.spider})
        return q

    def _dqdir(self, jobdir):
        if jobdir:
            dqdir = join(jobdir, 'requests.queue')
            if not exists(dqdir):
                os.makedirs(dqdir)
            return dqdir
