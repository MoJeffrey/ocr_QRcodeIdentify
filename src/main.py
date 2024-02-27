import threading
import traceback

import logging
import json

from Thread.Ocr_ThreadPoolExecutor import OCR_ThreadPoolExecutor
from Tools.QRCoder import QRCoder
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

    current_data = OCR_ThreadPoolExecutor.AddResult(result, question.match_name)
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

        if OCR_ThreadPoolExecutor.exist(result):
            return

        logging.info(f"数量 {len(OCR_ThreadPoolExecutor.GetResultSet())}")
        identify(result, Num)
    except Exception as e:
        logging.error(f'{e}')

    return


def ImgRun(logger):
    img = ImageProcessing.readImg('A000000001_1_116.jpg')
    qr_read(img, 1, QRCoder())
    websocketClient.Stop()


def CameraRun(logger, RTSP_URL: int):
    """
    驱动摄像头 获取图片
    :param logger:
    :param RTSP_URL:
    :return:
    """
    camera = RTSCapture.create(RTSP_URL, 'rtsp')
    camera.start_read(RTSP_URL)

    QRCoderList = []
    for i in range(config.Sys_MAX_WORKER):
        QRCoderList.append(QRCoder())

    Num = 0
    codeIndex = 0
    while True:
        try:
            ok, img = camera.read_latest_frame()
            if not ok or img is None:
                continue

            ImageP = ImageProcessing(img, str(Num))
            ImgList = ImageP.partition()

            for img in ImgList:
                OCR_ThreadPoolExecutor.RunTask(qr_read, img, Num, QRCoderList[codeIndex % config.Sys_MAX_WORKER])
                codeIndex += 1

            Num += 1

        except Exception as e:
            logger.error(f'通道{RTSP_URL} {e}')
            logger.error(f'通道{RTSP_URL} {traceback.print_exc()}')


def main():
    Init()
    logger = logging.getLogger('主线程')

    OCR_ThreadPoolExecutor.Init()
    # CameraRun(logger, int(config.RTSP_URLS[1]))
    for i in config.RTSP_URLS:
        thread = threading.Thread(target=CameraRun, args=(logger, int(i),))
        thread.start()

    # ImgRun(logger)


# main方法
if __name__ == "__main__":
    main()
