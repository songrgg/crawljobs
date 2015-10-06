# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Text

DBSession = scoped_session(sessionmaker())
Base = declarative_base()


class CrawlRule(Base):
    __tablename__ = 'crawl_rules'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    allow_domains = Column(Text)
    url_patterns = Column(Text)  # the url regular expression
    fields_extractions = Column(Text)  # the target page's field extraction rules
    enabled = Column(Integer)  # if the rule is enabled, set 1 else 0
