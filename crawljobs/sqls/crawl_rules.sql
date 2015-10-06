CREATE TABLE crawl_rules(
    id int(10) NOT NULL AUTO_INCREMENT, -- primary key
    name varchar(100) NOT NULL, -- config name
    allow_domains text NOT NULL, -- allow domains
    url_patterns text NOT NULL,
    fields_extractions text NOT NULL,
    enabled int NOT NULL DEFAULT 1,
    primary key(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


INSERT INTO crawl_rules(name, allow_domains, url_patterns, fields_extractions)
VALUES (
    'neitui',
    '["www.neitui.me"]',
    '[{"pattern": "www\\\\.neitui\\\\.me/.*page=.*", "type": "medium"}, {"pattern": "www\\\\.neitui\\\\.me/.*name=job&handle=detail&id=\\\\d+.*", "type": "target"}]',
    '{"website": {"xpath": "//a[@class=\\"defaulta bluea\\"]/@href"}, "companySize": {"xpath": "//dl[@class=\\"ci_body\\"][2]/dd[1]/text()"}, "positionName": {"xpath": "//div[@class=\\"jobnote\\"]/strong/text()"}, "companyName": {"xpath": "//span[@class=\\"jobtitle-l\\"]/text()"}, "originUrl": {"expr": "response.url"}, "workYear": {"xpath": "//span[@class=\\"padding-r10 experience\\"]/text()"}, "financeStage": {"xpath": "//dl[@class=\\"ci_body\\"][2]/dd[3]/text()"}, "salary": {"xpath": "//span[@class=\\"padding-r10 pay\\"]/text()"}, "city": {"xpath": "//span[@class=\\"jobtitle-r\\"]/text()", "to": "city"}, "companyLogo": {"xpath": "//div[@class=\\"img\\"]/a/img/@src"}, "positionId": {"expr": "re.match(r\\".*id=(\\\\d+).*\\", response.url).group(1)"}, "industryField": {"xpath": "//dl[@class=\\"ci_body\\"][2]/dd[2]/text()"}, "jobDescription": {"xpath": "//div[@class=\\"jobdetail nooverflow\\"]"}, "fromWhich": {"value": "neitui"}}');

INSERT INTO crawl_rules(name, allow_domains, url_patterns, fields_extractions)
VALUES (
    'neitui',
    '["www.neitui.me"]',
    '[{"pattern": ".*page=.*", "type": "medium"}, {"pattern": ".*name=job&handle=detail&id=.*", "type": "target"}]',
    '{"website": {"xpath": "//a[@class=\\"defaulta bluea\\"]/@href"}, "companySize": {"xpath": "//dl[@class=\\"ci_body\\"][2]/dd[1]/text()"}, "positionName": {"xpath": "//div[@class=\\"jobnote\\"]/strong/text()"}, "companyName": {"xpath": "//span[@class=\\"jobtitle-l\\"]/text()"}, "originUrl": {"expr": "response.url"}, "workYear": {"xpath": "//span[@class=\\"padding-r10 experience\\"]/text()"}, "financeStage": {"xpath": "//dl[@class=\\"ci_body\\"][2]/dd[3]/text()"}, "salary": {"xpath": "//span[@class=\\"padding-r10 pay\\"]/text()"}, "city": {"xpath": "//span[@class=\\"jobtitle-r\\"]/text()", "to": "city"}, "companyLogo": {"xpath": "//div[@class=\\"img\\"]/a/img/@src"}, "positionId": {"expr": "re.match(r\\".*id=(\\\\d+).*\\", response.url).group(1)"}, "industryField": {"xpath": "//dl[@class=\\"ci_body\\"][2]/dd[2]/text()"}, "jobDescription": {"xpath": "//div[@class=\\"jobdetail nooverflow\\"]"}, "fromWhich": {"value": "neitui"}}');
