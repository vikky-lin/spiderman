# -*- coding:utf8 -*-

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random


class RandUserAgent(UserAgentMiddleware):
    def __init__(self,user_agent_pool):
        super().__init__()
        if user_agent_pool:
            self.CUSTOM_UA = user_agent_pool
        else:
            self.CUSTOM_UA = None
            self.DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{0}.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/{0}.36 Edge/17.17134"
            

    def process_request(self,request,spider):
        if self.CUSTOM_UA:
            request.headers["user-agent"] = random.choice(self.CUSTOM_UA)
        else:
            request.headers["user-agent"] = self.DEFAULT_UA.format(str(random.randint(100,1000)))
    
    @classmethod
    def from_crawler(cls,crawler):
        try:
            return cls(user_agent_pool=USER_AGENT_POOL)
        except:
            return cls(user_agent_pool=None)