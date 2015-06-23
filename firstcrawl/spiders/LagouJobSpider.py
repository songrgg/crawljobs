import scrapy
import json
import re
from firstcrawl import items
from firstcrawl.config import constants

class LagouJobSpider(scrapy.Spider):

    name = "lagou"
    allowed_domains = ["lagou.com"]
    start_urls = [
        "http://www.lagou.com/jobs/positionAjax.json?px=new"
    ]

    patterns = {
        'lagou_job_detail': re.compile(r'^http://www\.lagou\.com/jobs/\d+\.html$')
    }

    def start_requests(self):
        init_request = scrapy.http.FormRequest(
            url=self.start_urls[0],
            formdata={
                'pn':'1',
                'first':'false',
                'kd':''
            },
            callback=self.parse)

        init_request.meta['pageNo'] = 1
        return [init_request]

    def parse(self, response):
        url = response.url

        if (url == self.start_urls[0]):
            # process json API
            jsonArr = json.loads(response.body_as_unicode())
            detail_urls = self.processJson(jsonArr)
            for detail_url in detail_urls:
                next_url = detail_url.get('url')
                request = scrapy.http.Request(next_url, callback=self.processDetail)
                request.meta['position'] = detail_url.get('position')
                yield request

            if ('content' in jsonArr):
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

    # process the json object from `http://www.lagou.com/jobs/positionAjax.json?px=new`
    def processJson(self, json):
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
                        "companyLogo": "image1/M00/30/0E/Cgo8PFWFi62AQWBeAABBiADh0W4407.png?cc=0.04744642600417137",
                        "companyName": "\u7384\u4eab",
                        "companyShortName": "\u4e0a\u6d77\u7384\u4eab\u4fe1\u606f\u79d1\u6280\u6709\u9650\u516c\u53f8",
                        "companySize": "15-50\u4eba",
                        "countAdjusted": false,
                        "createTime": "2015-06-20 23:55:18.0",
                        "createTimeSort": 1434815718000,
                        "education": "\u5b66\u5386\u4e0d\u9650",
                        "financeStage": "\u521d\u521b\u578b(\u672a\u878d\u8d44)",
                        "formatCreateTime": "23:55\u53d1\u5e03",
                        "haveDeliver": false,
                        "industryField": "\u79fb\u52a8\u4e92\u8054\u7f51 \u00b7 \u6570\u636e\u670d\u52a1",
                        "jobNature": "\u5168\u804c",
                        "leaderName": "\u6682\u6ca1\u6709\u586b\u5199",
                        "orderBy": 150,
                        "positionAdvantage": "\u89c6\u80fd\u529b\u800c\u5b9a\uff0c\u85aa\u6c34\u9ad8\u4e8e\u5e02\u573a\u4ef7\u683c",
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

        if ('success' in json and json['success']):
            self.log('---jsonApi return success')
            content = json.get('content')
            if (content != ''):                
                positions = content.get('result')

                detail_urls = []
                for position in positions:
                    positionId = position.get('positionId')
                    if (positionId > 0):
                        detail_url = 'http://www.lagou.com/jobs/' + str(positionId) + '.html'
                        # self.log('~~~start crawl ' + detail_url)
                        # yield scrapy.http.Request(detail_url, callback=self.processDetail)
                        detail_urls.append({ 'url': detail_url, 'position': position })
                    else:
                        self.log('###invalid position id')
                return detail_urls
            else:
                self.log('###empty content')

        else:
            self.log('---jsonApi return failure')

        return []

    def processDetail(self, response):
        self.log('---start job detail: ' + response.url)
        position = response.meta['position']
        jobDescription = response.xpath('//dd[@class="job_bt"]').extract()
        position['website'] = response.xpath('//dl[@class="job_company"]/dd/ul/li/a/text()').extract()
        position['originUrl'] = response.url
        position['fromWhich'] = constants.JobSources.LAGOU
        position['jobDescription'] = jobDescription

        # transfer the dict to the JobItem
        item = items.JobItem() 
        for key in position:
            try:
                item[key] = position[key]
            except KeyError, e:
                pass
        self.log('---end job detail: ' + response.url)
        return item
