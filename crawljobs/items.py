# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy import Field


class JobItem(Item):
    # company part
    city = Field()  # city
    companyLabelList = Field()  # list of company labels
    companyLogo = Field()  # company logo
    companyName = Field()  # company name
    companySize = Field()  # company size
    industryField = Field()  # industry field
    financeStage = Field()
    website = Field()  # official website

    # position part
    salary = Field()  # salary
    jobNature = Field()  # job nature
    createTime = Field()  # creat time
    positionName = Field()  # position name
    positionType = Field()  # position type
    positionAdvantage = Field()  # position benefits
    positionFirstType = Field()
    jobDescription = Field()  # job description
    workTime = Field()  # work period

    # requirement part
    workYear = Field()  # work year
    education = Field()  # required education degree

    # the job description source information
    positionId = Field()  # the origin position id if have
    originUrl = Field()  # source of the job description
    fromWhich = Field()  # source name
