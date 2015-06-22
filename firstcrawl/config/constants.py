#!/usr/bin/python
#-*-coding:utf-8-*-

class JobSources(object):
    LAGOU = 1
    NEITU = 2

    MAPPING = {
        LAGOU: 'lagou',
        NEITU: 'neitui'
    }

    def parse(self, source):
        return self.MAPPING.get(source)