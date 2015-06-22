# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # job info
    position_name = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()
    release_date = scrapy.Field()
    jd = scrapy.Field()
    work_time = scrapy.Field()
    releaser = scrapy.Field()

    # job prerequisite
    experience = scrapy.Field()
    degree = scrapy.Field()

    # job benefits
    benefit_info = scrapy.Field()

    # company info
    company = scrapy.Field()
    company_website = scrapy.Field()
    company_stage = scrapy.Field()
    company_domain = scrapy.Field()
    company_member = scrapy.Field()
    company_address = scrapy.Field()

    # job source
    source_url = scrapy.Field()
