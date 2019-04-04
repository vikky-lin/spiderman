
from scrapy.statscollectors import MemoryStatsCollector
from spiderman.utils.Monitor.StatsMonitor import StatsMonitor
from datetime import datetime
from scrapy.utils.project import get_project_settings

class CustomStatsCollector(MemoryStatsCollector):
    def __init__(self,crawler,period=60):
        super(CustomStatsCollector,self).__init__(crawler)
        self.spider_stats = {}
        self.STATS2DB = get_project_settings().get("STATS2DB",False)
        self.period = period
        self._stats_monitor = StatsMonitor()

    def _persist_stats(self, stats, spider):
        custom_stats = {}
        custom_stats['stat_time'] = int(datetime.now().strftime('%Y%m%d%H%M%S'))
        custom_stats['spider_job_id'] = spider.job_id
        custom_stats['request_bytes'] = stats['downloader/request_bytes']
        custom_stats['request_count'] = stats['downloader/request_count']
        custom_stats['response_count'] = stats['downloader/response_count']
        custom_stats['status_200_count'] = stats['downloader/response_status_count/200']
        custom_stats['status_other_count'] = custom_stats['response_count']-custom_stats['status_200_count']
        custom_stats['error_count'] = stats.get('log_count/ERROR',0)
        self.spider_stats[spider.name] = stats
        # print(custom_stats)
        if not self.STATS2DB:
            return
        self._stats_monitor.spider_crawl_stats(spider._db_link,custom_stats)