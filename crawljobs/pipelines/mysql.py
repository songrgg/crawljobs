#!/usr/bin/python
#-*-coding:utf-8-*-

import re
import sys
import json
from scrapy import log
from sqlalchemy import and_
from sqlalchemy.engine import create_engine
from crawljobs.config.constants import JobSources

from .mysqlmodel import DBSession, Base, JobModel

class MySQLPipeline(object):
    """
        save the data to MySQL.
    """

    def __init__(self, mysql_uri, mysql_port, mysql_db, mysql_user, mysql_passwd):
        self.mysql_uri = mysql_uri
        self.mysql_port = mysql_port
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_passwd = mysql_passwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_uri=crawler.settings.get('MYSQL_URI', 'localhost'),
            mysql_port=crawler.settings.get('MYSQL_PORT', 3306),
            mysql_db=crawler.settings.get('MYSQL_DB', 'jobs'),
            mysql_user=crawler.settings.get('MYSQL_USER', 'root'),
            mysql_passwd=crawler.settings.get('MYSQL_PASSWD', 'root')
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

            log.msg("connect to [mysql+pymysql://%s:%s@%s/%s?charset=utf8]" %
                (
                    self.mysql_user, self.mysql_passwd,
                    self.mysql_uri, self.mysql_db
                ),
                level=log.INFO, spider=spider)

            DBSession.configure(bind=engine)
            Base.metadata.bind = engine
        except Exception as e:
            print "Catch Exception when [MySQLPipeline]: %s" % str(e)

    def close_spider(self, spider):
        DBSession.close()

    def process_item(self, item, spider):
        mysqlItem = dict()
        allowFields = JobModel.__dict__
        # allowFields = ['city', 'salary', 'positionName', 'minWorkYear', 'maxWorkYear', 'companyName',\
        #                  'companyLogo', 'companySize', 'industryField', 'financeStage', 'website' \
        #                  'jobNature', 'createTime', 'positionType', 'positionAdvantage', 'positionFirstType',\
        #                  'jobDescription', 'workTime', 'minWorkYear', 'maxWorkYear', 'education', 'positionId', \
        #                  'originUrl', 'fromWhich'
        #     ]
        for key in item.keys():
            if key in allowFields:
                mysqlItem[key] = item[key]

        positionId = mysqlItem.get('positionId')
        fromWhich = mysqlItem.get('fromWhich')
        workYear = item['workYear']

        minWorkYear = 0
        maxWorkYear = 100
        if re.match(r".*(\d+)-(\d+)年.*", workYear):
            match = re.match(r".*(\d+)-(\d+)年.*", workYear)
            minWorkYear = match.group(1)
            maxWorkYear = match.group(2)
        elif re.match(r".*(\d+)年以下.*", workYear):
            match = re.match(r".*(\d+)年以下.*", workYear)
            maxWorkYear = match.group(1)
        elif re.match(r".*(\d+)年以上.*", workYear):
            match = re.match(r".*(\d+)年以上.*", workYear)
            minWorkYear = match.group(1)

        mysqlItem['minWorkYear'] = minWorkYear
        mysqlItem['maxWorkYear'] = maxWorkYear

        try:
            DBSession.query(JobModel).filter( \
                and_(JobModel.positionId == positionId, JobModel.fromWhich == fromWhich)).delete()

            DBSession.add(JobModel(**mysqlItem))
            DBSession.commit()
        except:
            e = sys.exc_info()[0]
            log.msg("Failed to store: %s" % json.dumps(mysqlItem), level=log.ERROR, spider=spider)
            DBSession.rollback()
        finally:
            log.msg("Job [`%s` from `%s`] wrote to MySQL table %s" %
                    (positionId, fromWhich, self.mysql_db),
                    level=log.DEBUG, spider=spider)

        return item
