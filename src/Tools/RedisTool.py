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
            "socket_timeout": self.socket_timeout,
            "max_connections": config.Sys_MAX_WORKER,
        }


class RedisTool:
    __redis_client = None
    __redis_Pool = None
    __ConnectDTO: RedisConnectDTO = None
    __logger = None

    def __init__(self):
        self.__redis_client = redis.Redis(connection_pool=RedisTool.__redis_Pool)

    @staticmethod
    def Init():
        RedisTool.__ConnectDTO = RedisConnectDTO()
        RedisTool.__redis_Pool = redis.ConnectionPool(**RedisTool.__ConnectDTO.get())
        RedisTool.__logger = logging.getLogger('RedisTools')

    def flush(self):
        self.__redis_client.flushdb()
        RedisTool.__logger.info('Redis链接成功！清空')

    def connect(self):
        while True:
            try:
                if self.__redis_client.ping():
                    RedisTool.__logger.info('Redis链接成功！')
                    break
            except redis.exceptions.TimeoutError:
                RedisTool.__logger.info('连接超时，等待重试...')
            except redis.exceptions.RedisError as e:
                RedisTool.__logger.info(f'发生Redis错误: {e}')
                break

    def exists(self, name) -> bool:
        return self.__redis_client.exists(name)

    def set(self, name, data):
        self.__redis_client.set(name, data)

    def get(self, name) -> str:
        return self.__redis_client.get(name)
