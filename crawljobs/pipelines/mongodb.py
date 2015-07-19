#!/usr/bin/python
#-*-coding:utf-8-*-

from pymongo import MongoClient
from scrapy import log
from crawljobs.config.constants import JobSources

class SingleMongodbPipeline(object):
    """
        save the data to mongodb.
    """

    MONGO_URI = "localhost"
    MONGO_PORT = 27017
    MONGO_DB = "job"

    def __init__(self, mongo_uri, mongo_port, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', cls.MONGO_URI),
            mongo_port=crawler.settings.get('MONGO_PORT', cls.MONGO_PORT),
            mongo_db=crawler.settings.get('MONGO_DB', cls.MONGO_DB)
        )

    def open_spider(self, spider):
        try:
            self.client = MongoClient(self.mongo_uri, self.mongo_port)
            self.db = self.client[self.mongo_db]
        except Exception as e:
            print "Catch Exception when [SingleMongodbPipeline]: %s" % str(e)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        mongoItem = dict()
        for key in item.keys():
            mongoItem[key] = item[key]
        positionId = mongoItem.get('positionId')
        fromWhich = mongoItem.get('fromWhich')

        condition = {'positionId': positionId, 'fromWhich': fromWhich}
        cursor = self.db['job_info'].find(condition)
        result = False
        if (cursor.count() > 0):
            # update this record
            # self.db['job_info'].delete_many(condition)
            # result = self.db['job_info'].insert_one(item)
            self.db['job_info'].update_one(
                condition,
                {
                    '$set': mongoItem
                }
            )
            # log.msg("update %d from %s successfully" %
            #         (positionId, fromWhich),
            #         level=log.DEBUG, spider=spider)
        else:
            # insert new record into db
            result = self.db['job_info'].insert_one(mongoItem)
            log.msg("Item %s wrote to MongoDB database %s/job_info" %
                    (result, self.MONGO_DB),
                    level=log.DEBUG, spider=spider)

        return item
