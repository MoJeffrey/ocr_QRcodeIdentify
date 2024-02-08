import logging
import multiprocessing
import time
from src.Tools.config import config


# 定义一个任务函数
def cpu_intensive_task(num):
    config.Init_Logging()
    logging.info(f"开始：{num}")
    result = 0
    for i in range(10**7):
        result += i
    logging.info(f"CPU intensive task result:{result}")


if __name__ == "__main__":
    config.Init_Logging()
    processes = []

    num = 0
    time_start = time.time()

    while num < 100:
        p = multiprocessing.Process(target=cpu_intensive_task, args=(num,))
        processes.append(p)
        p.start()
        num += 1

    for task in processes:
        task.join()

    time_end = time.time()
    logging.info("执行时间" + str(time_end - time_start))
