FROM python:2.7.10

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com -r requirements.txt

COPY . /usr/src/app
