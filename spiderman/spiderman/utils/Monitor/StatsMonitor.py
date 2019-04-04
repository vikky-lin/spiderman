# -*- coding: utf-8 -*-
from scrapy.statscollectors import MemoryStatsCollector
from scrapy import signals
import socket
from datetime import datetime
from scrapy.utils.project import get_project_settings
from spiderman.utils.DB.OraclePool import OraclePool
from spiderman.utils.DB.MysqlPool import MysqlPool



class StatsMonitor(MemoryStatsCollector):
    _monitor_period = get_project_settings().get("MONITOR_PERIOD",5)

    def __init__(self,crawler):
        self.crawler = crawler

    def spider_monitor(self,spider):
        # print(spider.spider_task_monitor)
        stats = self.crawler.stats.get_stats()
        last_note_time = stats.get('last_note_time',None)
        if last_note_time ==None or (datetime.now()-last_note_time).seconds>self._monitor_period:
            self.crawler.stats.set_value('last_note_time',datetime.now())
            custom_stats = {}
            custom_stats['stat_time'] = stats['last_note_time']
            custom_stats['job_instance_id'] = spider.spider_task_monitor['job_instance_id']
            custom_stats['task_instance_id'] = spider.spider_task_monitor['task_instance_id']
            custom_stats['request'] = stats['downloader/request_count']
            custom_stats['filtered_request'] = stats.get('dupefilter/filtered',0)
            custom_stats['response'] = stats['downloader/response_count']
            custom_stats['status_200'] = stats['downloader/response_status_count/200']
            custom_stats['status_other'] = stats['downloader/response_count']-stats['downloader/response_status_count/200']
            custom_stats['crawled_pages'] = stats.get('response_received_count',0)
            custom_stats['scraped_items'] = stats.get('item_scraped_count',0)    
            custom_stats['critical'] = stats.get('log_count/CRITICAL',0)
            custom_stats['error'] = stats.get('log_count/ERROR',0)
            custom_stats['warning'] = stats.get('log_count/WARN',0)
            custom_stats['redirect'] = stats.get('redirect_count',0)   # TODO
            custom_stats['retry'] = stats.get('retry/count',0)
            custom_stats['ignored'] = stats.get('httperror/response_ignored_count',0)
            self.update_spider_crawl_monitor(custom_stats,spider)

    def update_spider_task_monitor(self,spider,stats,update_params,flag=None):
        """
        update spider job running status
        param|stats: spider stats
        param|update_params:
              status: 0 pending
                      1 running
                      2 stop
                      3 cancel
                      4 success
              error_flag:
                      1 error happended
              remark: error description
        param|flag: spider open flag
    
        """
        if isinstance(spider._db_link,OraclePool):
            pass
            # base_sql = 'insert into spider_task_monitor({})values({})'
            # for column in list(stats.keys()):
            #     base_sql = base_sql.format(column+',{}',':'+column+',{}')
            # sql = base_sql.replace(',{}','')
            # cursor.execute(sql,stats)
            # cursor.commit()
        elif isinstance(spider._db_link,MysqlPool):
            if flag:
                sub_stats_params = {'project_id','project_name','version','job_instance_id','spider_name','task_instance_id','execute_ip','priority','args','create_time','status','remark'}
                sub_stats = {key: value for key, value in spider.spider_task_monitor.items() if key in sub_stats_params}
                sub_stats.update(update_params)
                spider._db_link.insert_one('spider_task_monitor',sub_stats)
            else:
                sub_stats_params = {'project_id','project_name','job_instance_id','task_instance_id','execute_ip'}
                sub_stats = {key: value for key, value in spider.spider_task_monitor.items() if key in sub_stats_params}
                spider._db_link.update('spider_task_monitor',update_params,sub_stats)


    def update_spider_crawl_monitor(self,custom_stats,spider):
        if isinstance(spider._db_link,OraclePool):
            base_sql = 'insert into spider_crawl_monitor({})values({})'
            sub_stats_params = {'stat_time','job_instance_id','task_instance_id','create_time','request','response','filtered_request','crawled_pages','scraped_items','status_200','status_other','critical','error','warning','redirect','retry','ignored'}
            sub_stats = {key: value for key, value in custom_stats.items() if key in sub_stats_params}
            sub_stats['spider_name']=spider.spider_task_monitor['spider_name']
            sub_stats['create_time']=spider.spider_task_monitor['create_time']
            # sub_stats['remark']=spider.spider_task_monitor['remark']
            for column in list(custom_stats.keys()):
                base_sql = base_sql.format(column+',{}',':'+column+',{}')
            sql = base_sql.replace(',{}','')
            spider._db_link.insert_one('spider_crawl_monitor',sub_stats)
            spider._db_link.commit()
        elif isinstance(spider._db_link,MysqlPool):
            sub_stats_params = {'stat_time','job_instance_id','task_instance_id','request','response','filtered_request','crawled_pages','scraped_items','status_200','status_other','critical','error','warning','redirect','retry','ignored'}
            sub_stats = {key: value for key, value in custom_stats.items() if key in sub_stats_params}
            sub_stats['spider_name']=spider.spider_task_monitor['spider_name']
            sub_stats['create_time']=spider.spider_task_monitor['create_time']
            # sub_stats['remark']=spider.spider_task_monitor['remark']
            # print(sub_stats)
            spider._db_link.insert_one('spider_crawl_monitor',sub_stats)

      
    def spider_opened(self,spider):
        """
        logging spider job state into spider_task_monitor
        """
        stats = self.crawler.stats.get_stats()
        # if spider._kwargs.get('is_timer_task',True):
        spider.spider_task_monitor = {}
        spider.spider_task_monitor['project_id'] = spider._kwargs.get('project_id','unkown')  # TODO 
        spider.spider_task_monitor['project_name'] = spider._kwargs.get('project_name','unkown')
        spider.spider_task_monitor['version'] = spider._kwargs.get('_version','unkown')
        spider.spider_task_monitor['job_instance_id'] = spider._kwargs.get('task_id','unkown')
        spider.spider_task_monitor['spider_name'] = spider.name
        spider.spider_task_monitor['task_instance_id'] = spider._kwargs.get('_job','unkown')
        spider.spider_task_monitor['execute_ip'] = socket.gethostbyname(socket.gethostname())
        spider.spider_task_monitor['priority'] = spider._kwargs.get('priority','0')
        spider.spider_task_monitor['args'] = spider._kwargs.get('args',None)
        spider.spider_task_monitor['create_time'] = spider._kwargs.get('create_time',datetime.now())
        update_params = {'status':1}
        self.update_spider_task_monitor(spider,stats,update_params,flag=1)

      
    def spider_closed(self,spider):
        """
        logging spider job state into spider_task_monitor
        TODO 获取人为取消信号
        """
        stats = self.crawler.stats.get_stats()
        if stats.get('log_count/ERROR',0) != 0:
            update_params = {'status':4,'error_flag':1}
            self.update_spider_task_monitor(spider,stats,update_params)
        else:
            update_params = {'status':4}
            self.update_spider_task_monitor(spider,stats,update_params)

    def spider_error(self,spider):
        """
        logging spider job state into spider_task_monitor when error occcured
        """
        stats = self.crawler.stats.get_stats()
        update_params = {'error_flag':1}
        self.update_spider_task_monitor(spider,stats,update_params)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        if not get_project_settings().get("STATS2DB",False):
            return
        s = cls(crawler)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_monitor, signal=signals.response_received)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(s.spider_error, signal=signals.spider_error)
        # crawler.signals.connect(s.spider_error, signal=signals)
        return s


