# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse
import random
import time


user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

proxy_http = ['125.27.10.150:56292','114.34.168.157:46160']
proxy_https = ['1.20.101.81:35454','113.78.254.156:9000']

class UAPool(UserAgentMiddleware):  # UA池,存放请求头
    def process_request(self, request, spider):
        ua = random.choices(user_agent_list)
        request.headers['User-Agent'] = ua
        # print(request.headers['User-Agent'])



class NewsproDownloaderMiddleware(object):  # 下载中间件

    # def process_request(self, request, spider):
    #     if request.url.split(':')[0] == 'https':    # 代理池
    #         request.meta['proxy'] = 'https://' + random.choice(proxy_https)
    #     else:
    #         request.meta['proxy'] = 'http://' + random.choice(proxy_http)
    #     print(request.meta['proxy'])
    #     return None

    def process_response(self, request, response, spider):    # scrapy框架中使用selenium模拟浏览器
        # 使用selenium获取动态加载出来的数据
        '''
        spider 就是我们写的news.py里的实例化类
        print(self,type(self))   # <newsPro.middlewares.NewsproDownloaderMiddleware object at 0x00000194D19F75F8> <class 'newsPro.middlewares.NewsproDownloaderMiddleware'>
        print(request,type(request))   # <GET http://news.163.com/domestic/> <class 'scrapy.http.request.Request'>
        print(response,type(response)) # <200 http://news.163.com/domestic/> <class 'scrapy.http.response.html.HtmlResponse'>
        print(spider,type(spider))     # <NewsSpider 'news' at 0x194d19c4240> <class 'newsPro.spiders.news.NewsSpider'>
        '''
        if request.url in ['http://news.163.com/domestic/']:  # 这里的url也可以放到spider对象中
            spider.bro.get(request.url)
            time.sleep(2)
            page_text = spider.bro.page_source  # selenium对象封装到了spider的bro方法中
            return HtmlResponse(url=spider.bro.current_url, body=page_text, encoding='utf-8', request=request)  # 重新实例化一个HtmlResponse对象,response也是HtmlResponse对象

        return response


    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
