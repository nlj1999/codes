# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
class QiubaiPipeline(object):
    def process_item(self, item, spider):
        with open(os.getcwd() + '/qiubai/result/qiubai.txt', 'a+') as f:
            f.write('作者: {}\n{}\n点赞: {} \t 评论: {}\n\n'.format(
            item['auther'].encode('utf-8'),
            item['content'].encode('utf-8'),
            item['funNum'].encode('utf-8'),
            item['comNum'].encode('utf-8')))
        return item
