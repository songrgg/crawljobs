# -*- coding: utf-8 -*-

import re
import string
import datetime

import scrapy

from crawljobs.models.items import JobItem


class NeituiSpider(scrapy.Spider):

    name = "neitui"
    neitui_domain = "http://www.neitui.me"
    # allowed_domains = [neitui_domain]
    start_urls = [
        "http://www.neitui.me/neitui/page=1.html"
    ]

    cur_page = 1
    max_page = 135

    def parse(self, response):
        if self.cur_page >= self.max_page:
            yield None

        job_links = response.xpath('//div[@class="jobnote-l"]/a/@href').\
            extract()

        for job_link in job_links:
            job_link = '%s%s' % (self.neitui_domain, job_link)
            self.log('crawl %s' % job_link)
            yield scrapy.http.Request(url=job_link, callback=self.parse_detail)

        next_link = "http://www.neitui.me/neitui/page=%d.html" % \
            (self.cur_page+1)
        self.cur_page += 1
        self.log('go to next page: %s' % next_link)
        yield scrapy.http.Request(url=next_link, callback=self.parse)

    def parse_detail(self, response):
        self.log('go to detail page: %s' % response.url)
        city = response.xpath('//span[@class="jobtitle-r"]/text()').\
            extract()[0]
        companyLogo = response.xpath('//div[@class="img"]/a/img/@src').\
            extract()[0]
        companyName = response.xpath('//span[@class="jobtitle-l"]/text()').\
            extract()[0]

        company_panel = response.xpath('//dl[@class="ci_body"]/dd/text()').\
            extract()
        companySize = company_panel[1]
        industryField = company_panel[2]
        financeStage = company_panel[3]
        website = response.xpath('//a[@class="defaulta bluea"]/@href').\
            extract()[0]

        # position part
        salary = response.xpath('//span[@class="padding-r10 pay"]/text()').\
            extract()[0]
        jobNature = ''

        jobnote = response.xpath('//div[@class="jobnote"]').extract()
        jobnote1 = jobnote[0].replace('\r\n', '')
        month = re.match(r".*(\d\d).*(\d\d).*", jobnote1).group(1)
        day = re.match(r".*(\d\d).*(\d\d).*", jobnote1).group(2)
        createTime = '%s-%s-%s' % (datetime.datetime.now().year, month, day)
        positionName = response.xpath(
            '//div[@class="jobnote"]/strong/text()').extract()[0]
        positionType = ''

        advantages = response.xpath(
            '//li[@class="company_tag"]/span[@class="content"]/text()').\
            extract()
        positionAdvantage = "[]"
        if len(advantages) > 0:
            positionAdvantage = '["%s"]' % string.join(advantages, '","')

        positionFirstType = ''
        jobDescription = response.xpath(
            '//div[@class="jobdetail nooverflow"]').extract()[0]
        workTime = 8

        # requirement part
        workYear = response.xpath(
            '//span[@class="padding-r10 experience"]/text()').extract()[0]
        education = ''

        # the job description source information
        match = re.match(r".*id=(\d+).*", response.url)
        positionId = match.group(1)  # the origin position id if have

        originUrl = response.url  # source of the job description
        fromWhich = 'neitui,内推'  # source name

        yield JobItem(
            city=city,
            companyLogo=companyLogo,
            companyName=companyName,
            companySize=companySize,
            industryField=industryField,
            financeStage=financeStage,
            website=website,
            salary=salary,
            jobNature=jobNature,
            createTime=createTime,
            positionName=positionName,
            positionType=positionType,
            positionAdvantage=positionAdvantage,
            jobDescription=jobDescription,
            workTime=workTime,
            workYear=workYear,
            education=education,
            positionId=positionId,
            originUrl=originUrl,
            fromWhich=fromWhich
        )
