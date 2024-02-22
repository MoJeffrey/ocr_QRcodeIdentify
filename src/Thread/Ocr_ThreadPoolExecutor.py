import threading
from concurrent.futures import ThreadPoolExecutor

from Tools.config import config


class OCR_ThreadPoolExecutor:
    __executor = None
    __lock = None

    __resultSet = set()

    @staticmethod
    def Init(max_workers=config.Sys_MAX_WORKER):
        OCR_ThreadPoolExecutor.__executor = ThreadPoolExecutor(max_workers=max_workers)
        OCR_ThreadPoolExecutor.__lock = threading.Lock()

    @staticmethod
    def RunTask(*args):
        OCR_ThreadPoolExecutor.__executor.submit(*args)

    @staticmethod
    def compare(result: str) -> bool:
        return True
