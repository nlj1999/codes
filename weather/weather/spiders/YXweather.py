# -*- coding: utf-8 -*-
import scrapy

from weather.items import WeatherItem
class YxweatherSpider(scrapy.Spider):
	name = 'YXweather'
	allowed_domains = ['tianqi.com']
	start_urls = []
	cities = ['huangshi', 'beijing', 'wuhan']
	for city in cities:
		start_urls.append('http://' + city + '.tianqi.com')
		
	def parse(self, response):
		items = []
		days = response.xpath('//div[@class="tqshow1"]')
		for day in days:
			item = WeatherItem()
			date = ''
			for datetitle in day.xpath('./h3//text()').extract():
				date += datetitle
			item['date'] = date
			item['week'] = day.xpath('./p//text()').extract()[0]
			item['img'] = day.xpath('./ul/li[@class="tqpng"]/img/@src').extract()[0]
			tq = day.xpath('./ul/li[2]//text()').extract()
			item['temperature'] = ''.join(tq)
			item['weather'] = day.xpath('./ul/li[3]/text()').extract()[0]
			item['wind'] = day.xpath('./ul/li[4]/text()').extract()[0]
			items.append(item)
		return items
		
