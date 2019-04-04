from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

class HotMusicSpider(CrawlSpider):
    name = 'hot_music'
    start_urls = ['https://music.163.com/discover/toplist?id=3778678']
    custom_settings = {
        # 'DEFAULT_REQUEST_HEADERS':{
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        #     'Cache-Control': 'max-age=0',
        #     'Connection': 'keep-alive',
        #     'Referer': 'https://email.163.com/',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100000 Firefox/63.0'
        # },
        'DOWNLOADER_MIDDLEWARES' : {
           'spiderman.utils.Middlewares.RandUserAgent.RandUserAgent': 543,
           'spiderman.utils.Middlewares.RandProxy.RandProxy': 543,
        },
        'PIPELINES':{
            'spiderman.pipelines.SpidermanPipeline': 300,
        }
    }
    rules = [
        Rule(LinkExtractor(allow=(r'start=\d*')),follow=True),
        # Rule(LinkExtractor(allow=(r'song?id=\d*')),follow=False,callback='parse_detail')
    ]

    def parse_start_url(self,response):
        print(response.request.headers)
        item = {}
        # music_list = response.xpath('//ul[@class="f-hide"]//li').extract()
        # for song in music_list:
        #     item['update_date'] = response.xpath('//span[@class="sep s-fc3"]//text()').extract_first()
        #     item['rank'] = music_list.xpath('./div[@class="hd"]//span[1]/text()').extract_first()
        #     item['rank'] = music_list.xpath('./div[@class="rk"]//span[2]/text()').extract_first()
        #     yield item


    def parse_detail(self,response):
        item = {}
        item['top250-no'] = response.xpath('//div[@class="top250"]//span[@class="top250-no"]//text()').extract_first()
        yield item
    