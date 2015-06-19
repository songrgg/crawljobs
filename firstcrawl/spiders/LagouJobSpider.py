import scrapy
import re

from firstcrawl.items import JobItem

class DmozSpider(scrapy.Spider):
	name = "dmoz"
	allowed_domains = ["dmoz.org"]
	start_urls = [
		"http://www.lagou.com/zhaopin/"
	]

	patterns = {
		'lagou': re.compile(r'www\.lagou\.com/jobs/\d+\.html')
	}

	def parse(self, response):
		# check if the job detail page
		for source, pattern in self.patterns:
			match = pattern.match(response.url)
			if (match):
				# process the job detail page
				self.log('be to processing the job detail page ' + match.group())
				yield JobItem(source=match.group())

		
		# job list
