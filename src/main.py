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
from Tools.HttpUpload import HttpUpload
from Tools.RTSCapture import RTSCapture


def passFun(*obj):
    pass


def Init():
    config().Init()

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
    if question.identify() is not None:
        return result

    # 对问题编号进行判断，如果不存在，则进行存储，用于后续的判断
    if not RedisTool.exists(question.match_name):
        RedisTool.set(question.match_name, json.dumps([]))

    # 获取当前match_name的Redis列表
    current_data = json.loads(RedisTool.get(question.match_name))
    logger.info(f'已获取当前match_name的Redis列表')

    # 将新result添加到列表中
    if result in current_data:
        return None

    current_data.append(result)
    logger.warning(f'{Num}-问题编号：{question.match_name}当前为{question.curr_num}段，需要{question.data_all_num}段 已有{len(current_data)}段')
    RedisTool.set(question.match_name, json.dumps(current_data))
    logger.info(f'已存储到Redis')

    if len(current_data) != question.data_all_num:
        return result

    # 当前段数与数据分段总数相同，则进行排序、拼接
    logger.error('进入拼接程序')
    # 根据第几段信息进行排序
    sorted_data = sorted(current_data, key=lambda x: int(x[x.index('_') + 1:x.index('&')]))
    # 拼接数据
    concatenated_data = ''.join([d[d.index(']') + 1:] for d in sorted_data])
    # 添加问题编号
    concatenated_data = f'[{question.match_name}]{concatenated_data}'
    logging.error(f'打印原数据 = {concatenated_data}')
    # noinspection PyUnusedLocal
    data_all_num = 0

    # http上传请求，将拼接好的数据进行上传
    http_upload = HttpUpload(config.API_URL_IP, config.API_URL_PORT)
    response_data = http_upload.upload_data(config.API_URL, concatenated_data)
    logging.info(f"请求结果: {response_data}")


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


def main():
    Init()

    logger = logging.getLogger('主线程')
    codeNum = config.IMG_WIDTH_QUANTITY * config.IMG_HIGH_QUANTITY

    QRCoderList = []
    for i in range(codeNum):
        QRCoderList.append(QRCoder())

    executor = ThreadPoolExecutor(max_workers=config.Sys_MAX_WORKER)
    RedisTool()
    RedisTool.connect()
    camera = RTSCapture.create(int(config.RTSP_URLS[0]), 'rtsp')
    camera.start_read()

    logger.info(f'已初始化摄像头及二维码检测器')

    if not camera.isStarted():
        logger.error("摄像头未能正确启动！")
        exit(0)

    Num = 0
    while camera.isStarted():
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


# main方法
if __name__ == "__main__":
    main()
