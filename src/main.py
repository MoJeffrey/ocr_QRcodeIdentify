import re
import traceback

import logging
import time
import json
from concurrent.futures import ThreadPoolExecutor

from Thread.Ocr_ThreadPoolExecutor import OCR_ThreadPoolExecutor
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
    """
    对识别后的二维码进行Redis 比对
    比对成功后转发给后端
    :param result: 二维码 识别后的String 数据
    :param Num: 第多少张二维码。 方便bug追踪
    :return:
    """
    logger = logging.getLogger('对码识别')
    logger.info = passFun

    # 对识别的结果进行编号截取及格式转换
    logger.info(f'识别结果 = {result}')

    question = QuestionsDTO(result)
    question.identify()

    redis = RedisTool()
    # 对问题编号进行判断，如果不存在，则进行存储，用于后续的判断
    if not redis.exists(question.match_name):
        redis.set(question.match_name, json.dumps([]))

    current_data = json.loads(redis.get(question.match_name))
    if result in current_data:
        return None

    current_data.append(result)
    redis.set(question.match_name, json.dumps(current_data))
    # 数据拼接
    if len(current_data) == question.data_all_num:
        data = QuestionsDTO.splicing(current_data)
        data = json.loads(data)
        data['code'] = question.match_name
        websocketClient.send(data)

    return result


# 开始识别帧中二维码
def qr_read(img, Num, coder: QRCoder):
    try:
        result = coder.qrRead(img)

        # 判断二维码数据，如果二维码数据为空
        if result is None:
            return

        # if OCR_ThreadPoolExecutor.exist(result):
        #     return

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
    OCR_ThreadPoolExecutor.Init()
    camera = RTSCapture.create(int(config.RTSP_URLS[0]), 'rtsp')
    camera.start_read()

    Num = 0
    while True:
        try:
            ok, img = camera.read_latest_frame()
            if not ok or img is None:
                continue

            ImageP = ImageProcessing(img, str(Num))
            ImgList = ImageP.partition()

            codeIndex = 0
            for img in ImgList:
                OCR_ThreadPoolExecutor.RunTask(qr_read, img, Num, QRCoderList[codeIndex])
                codeIndex += 1

            time.sleep(config.OTHER_PAUSE_TIME)
            Num += 1
        except Exception as e:
            logger.error(e)
            logger.error(traceback.print_exc())


def main():
    Init()
    logger = logging.getLogger('主线程')

    QRCoderList = []
    print(config.Sys_MAX_WORKER)
    for i in range(config.Sys_MAX_WORKER):
        QRCoderList.append(QRCoder())

    RedisTool.Init()
    CameraRun(logger, QRCoderList)
    # ImgRun(logger, QRCoderList)


# main方法
if __name__ == "__main__":
    main()
