# -*- coding:utf8 -*-

from scrapy.downloadermiddlewares.cookies import CookiesMiddleware
import random


class RandCookies(CookiesMiddleware):
    def __init__(self,cookies_pool):
        super().__init__()
        if cookies_pool:
            self.CUSTOM_COOKIES = cookies_pool
        else:
            self.CUSTOM_COOKIES = None
            

    def process_request(self,request,spider):
        if self.CUSTOM_COOKIES:
            request.cookies = random.choice(self.CUSTOM_COOKIES)
        else:
            request.cookies = None
    
    @classmethod
    def from_crawler(cls,crawler):
        try:
            return cls(cookies_pool=cookies_pool)
        except:
            return cls(cookies_pool=None)