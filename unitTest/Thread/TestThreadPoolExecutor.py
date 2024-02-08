import concurrent
from concurrent.futures import ThreadPoolExecutor
import time
import logging
from src.Tools.config import config


# 定义一个任务函数
def cpu_intensive_task(num):
    logging.info(f"开始：{num}")
    result = 0
    for i in range(10**7):
        result += i
    logging.info(f"CPU intensive task result:{result}")


if __name__ == "__main__":
    config.Init_Logging()
    executor = ThreadPoolExecutor(max_workers=50)
    task_list = []

    time_start = time.time()
    Num = 0
    while Num < 100:
        task = executor.submit(cpu_intensive_task, Num)
        task_list.append(task)
        Num += 1

    for task in task_list:
        task.result()

    time_end = time.time()
    logging.info("执行时间" + str(time_end - time_start))
