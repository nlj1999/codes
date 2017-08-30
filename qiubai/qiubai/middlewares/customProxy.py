from qiubai.middlewares.proxy import proxies
import random

class RandomProxy(object):
    def process_request(self, request, spider):
        proxy = random.choice(proxies)
        request.meta['proxy'] = 'http://{}'.format(proxy)
