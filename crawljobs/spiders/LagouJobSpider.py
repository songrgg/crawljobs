# -*- coding: utf-8 -*-

import json
import re

import scrapy

from crawljobs.models import items
from crawljobs.config import constants


class LagouJobSpider(scrapy.Spider):

    name = "lagou"
    allowed_domains = ["lagou.com"]
    start_urls = [
        "http://www.lagou.com/jobs/positionAjax.json?px=new"
    ]

    patterns = {
        'lagou_job_detail':
            re.compile(r'^http://www\.lagou\.com/jobs/\d+\.html$')
    }

    def start_requests(self):
        init_request = scrapy.http.FormRequest(
            url=self.start_urls[0],
            formdata={
                'pn': '1',
                'first': 'false',
                'kd': ''
            },
            callback=self.parse)

        init_request.meta['pageNo'] = 1
        return [init_request]

    def parse(self, response):
        url = response.url

        if url == self.start_urls[0]:
            # process json API
            json_arr = json.loads(response.body_as_unicode())
            detail_urls = self.process_json(json_arr)
            for detail_url in detail_urls:
                next_url = detail_url.get('url')
                request = scrapy.http.Request(next_url,
                                              callback=self.process_detail)
                request.meta['position'] = detail_url.get('position')
                yield request

            if 'content' in json_arr:
                next_page = response.meta['pageNo'] + 1
                self.log('next page: ' + str(next_page))
                next_request = scrapy.http.FormRequest(
                    url=self.start_urls[0],
                    formdata={
                        'pn': str(next_page),
                        'first': 'false',
                        'kd': ''
                    },
                    callback=self.parse)

                next_request.meta['pageNo'] = next_page

                yield next_request
            else:
                self.log('No more jobs~~')

    # process the json object from `http://www.lagou.com/jobs/positionAjax.json
    # ?px=new`
    def process_json(self, json):
        """
        {
            "code": 0,
            "content": {
                "currentPageNo": 1,
                "hasNextPage": true,
                "hasPreviousPage": false,
                "pageNo": 1,
                "pageSize": 15,
                "result": [
                    {
                        "adWord": 0,
                        "adjustScore": 0,
                        "calcScore": false,
                        "city": "\u4e0a\u6d77",
                        "companyId": 78303,
                        "companyLabelList": [
                            "\u8282\u65e5\u793c\u7269",
                            "\u7ee9\u6548\u5956\u91d1",
                            "\u5e74\u5ea6\u65c5\u6e38",
                            "\u9886\u5bfc\u597d"
                        ],
                        "companyLogo": "",
                        "companyName": "\u7384\u4eab",
                        "companyShortName": "",
                        "companySize": "15-50\u4eba",
                        "countAdjusted": false,
                        "createTime": "2015-06-20 23:55:18.0",
                        "createTimeSort": 1434815718000,
                        "education": "\u5b66\u5386\u4e0d\u9650",
                        "financeStage": "",
                        "formatCreateTime": "23:55\u53d1\u5e03",
                        "haveDeliver": false,
                        "industryField": "",
                        "jobNature": "\u5168\u804c",
                        "leaderName": "\u6682\u6ca1\u6709\u586b\u5199",
                        "orderBy": 150,
                        "positionAdvantage": "",
                        "positionFirstType": "\u6280\u672f",
                        "positionId": 810880,
                        "positionName": "Java",
                        "positionType": "\u540e\u7aef\u5f00\u53d1",
                        "positonTypesMap": null,
                        "randomScore": 0,
                        "relScore": 0,
                        "salary": "12k-18k",
                        "score": 0,
                        "searchScore": "NaN",
                        "showOrder": 0,
                        "totalCount": 250603,
                        "workYear": "3-5\u5e74"
                    }
                ],
                "start": 0,
                "totalCount": 450,
                "totalPageCount": 30
            },
            "msg": null,
            "requestId": null,
            "resubmitToken": null,
            "success": true
        }
        """
        self.log('---start jsonApi---')

        if 'success' in json and json['success']:
            self.log('---jsonApi return success')
            content = json.get('content')
            if content != '':
                positions = content.get('result')

                detail_urls = []
                for position in positions:
                    position_id = position.get('positionId')
                    if position_id > 0:
                        detail_url = 'http://www.lagou.com/jobs/' +\
                                    str(position_id) + '.html'
                        detail_urls.append({'url': detail_url,
                                            'position': position})
                    else:
                        self.log('###invalid position id')
                return detail_urls
            else:
                self.log('###empty content')

        else:
            self.log('---jsonApi return failure')

        return []

    def process_detail(self, response):
        self.log('---start job detail: ' + response.url)
        position = response.meta['position']
        job_description = response.xpath('//dd[@class="job_bt"]').extract()
        website = response.xpath(
            '//dl[@class="job_company"]/dd/ul/li/a/text()').extract()

        position['website'] = ','.join(website)
        position['originUrl'] = response.url
        position['fromWhich'] = constants.JobSources.LAGOU
        position['jobDescription'] = ','.join(job_description)

        # transfer the dict to the JobItem
        item = items.JobItem()
        for key in position:
            try:
                item[key] = position[key]
            except KeyError, e:
                pass
        self.log('---end job detail: ' + response.url)
        return item
