# -*- coding: utf-8 -*-

"""
使用DBUtils数据库连接池中的连接，操作数据库
OperationalError: (2006, ‘MySQL server has gone away’)
"""
import json
import pymysql
import datetime
from DBUtils.PooledDB import PooledDB
import pymysql
import logging


class MysqlPool():
    __pool = None   # 连接池对象
    __pool_cfg = {}

    def __init__(self,db_info = None,pool_cfg = {}):
        if not db_info.get('charset',False):
            db_info['charset'] = 'utf8mb4'
        self.__pool_cfg['mincached'] = pool_cfg.get('mincached',10)
        self.__pool_cfg['maxcached'] = pool_cfg.get('maxcached',20)
        self.__pool_cfg['maxshared'] = pool_cfg.get('maxshared',10)
        self.__pool_cfg['maxconnections'] = pool_cfg.get('maxconnections',200)
        self.__pool_cfg['blocking'] = pool_cfg.get('blocking',True)
        self.__pool_cfg['maxusage'] = pool_cfg.get('maxusage',100)
        self.__pool_cfg['setsession'] = pool_cfg.get('setsession',None)
        self.__pool_cfg['reset'] = pool_cfg.get('reset',True)
        # 连接池方式
        self.db_info = db_info
        self.conn = MysqlPool.__getConn(db_info,self.__pool_cfg)
        self.cursor = self.conn.cursor()

    @staticmethod
    def __getConn(db_info,__pool_cfg):
        # 静态方法，从连接池中取出连接
        # mincached，最少的空闲连接数，如果空闲连接数小于这个数，pool会创建一个新的连接
        # maxcached，最大的空闲连接数，如果空闲连接数大于这个数，pool会关闭空闲连接
        # maxconnections，最大的连接数，
        # blocking，当连接数达到最大的连接数时，在请求连接的时候，如果这个值是True，请求连接的程序会一直等待，直到当前连接数小于最大连接数，如果这个值是False，会报错，
        # maxshared 当连接数达到这个数，新请求的连接会分享已经分配出去的连接
        if MysqlPool.__pool is None:
            MysqlPool.__pool = PooledDB(pymysql,
                                   mincached=__pool_cfg['mincached'], 
                                   maxcached=__pool_cfg['maxcached'],
                                   maxshared=__pool_cfg['maxshared'], 
                                   maxconnections=__pool_cfg['maxconnections'], 
                                   blocking=__pool_cfg['blocking'],
                                   maxusage=__pool_cfg['maxusage'], 
                                   setsession=__pool_cfg['setsession'], 
                                   reset=__pool_cfg['reset'],
                                   user=db_info['username'],
                                   passwd=db_info['password'],
                                   charset=db_info['charset'],
                                   host=db_info['host'], 
                                   port=db_info['port'], 
                                   db=db_info['db'],
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
        return MysqlPool.__pool.connection()

    # 执行sql
    def execute_query_batch(self, sql, args={}):
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            self.close()
            raise e

    # 执行sql
    def execute(self, sql, args={}):
        try:
            self.cursor.execute(sql, args)
            return self.cursor
        except Exception as e:
            self.close()
            raise e

    def insert_one(self,table_name,params={}):
        sql = 'insert into {}({}) values({})'.format(table_name,','.join(list(params.keys())),','.join(['%s']*params.__len__()))
        self.cursor.execute(sql,list(params.values()))
        self.commit()
        # self.close()

    def insert_many(self,table_name,params_list=[]):
        for params in params_list:
            sql = 'insert into {}({}) values({})'.format(table_name,','.join(list(params.keys())),','.join(['%s']*params.__len__()))
            self.cursor.execute(sql,list(params.values()))
        self.commit()
        # self.close()

    def update(self,table_name,params={},conditions={1:1}):
        exec_part = '{0}=%s {1}'
        for item in list(params.keys()):
            exec_part = exec_part.format(item,',{0}=%s {1}')
        exec_part = exec_part.replace(',{0}=%s {1}','')
        condition_part = '{0}=%s {1}'
        for item in list(conditions.keys()):
            condition_part = condition_part.format(item,'and {0}=%s {1}')
        condition_part = condition_part.replace('and {0}=%s {1}','')
        sql = 'update {} set {} where {}'.format(table_name,exec_part,condition_part)
        # logging.error(sql)
        self.cursor.execute(sql,list(params.values())+list(conditions.values()))
        self.commit()

    # 提交
    def commit(self):
        self.conn.commit()

    # 回滚
    def rollback(self):
        self.conn.rollback()

    # 销毁
    def __del__(self):
        self.close()

    # 关闭连接
    def close(self):
        self.cursor.close()
        self.conn.close()

    
    # def __get_conn(self):
    #     self._conn = self.__pool.connection()
    #     self._cursor = self._conn.cursor()

    # def close(self):
    #     try:
    #         self._cursor.close()
    #         self._conn.close()
    #     except Exception as e:
    #         print e

    # def __execute(self, sql, param=()):
    #     count = self._cursor.execute(sql, param)
    #     print count
    #     return count

    # @staticmethod
    # def __dict_datetime_obj_to_str(result_dict):
    #     """把字典里面的datatime对象转成字符串，使json转换不出错"""
    #     if result_dict:
    #         result_replace = {k: v.__str__() for k, v in result_dict.keys() if isinstance(v, datetime.datetime)}
    #         result_dict.update(result_replace)
    #     return result_dict

    # def select_one(self, sql, param=()):
    #     """查询单个结果"""
    #     count = self.__execute(sql, param)
    #     result = self._cursor.fetchone()
    #     """:type result:dict"""
    #     result = self.__dict_datetime_obj_to_str(result)
    #     return count, result

    # def select_many(self, sql, param=()):
    #     """
    #     查询多个结果
    #     :param sql: qsl语句
    #     :param param: sql参数
    #     :return: 结果数量和查询结果集
    #     """
    #     count = self.__execute(sql, param)
    #     result = self._cursor.fetchall()
    #     """:type result:list"""
    #     [self.__dict_datetime_obj_to_str(row_dict) for row_dict in result]
    #     return count, result

    # def execute(self, sql, param=()):
    #     count = self.__execute(sql, param)
    #     return count

    # def begin(self):
    #     """开启事务"""
    #     self._conn.autocommit(0)

    # def end(self, option='commit'):
    #     """结束事务"""
    #     if option == 'commit':
    #         self._conn.autocommit()
    #     else:
    #         self._conn.rollback()

if __name__ == '__main__':
    DB_INFO = {
        "username": "root",
        "password": "admin",
        "host": "127.0.0.1",
        "port": 3306,
        "db": "spiderdb",
    }
    mysql = MysqlPool(DB_INFO)
    # print(mysql.execute('select * from spider_crawl_stats').fetchone())
    dd = {'stat_time':'1','spider_job_id':'1'}

    sql = 'insert into spider_crawl_stats({}) values({})'.format(','.join(list(dd.keys())),','.join(['%s']*dd.__len__()))
    print(sql)
    # sub_stats_params = {'stat_time','spider_job_id','request_bytes','request_count','response_count','status_200_count','status_other_count','error_count','remark','MSFT'}
    # sub_stats = {key: value for key, value in stats.keys() if key in sub_stats_params}
    # for column in list({'stat_time':'test'}.keys()):
    #     base_sql = base_sql.format(column+',{}',':'+column+',{}')
    # sql = base_sql.replace(',{}','')
    # sql = "insert into spider_crawl_stats(stat_time) values(%s)"
    print(list(dd.values()))
    mysql.execute(sql,list(dd.values()))
    mysql.commit()