# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis

from aip import AipNlp

APP_ID = '14790912'
API_KEY = 'db9r8XomfKdhuWphvzWeWGCV'
SECRET_KEY = 'gpROMOFW6v26WHzhYk2s7TuE2oYs1Il8'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

class NewsproPipeline(object):
    fp = None
    keys = []
    def open_spider(self, spider):
        self.fp = open('./news.html', 'w', encoding='utf-8')
        self.conn = redis.Redis(host='127.0.0.1',port=6379)

    def process_item(self, item, spider):
        title = item['title']
        content = item['content']
        keys_dict = client.keyword(title,content)
        for dic in keys_dict['items']:
            self.keys.append(dic['tag'])
        keys = '/'.join(self.keys)
        type_dic = client.topic(title,content)
        news_type = type_dic['item']['lv1_tag_list'][0]['tag']



        self.fp.write(title + '\n\n' + content + '\n\n'+keys+'\n\n'+news_type)
        dict = {
            'title':title,
            'content':content,
            'keys':keys,
            'news_type':news_type,
        }
        self.conn.lpush('data',dict)

        return item
    def close_spider(self, spider):
        self.fp.close()
