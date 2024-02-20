import re
import traceback

import logging
import time
import json
from concurrent.futures import ThreadPoolExecutor

from Tools.QRCoder import QRCoder
from Tools.RedisTool import RedisTool
from Tools.config import config
from Tools.questionsDTO import QuestionsDTO
from Tools.ImageProcessing import ImageProcessing
from Tools.RTSCapture import RTSCapture
from Tools.websocketClient import websocketClient


def passFun(*obj):
    pass


def Init():
    config().Init()
    websocketClient.Init()

    if not config.IMG_SHOW:
        ImageProcessing.show = passFun

    if not config.IMG_SAVE:
        ImageProcessing.save = passFun


# 对码进行循环识别
def identify(result, Num):
    logger = logging.getLogger('对码识别')
    logger.info = passFun

    # 对识别的结果进行编号截取及格式转换
    logger.info(f'识别结果 = {result}')

    question = QuestionsDTO(result)
    question.identify()

    # 对问题编号进行判断，如果不存在，则进行存储，用于后续的判断
    if not RedisTool.exists(question.match_name):
        RedisTool.set(question.match_name, json.dumps([]))

    current_data = json.loads(RedisTool.get(question.match_name))
    if result in current_data:
        return

    current_data.append(result)
    RedisTool.set(question.match_name, json.dumps(current_data))

    if len(current_data) != question.data_all_num:
        return

    data = QuestionsDTO.splicing(current_data)
    data = json.loads(data)
    data['code'] = question.match_name
    websocketClient.send(data)


# 开始识别帧中二维码
def qr_read(img, Num, coder: QRCoder):
    try:
        result = coder.qrRead(img)

        # 判断二维码数据，如果二维码数据为空
        if result is None:
            return

        identify(result, Num)
    except Exception as e:
        logging.error(f'{e}')

    return


def ImgRun(logger, QRCoderList):
    img = ImageProcessing.readImg('Q000000001_1_1.jpg')
    qr_read(img, 1, QRCoderList[0])
    websocketClient.Stop()


def CameraRun(logger, QRCoderList):
    """
    驱动摄像头 获取图片
    :param logger:
    :param QRCoderList:
    :return:
    """
    executor = ThreadPoolExecutor(max_workers=config.Sys_MAX_WORKER)
    camera = RTSCapture.create(int(config.RTSP_URLS[0]), 'rtsp')
    camera.start_read()

    Num = 0
    while True:
        try:
            ok, img = camera.read_latest_frame()
            if not ok or img is None:
                continue

            ImageP = ImageProcessing(img)
            ImgList = ImageP.partition()

            codeIndex = 0
            for img in ImgList:
                executor.submit(qr_read, img, Num, QRCoderList[codeIndex])
                codeIndex += 1
                Num += 1
            time.sleep(config.OTHER_PAUSE_TIME)

        except Exception as e:
            logger.error(e)
            logger.error(traceback.print_exc())


def main():
    Init()
    logger = logging.getLogger('主线程')
    codeNum = config.IMG_WIDTH_QUANTITY * config.IMG_HIGH_QUANTITY

    QRCoderList = []
    for i in range(codeNum):
        QRCoderList.append(QRCoder())

    RedisTool()
    RedisTool.connect()
    CameraRun(logger, QRCoderList)
    # ImgRun(logger, QRCoderList)


# main方法
if __name__ == "__main__":
    main()
