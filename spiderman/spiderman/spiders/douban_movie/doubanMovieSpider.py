from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

class doubanMovieSpider(CrawlSpider):
    name = 'douban_mv'
    start_urls = ['https://movie.douban.com/top250']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS':{
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'movie.douban.com',
            'Referer': 'https://movie.douban.com/top250',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100000 Firefox/63.0'
        }
    }
    rules = [
        Rule(LinkExtractor(allow=(r'start=\d*')),follow=True),
        Rule(LinkExtractor(allow=(r'subject/\d*')),follow=False,callback='parse_detail')
    ]

    def parse_detail(self,response):
        print(SpiderStats)
        item = {}
        item['top250-no'] = response.xpath('//div[@class="top250"]//span[@class="top250-no"]//text()').extract_first()
        yield item
    