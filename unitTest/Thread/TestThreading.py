import logging
import threading
import time

from Tools.config import config


# 定义一个 CPU 密集型的计算任务
def cpu_intensive_task(num):
    logging.info(f"开始：{num}")
    result = 0
    for i in range(10**7):
        result += i
    logging.info(f"CPU intensive task result:{result}")


if __name__ == "__main__":
    config.Init_Logging()
    # 创建多个线程来执行 CPU 密集型任务
    threads = []
    time_start = time.time()
    Num = 0

    while Num < 100:
        thread = threading.Thread(target=cpu_intensive_task, args=(Num, ))
        threads.append(thread)
        thread.start()
        Num += 1

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    time_end = time.time()
    logging.info("执行时间" + str(time_end - time_start))
