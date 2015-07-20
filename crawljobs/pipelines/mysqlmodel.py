from contextlib import contextmanager

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Text
import datetime

DBSession = scoped_session(sessionmaker())
Base = declarative_base()


class JobModel(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)

    city = Column(String(20), nullable=False)
    companyLogo = Column(String(30))
    companySize = Column(Integer)
    companyName = Column(String(30), nullable=False)
    industryField = Column(String(30))
    financeStage = Column(String(30))
    website = Column(String(30))

    salary = Column(Integer, nullable=False)
    jobNature = Column(String(50))
    createTime = Column(DateTime, default=datetime.datetime.now, nullable=False)
    positionName = Column(String(30), nullable=False)
    positionType = Column(String(30))
    positionAdvantage = Column(String(30))
    positionFirstType = Column(String(30))
    jobDescription = Column(Text)
    workTime = Column(String(30))

    minWorkYear = Column(Integer, nullable=False)
    maxWorkYear = Column(Integer, nullable=False)
    education = Column(String(20))

    positionId = Column(Integer)
    originUrl = Column(String(30))
    fromWhich = Column(String(30))
