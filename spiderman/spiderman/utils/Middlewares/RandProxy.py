# -*- coding:utf8 -*-

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import random


class RandProxy(HttpProxyMiddleware):
    def __init__(self,proxy_pool):
        super().__init__()
        if proxy_pool:
            self.CUSTOM_PROXY = proxy_pool
        else:
            self.CUSTOM_PROXY = None
            self.DEFAULT_PROXY = "127.0.0.1:8000"   
            

    def process_request(self,request,spider):
        if self.CUSTOM_PROXY:
            request.headers["Proxy-Authorization"] = random.choice(self.CUSTOM_PROXY)
        else:
            request.headers["Proxy-Authorization"] = self.DEFAULT_PROXY
    
    @classmethod
    def from_crawler(cls,crawler):
        try:
            return cls(proxy_pool=PROXY_POOL)
        except:
            return cls(proxy_pool=None)