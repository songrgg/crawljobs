# coding: utf-8

import re
import json
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import create_engine
from .mysqlmodel import DBSession, Base, JobModel


class MySQLPipeline(object):
    """
        save the data to MySQL.
    """

    def __init__(self,
                 mysql_uri,
                 mysql_port,
                 mysql_db,
                 mysql_user,
                 mysql_passwd):
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

            logging.info("connect to [mysql+pymysql://%s:%s@%s/%s?charset=utf8]" %
                         (
                            self.mysql_user, self.mysql_passwd,
                            self.mysql_uri, self.mysql_db
                         ))

            DBSession.configure(bind=engine)
            Base.metadata.bind = engine
        except Exception as e:
            print "Catch Exception when [MySQLPipeline]: %s" % str(e)

    def close_spider(self, spider):
        DBSession.close()

    def process_item(self, item, spider):
        mysqlItem = dict()
        allowFields = JobModel.__dict__
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
            DBSession.query(JobModel).filter(
                JobModel.positionId == positionId and
                JobModel.fromWhich == fromWhich
            ).delete()
            DBSession.add(JobModel(**mysqlItem))
            DBSession.commit()
            logging.debug("Job [`%s` from `%s`] written to MySQL" %
                (positionId, fromWhich))
        except SQLAlchemyError:
            # e = sys.exc_info()[0]
            logging.error("Failed to store: %s" % json.dumps(mysqlItem))
            DBSession.rollback()

        return item
