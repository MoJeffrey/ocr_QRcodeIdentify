import logging
import os
from concurrent.futures import ThreadPoolExecutor

from Tools.ImageProcessing import ImageProcessing
from Tools.RTSCapture import RTSCapture
from Tools.config import config


def run(camera, name):
    N = 0
    logging.info("开始")
    while camera.isStarted():

        ok, img = camera.read_latest_frame()
        if not ok or img is None:
            continue

        ImageP = ImageProcessing(img, name)
        logging.info("储存")


config.Init_Logging()
config.FRAME_FOLDER_PHAT = os.getcwd() + "\img"

executor = ThreadPoolExecutor(max_workers=4)

cameraList = []

for i in range(2):
    c = RTSCapture.create(i, 'rtsp')
    c.start_read()
    cameraList.append(c)


n = 0
for camera in cameraList:
    executor.submit(run, camera, n)
    n += 1

