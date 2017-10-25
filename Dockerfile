FROM python:3
MAINTAINER ouyangsong
ADD . /code
WORKDIR /code
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
ENTRYPOINT ["scrapy"]
CMD ["crawl", "articles"]
