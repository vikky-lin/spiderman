# -*- coding: utf-8 -*-
import redis
from scrapy import log


class RedisPool():
    __pool = None

    def __init__(self, redis_info):
        if RedisPool.__pool is None:
            try:
                RedisPool.__pool = redis.ConnectionPool(host=redis_info["ip"], port=redis_info["port"], password=redis_info["password"], db=0)
                log.msg("初始化redis连接池成功")
            except Exception as e:
                log.msg("初始化redis连接池出现异常")

    @staticmethod
    def __get_redis_connection():
        return redis.StrictRedis(connection_pool=RedisPool.__pool)

    @staticmethod
    def lpush_string(key, str):
        try:
            RedisPool.__get_redis_connection().lpush(key, str)
        except Exception as e:
            log.msg("插入redis出现异常")

    @staticmethod
    def insert_string(key, str):
        try:
            RedisPool.__get_redis_connection().set(key,str)
        except Exception as e:
            log.msg("插入redis出现异常")

    @staticmethod
    def get_value(key):
        try:
            return RedisPool.__get_redis_connection().get(key)
        except Exception as e:
            log.msg("获取redis值出现异常！key位:" + key)
