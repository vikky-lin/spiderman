# -*- coding:utf8 -*-

from scrapy import Request,Spider
from pydispatch import dispatcher
from scrapy import signals
import re
import time
from bs4 import BeautifulSoup as bs
from spiderman.utils.DB.MysqlPool import MysqlPool
from spiderman.utils.Monitor.StatsMonitor import StatsMonitor
# from spidertool.settings import DB_INFO
from datetime import datetime
from urllib.parse import unquote
import os
import logging
from scrapy.statscollectors import StatsCollector
import uuid
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class cbdioSpider(Spider):
    name = 'cbdio_spider'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
            'spiderman.utils.Monitor.StatsMonitor.StatsMonitor': 543
        },
        'DOWNLOAD_DELAY' : 0.5,
        'LOG_ENABLED' : True,
        'LOG_ENCODING' : 'utf8',
        'LOG_LEVEL' : 'INFO',
        # 'LOG_FILE' : './spidertool/workspace/cbdioSpiders/log_file/cbdioSpider_crawl_log.log'
    }
    hot_label = {
        "大数据政策" : "1",
        "区块链": "1",
        "人工智能": "1",
        "图文直播": "1",
        "非常数据观" : "1",
        "数字经济": "1",
        "数据观专访" : "1",
        "数博会" : "1",
        "贵州大数据" : "1",
        "工业大数据" : "1",
        "大数据分析" : "1",
        "大数据概念" : "1",
        "大数据资讯" : "1",
        "大数据应用" : "1",
        "可视化效果" : "1",
        "大数据门户" : "1"
    }

    def __init__(self,**kwargs):
        """
        params _job: 接收scrapyd传入的job执行任务实例
        """
        logging.debug(kwargs)
        self._kwargs = kwargs
        self.base_url = 'http://www.cbdio.com/'
        self.start_urls = ['http://www.cbdio.com/node_2563.htm']
        self.counter = 0
        DB_INFO = {
            "username": "root",
            "password": "admin",
            "host": "127.0.0.1",
            "port": 3306,
            "db": "spiderdb",
        }
        self._db_link = MysqlPool(DB_INFO)
        # print(mysql.execute('select * from spider_crawl_stats').fetchone())
        # self.ora = OraclePool(DB_INFO)
        # dispatcher.connect(StatsMonitor.spider_monitor, signals.response_received)


    def parse(self,response):
        label_link_list = response.xpath('//div[@class="cb-tag"]//a[@class="cb-tag-item"]/@href').extract()
        label_name_list = response.xpath('//div[@class="cb-tag"]//a[@class="cb-tag-item"]/text()').extract()
        for label_item in zip(label_link_list,label_name_list):
            url = self.base_url+label_item[0]
            yield Request(url,callback=self.parse_detail,meta={'label_name':label_item[1].strip()})
            time.sleep(5)
            # break

    def parse_detail(self,response):
        if response.status == 200:
            if response.url.count('_') == 1:
                # 标签首页处理
                label_item = {}
                label_item['label_name'] = response.meta['label_name']   # 标签名
                label_item['label_website'] = response.url   # 标签链接
                label_item['web_id'] = '1'
                label_item['label_add_website'] = 'http://www.cbdio.com/node_2563.htm'   # 标签来源网站
                label_item['label_img_url'] = self.base_url+response.xpath('//div[@class="am-g cb-tag-wiki"]//img/@src').extract()[0]   # 标签图片
                label_item['is_hot'] = self.hot_label.get(label_item['label_name'],None)   # 热门标签
                label_item['lable_content'] = response.xpath('//p[@class="cb-tag-wiki-intro"]/text()').extract()[0]   # 标签介绍
                label_item['status'] = '1000'
                label_item['create_time'] = datetime.now().strftime('%Y-%m-%d') 
                base_sql = 'insert into tmp_base_label_bdlk_info({})values({})'
                for column in list(label_item.keys()):
                    if column == 'create_time':
                        base_sql = base_sql.format(column+',{}',"to_date(:"+column+",'yyyy-mm-dd hh24:mi'),{}")
                    else:
                        base_sql = base_sql.format(column+',{}',':'+column+',{}')
                sql = base_sql.replace(',{}','')
                # logging.info(label_item)
                # self.ora.execute(sql,label_item)
                # self.ora.commit()

            article_list = response.xpath('//div[@class="cb-media"]//li')
            for article_item in article_list:
                consult_item = {}
                consult_item['consult_title'] = article_item.xpath('.//p[@class="cb-media-title"]//a/text()').extract()[0]
                consult_item['consult_url'] = self.base_url+article_item.xpath('.//p[@class="cb-media-title"]//a/@href').extract()[0]
                consult_item['consult_time'] = article_item.xpath('.//p[@class="cb-media-datetime"]/text()').extract()[0]
                try:
                    consult_item['consult_content'] = article_item.xpath('.//p[@class="cb-media-summary"]/text()').extract()[0]
                except:
                    consult_item['consult_content'] = None
                consult_item['consult_img_url'] = self.base_url+article_item.xpath('.//p[@class="cb-media-thumb am-u-md-4 am-sm-only-text-center"]/a/img/@src').extract()[0]
                consult_item['consult_py_time'] = datetime.now().strftime('%Y-%m-%d %H:%M') 
                consult_item['status'] = '1000'
                # consult_item['label_id'] = response.meta['label_name']
                if consult_item['consult_time'][:10] == datetime.now().strftime('%Y-%m-%d'):
                    '''
                        筛选当天发布文章
                    '''
                    base_sql = 'insert into tmp_base_news_bdlk_info({})values({})'
                    for column in list(consult_item.keys()):
                        if column == 'consult_time' or column == 'consult_py_time':
                            base_sql = base_sql.format(column+',{}',"to_date(:"+column+",'yyyy-mm-dd hh24:mi'),{}")
                        else:
                            base_sql = base_sql.format(column+',{}',':'+column+',{}')
                    sql = base_sql.replace(',{}','')
                    # self.ora.execute(sql,consult_item)
                    # self.ora.commit()
                    # self.ora.close()
                # logging.info(consult_item)

            if consult_item['consult_time'][:10] == datetime.now().strftime('%Y-%m-%d'):
                if response.url.count('_') == 1:
                    next_url = response.url.replace('.htm','_2.htm')
                else:
                    current_page = int(response.url.split('_')[-1].split('.')[0])
                    next_url = '{}_{}_{}.htm'.format(response.url.split('_')[0],response.url.split('_')[1],str(current_page+1))
                    yield Request(next_url,callback=self.parse_detail)


    
    # def spider_closed(self,spider):
    #     logfile = open('./spidertool/workspace/govLocalBidSpiders/log_file/govLocalBidSpider.log','w',encoding='utf8')
    #     logfile.write('retCode:0\n')
    #     logfile.write('retMes:成功')
                

                