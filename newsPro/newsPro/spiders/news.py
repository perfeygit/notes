# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from newsPro.items import NewsproItem

# 无头浏览器的配置
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

class NewsSpider(scrapy.Spider):
    name = 'news'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://news.163.com/domestic/']
    item = NewsproItem()

    def __init__(self):
        # self.bro = webdriver.Chrome()   # 有界面的浏览器
        self.bro = webdriver.Chrome(chrome_options=chrome_options)  # 无头浏览器

    def parse(self, response):
        div_list = response.xpath('//div[@class="ndi_main"]/div')
        for div in div_list:
            title = div.xpath('./div[1]/div[1]/h3/a/text()').extract()  # 应为有的取出来的是空,所以这里没有直接使用extract_first()
            content_url = div.xpath('./div[1]/div[1]/h3/a/@href').extract()
            if title[0]:
                # self.item['title'] = title[0]
                print(title[0])
                yield scrapy.Request(url=content_url[0], callback=self.detail_parse)

    def detail_parse(self, response):
        title = response.xpath("//div[@id='epContentLeft']/h1/text()").extract_first()
        content_list = response.xpath('//div[@id="endText"]/p/text()').extract()
        content = ''.join(content_list)
        self.item['title'] = title
        self.item['content'] = content
        yield self.item

    def closed(self, spider):
        self.bro.quit()
