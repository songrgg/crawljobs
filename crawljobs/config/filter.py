#!/usr/bin/python
#-*-coding:utf-8-*-

from scrapy.dupefilters import RFPDupeFilter

class CustomURLFilter(RFPDupeFilter):

    def __init__(self, path=None, debug=False):
        self.urls_seen = set()
        RFPDupeFilter.__init__(self, path=path, debug=debug)

    # pass the [POST] method requests
    def request_seen(self, request):
        if (request.method == 'POST'):
            return False

        if (request.url in self.urls_seen):
            return True
        else:
            self.urls_seen.add(request.url)

        return False
