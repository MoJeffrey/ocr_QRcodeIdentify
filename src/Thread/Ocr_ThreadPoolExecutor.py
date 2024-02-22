import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from sortedcontainers import SortedSet

from Tools.config import config


class OCR_ThreadPoolExecutor:
    __executor = None
    __lock = None

    __resultSet = None

    @staticmethod
    def Init(max_workers=config.Sys_MAX_WORKER):
        OCR_ThreadPoolExecutor.__executor = ThreadPoolExecutor(max_workers=max_workers)
        OCR_ThreadPoolExecutor.__lock = threading.Lock()
        OCR_ThreadPoolExecutor.__resultSet = SortedSet()

    @staticmethod
    def RunTask(*args):
        OCR_ThreadPoolExecutor.__executor.submit(*args)

    @staticmethod
    def exist(result: str) -> bool:
        OCR_ThreadPoolExecutor.__lock.acquire()
        if result in OCR_ThreadPoolExecutor.__resultSet:
            OCR_ThreadPoolExecutor.__lock.release()
            return True
        else:
            OCR_ThreadPoolExecutor.__resultSet.add(result)
            logging.error(f"数量: {len(OCR_ThreadPoolExecutor.__resultSet)}")
            OCR_ThreadPoolExecutor.__lock.release()
            return False
