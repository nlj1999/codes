# -*- coding: utf-8 -*-
import scrapy
from qiubai.items import QiubaiItem

class HotspiderSpider(scrapy.Spider):
    name = 'hotspider'
    allowed_domains = ['qiushibaike.com']
    start_urls = []
    for i in range(1,5):
        start_urls.append('https://www.qiushibaike.com/8hr/page/' + str(i) + '/')
    def parse(self, response):
        item = QiubaiItem()
        main = response.xpath('//div[@id="content-left"]/div')
        for div in main:
            item['auther'] = div.xpath('.//h2/text()').extract()[0].strip()
            item['content'] = ''.join(div.xpath('a[@class="contentHerf"]/div/span[1]/text()').extract()).strip()
            item['funNum'] = div.xpath('.//span[@class="stats-vote"]/i/text()').extract()[0]
            item['comNum'] = div.xpath('.//span[@class="stats-comments"]/a/i/text()').extract()[0]
            yield item
