import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from sortedcontainers import SortedSet

from Tools.config import config


class OCR_ThreadPoolExecutor:
    __executor = None
    __lock = None

    __result_dict = None
    __resultSet = None

    @staticmethod
    def Init(max_workers=config.Sys_MAX_WORKER):
        OCR_ThreadPoolExecutor.__executor = ThreadPoolExecutor(max_workers=max_workers)
        OCR_ThreadPoolExecutor.__lock = threading.Lock()
        OCR_ThreadPoolExecutor.__resultSet = SortedSet()
        OCR_ThreadPoolExecutor.__result_dict = {}

    @staticmethod
    def ReSetData():
        logging.info("清除记录")
        OCR_ThreadPoolExecutor.__lock.acquire()
        OCR_ThreadPoolExecutor.__resultSet = SortedSet()
        OCR_ThreadPoolExecutor.__result_dict = {}
        OCR_ThreadPoolExecutor.__lock.release()

    @staticmethod
    def RunTask(*args):
        OCR_ThreadPoolExecutor.__executor.submit(*args)

    @staticmethod
    def GetResultSet():
        return OCR_ThreadPoolExecutor.__resultSet

    @staticmethod
    def GetResultDict():
        return OCR_ThreadPoolExecutor.__result_dict

    @staticmethod
    def exist(result: str) -> bool:
        OCR_ThreadPoolExecutor.__lock.acquire()
        if result in OCR_ThreadPoolExecutor.__resultSet:
            OCR_ThreadPoolExecutor.__lock.release()
            return True
        else:
            OCR_ThreadPoolExecutor.__resultSet.add(result)
            OCR_ThreadPoolExecutor.__lock.release()
            return False

    @staticmethod
    def removeSet(results: list):
        OCR_ThreadPoolExecutor.__lock.acquire()
        for i in results:
            OCR_ThreadPoolExecutor.__resultSet.remove(i)
        OCR_ThreadPoolExecutor.__lock.release()

    @staticmethod
    def AddResult(result: str, code: str):
        OCR_ThreadPoolExecutor.__lock.acquire()
        if code not in OCR_ThreadPoolExecutor.__result_dict:
            OCR_ThreadPoolExecutor.__result_dict[code] = []

        OCR_ThreadPoolExecutor.__result_dict[code].append(result)

        data = OCR_ThreadPoolExecutor.__result_dict[code]
        OCR_ThreadPoolExecutor.__lock.release()
        return data

    @staticmethod
    def DeleteResult(code: str):
        OCR_ThreadPoolExecutor.__lock.acquire()
        data = OCR_ThreadPoolExecutor.__result_dict[code]
        del OCR_ThreadPoolExecutor.__result_dict[code]
        OCR_ThreadPoolExecutor.__lock.release()
        return data
