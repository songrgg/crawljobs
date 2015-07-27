# 项目目的
爬取中国互联网招聘职位信息，用于之后搭建职位搜索引擎网站``yongwu.org``。

# 技术细节
## 容器化
基于``Docker``构建爬虫，依赖``docker``，``docker-compose``工具。
## 存储
基于``MySQL``的数据持久化，依赖于另一容器提供的``MySQL``服务。
## 调度模块
构建一个调度服务，用来注册爬虫服务，爬取内容的逻辑，申请查询下一个爬取的url，添加新url，查询爬取规则。使用Redis存储链接。

##爬虫
``$ git clone https://github.com/songrgg/crawljobs.git``  
``$ cd crawljobs``  
``$ docker-compose up -d scrapy``  
