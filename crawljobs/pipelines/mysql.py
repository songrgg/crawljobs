#!/usr/bin/python
#-*-coding:utf-8-*-

from scrapy import log
from sqlalchemy.engine import create_engine
from crawljobs.config.constants import JobSources

class MySQLPipeline(object):
    """
        save the data to MySQL.
    """

    MYSQL_URI = "localhost"
    MYSQL_PORT = 3306
    MYSQL_DB = "jobs"

    def __init__(self, mysql_uri, mysql_port, mysql_db):
        self.mysql_uri = mysql_uri
        self.mysql_port = mysql_port
        self.mysql_db = mysql_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_uri=crawler.settings.get('MYSQL_URI', cls.MYSQL_URI),
            mysql_port=crawler.settings.get('MYSQL_PORT', cls.MYSQL_PORT),
            mysql_db=crawler.settings.get('MYSQL_DB', cls.MYSQL_DB)
        )

    def open_spider(self, spider):
        try:
            engine = create_engine(
                "mysql+pymysql://root:yongwu@yongwuapi_mysql_1/yongwu?charset=utf8")

            self.conn = engine.connect()
        except Exception as e:
            print "Catch Exception when [MySQLPipeline]: %s" % str(e)

    def close_spider(self, spider):
        self.conn.close()

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
        else:
            # insert new record into db
            result = self.db['job_info'].insert_one(mongoItem)
            log.msg("Item %s wrote to MongoDB database %s/job_info" %
                    (result, self.MONGO_DB),
                    level=log.DEBUG, spider=spider)

        return item
