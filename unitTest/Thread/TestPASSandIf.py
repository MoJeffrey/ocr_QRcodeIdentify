import logging
import time

from Tools.config import config


def passFunc():
    Run = False
    time_start = time.time()
    time_list = []
    N = 0
    while True:
        pass
        N += 1

        if N % (10 ** 7) == 0:
            time_end = time.time()
            logging.info(f"[{N}]执行时间" + str(time_end - time_start))

        if N % (10 ** 9) == 0:
            time_end = time.time()
            logging.info("总执行时间" + str(time_end - time_start))
            return

def ifFunc():
    Run = False
    time_start = time.time()
    time_list = []

    N = 0
    while True:
        if Run:
            print("进入")

        N += 1

        if N % (10 ** 7) == 0:
            time_end = time.time()
            logging.info(f"[{N}]执行时间" + str(time_end - time_start))

        if N % (10 ** 9) == 0:
            time_end = time.time()
            logging.info("总执行时间" + str(time_end - time_start))
            return


if __name__ == "__main__":
    config.Init_Logging()
    logging.info('开始')
    passFunc()
    ifFunc()
