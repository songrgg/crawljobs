#!/usr/bin/python
#-*-coding:utf-8-*-

class JobSources(object):
    LAGOU = 1
    NEITU = 2

    MAPPING = {
        LAGOU: 'lagou',
        NEITU: 'neitui'
    }

    @classmethod
    def parse(cls, source):
        return cls.MAPPING.get(source)