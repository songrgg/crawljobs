#!/usr/bin/python
#-*-coding:utf-8-*-

from scrapy import log
from sqlalchemy.engine import create_engine
from crawljobs.config.constants import JobSources

from .mysqlmodel import DBSession, Base, JobModel

class MySQLPipeline(object):
    """
        save the data to MySQL.
    """

    MYSQL_URI = "localhost"
    MYSQL_PORT = 3306
    MYSQL_DB = "jobs"
    MYSQL_USER = "root"
    MYSQL_PASSWD = "root"

    def __init__(self, mysql_uri, mysql_port, mysql_db, mysql_user, mysql_passwd):
        self.mysql_uri = mysql_uri
        self.mysql_port = mysql_port
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_passwd = mysql_passwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_uri=crawler.settings.get('MYSQL_URI', cls.MYSQL_URI),
            mysql_port=crawler.settings.get('MYSQL_PORT', cls.MYSQL_PORT),
            mysql_db=crawler.settings.get('MYSQL_DB', cls.MYSQL_DB),
            mysql_user=crawler.settings.get('MYSQL_USER', cls.MYSQL_USER),
            mysql_passwd=crawler.settings.get('MYSQL_PASSWD', cls.MYSQL_PASSWD)
        )

    def open_spider(self, spider):
        try:
            engine = create_engine(
                "mysql+pymysql://%s:%s@%s/%s?charset=utf8" %
                (
                    self.mysql_user, self.mysql_passwd,
                    self.mysql_uri, self.mysql_db
                )
            )

            DBSession.configure(bind=engine)
            Base.metadata.bind = engine
        except Exception as e:
            print "Catch Exception when [MySQLPipeline]: %s" % str(e)

    def close_spider(self, spider):
        DBSession.close()

    def process_item(self, item, spider):
        mysqlItem = dict()
        for key in item.keys():
            mysqlItem[key] = item[key]
        positionId = mysqlItem.get('positionId')
        fromWhich = mysqlItem.get('fromWhich')

        try:
            DBSession.add(JobModel(**mysqlItem))
            DBSession.commit()
        except:
            DBSession.rollback()
        finally:
            DBSession.close()
            log.msg("Job [`%s` from `%s`] wrote to MySQL table %s" %
                    (positionId, fromWhich, self.MYSQL_DB),
                    level=log.DEBUG, spider=spider)

        return item
