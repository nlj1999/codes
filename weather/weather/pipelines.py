# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import json
import codecs

class WeatherPipeline(object):
	def process_item(self, item, spider):
		base_dir = os.getcwd()
		filename = base_dir + '/data/weather.txt'
		with open(filename, 'a') as f:
			f.write(item['date'].encode('utf-8') + '\n')
			f.write(item['week'].encode('utf-8') + '\n')
			f.write(item['temperature'].encode('utf-8') + '\n')
			f.write(item['weather'].encode('utf-8') + '\n')
			f.write(item['wind'].encode('utf-8') + '\n')
		with open(base_dir + '/data/' + item['date'] + '.png', 'wb') as f:
			f.write(requests.get(item['img']).content)
		return item
