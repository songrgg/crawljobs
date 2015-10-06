# -*- coding: utf-8 -*-
import re
import string
import traceback
import copy
import json
import logging
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.spiders.crawl import CrawlSpider
from crawljobs.models.items import JobItem
from crawljobs.models.rule import Base
from crawljobs.models.rule import CrawlRule
from crawljobs.models.rule import DBSession
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import SQLAlchemyError
from scrapy.utils.project import get_project_settings


class RuleSpider(CrawlSpider):

    allowed_domains = []

    rules = []

    fields = {}

    def _compile_rules(self):
        self._initialize_rules()
        super(RuleSpider, self)._compile_rules()

    def _initialize_rules(self):
        try:
            settings = get_project_settings()
            mysql_user = settings.get('MYSQL_USER', 'root')
            mysql_db = settings.get('MYSQL_DB', 'yongwu')
            mysql_uri = settings.get('MYSQL_URI', 'localhost')
            mysql_passwd = settings.get('MYSQL_PASSWD', 'root')
            engine = create_engine(
                "mysql+pymysql://%s:%s@%s/%s?charset=utf8" %
                (
                    mysql_user, mysql_passwd,
                    mysql_uri, mysql_db
                )
            )

            DBSession.configure(bind=engine)
            Base.metadata.bind = engine
            for rule in DBSession.query(CrawlRule).filter_by(enabled=1).all():
                self.log("start loading rule: %s" % rule.name)
                allowed_domains = json.loads(rule.allow_domains)
                self.allowed_domains.extend(allowed_domains)

                url_patterns = json.loads(rule.url_patterns)
                for url_pattern in url_patterns:
                    if url_pattern['type'] == 'medium':
                        self.rules.append(
                            Rule(
                                LinkExtractor(allow=(url_pattern['pattern'])),
                                callback='parse_the_page',
                                follow=True
                            )
                        )
                    elif url_pattern['type'] == 'target':
                        self.rules.append(
                            Rule(
                                LinkExtractor(allow=(url_pattern['pattern'])),
                                callback='parse_item',
                                follow=False
                            )
                        )

                self.fields = json.loads(rule.fields_extractions)
        except SQLAlchemyError:
            self.log("Failed to query", logging.ERROR)

    def parse_the_page(self, response):
        self.log("go to page: %s" % response.url)
        yield Request(url=response.url, callback=self.parse, dont_filter=True)


class JobSpider(RuleSpider):

    name = 'jobs'

    start_urls = ['http://www.neitui.me']

    def parse_item(self, response):
        self.log("collect detail page: %s" % response.url)

        item = JobItem()
        fields = copy.copy(self.fields)
        for field in fields:
            try:
                value = fields[field]
                if 'xpath' in value:
                    temp_value = response.xpath(value['xpath']).extract()[0]
                    if 'to_json'in value:
                        temp_value = '["%s"]' % string.join(temp_value, '","')
                    item[field] = temp_value
                elif 'expr' in value:
                    item[field] = eval(value['expr'])
                elif 'value' in value:
                    item[field] = value['value']
            except Exception:
                traceback.print_exc()
                self.log("Something wrong when rendering fields", logging.ERROR)
        yield item
