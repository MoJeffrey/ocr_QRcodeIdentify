import logging

import redis

from Tools.config import config


class RedisConnectDTO:
    host: str = None
    port: int = None
    db: int = None
    socket_timeout: int = 1
    password: str = None

    def __init__(self):
        self.host = config.REDIS_HOST
        self.port = config.REDIS_PORT
        self.db = config.REDIS_DB
        self.password = config.REDIS_PASSWORD

    def get(self):
        return {
            "host": self.host,
            "port": self.port,
            "db": self.db,
            "password": self.password,
            "socket_timeout": self.socket_timeout
        }


class RedisTool:
    __redis_client = None
    __ConnectDTO: RedisConnectDTO = None
    __logger = None

    def __init__(self):
        RedisTool.__ConnectDTO = RedisConnectDTO()
        RedisTool.__redis_client = redis.Redis(**RedisTool.__ConnectDTO.get())
        RedisTool.__logger = logging.getLogger('RedisTools')

    @staticmethod
    def flush():
        RedisTool.__redis_client.flushdb()
        RedisTool.__logger.info('Redis链接成功！清空')

    @staticmethod
    def connect():
        while True:
            try:
                if RedisTool.__redis_client.ping():
                    RedisTool.__logger.info('Redis链接成功！')
                    break
            except redis.exceptions.TimeoutError:
                RedisTool.__logger.info('连接超时，等待重试...')
            except redis.exceptions.RedisError as e:
                RedisTool.__logger.info(f'发生Redis错误: {e}')
                break

    @staticmethod
    def exists(name) -> bool:
        return RedisTool.__redis_client.exists(name)

    @staticmethod
    def set(name, data):
        RedisTool.__redis_client.set(name, data)

    @staticmethod
    def get(name) -> str:
        return RedisTool.__redis_client.get(name)
