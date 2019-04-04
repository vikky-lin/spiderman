# -*- coding: utf-8 -*-
import sys
import cx_Oracle
from DBUtils.PooledDB import PooledDB


class OraclePool():
    __pool = None  # 连接池对象
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
        self.conn = OraclePool.__getConn(db_info,self.__pool_cfg)
        self.cursor = self.conn.cursor()

    @staticmethod
    def __getConn(db_info,__pool_cfg):
        # 静态方法，从连接池中取出连接
        # mincached，最少的空闲连接数，如果空闲连接数小于这个数，pool会创建一个新的连接
        # maxcached，最大的空闲连接数，如果空闲连接数大于这个数，pool会关闭空闲连接
        # maxconnections，最大的连接数，
        # blocking，当连接数达到最大的连接数时，在请求连接的时候，如果这个值是True，请求连接的程序会一直等待，直到当前连接数小于最大连接数，如果这个值是False，会报错，
        # maxshared 当连接数达到这个数，新请求的连接会分享已经分配出去的连接
        if OraclePool.__pool is None:
            OraclePool.__pool = PooledDB(cx_Oracle,
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
                                   dsn="%s:%s/%s" % (db_info['host'],db_info['port'], db_info['db'])
                                   )
        return OraclePool.__pool.connection()
        

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
            return self.cursor.execute(sql, args)
        except Exception as e:
            self.close()
            raise e

    # 批量执行
    def executemany(self, sql, args):
        try:
            return self.cursor.executemany(sql, args)
        except Exception as e:
            self.close()
            raise e

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
        # self.commit()
        self.cursor.close()
        self.conn.close()
