import time

import cv2

from Tools.ImageProcessing import ImageProcessing
from Tools.QRCoder import QRCoder
from Tools.config import config

# 蓝色
blue = {
    "lower": (100, 50, 50),
    "upper": (140, 255, 255)
}

# 绿色
green = {
    "lower": (40, 40, 40),
    "upper": (80, 255, 255)
}

config().Init()
# ImgFile = 'img.png'
ImgFile = 'A000000001_1_116.jpg'
img = ImageProcessing.readImg(ImgFile)

param = {
    "detector_prototxt_path": "../../src/caffe/detect.prototxt",
    "detector_caffe_model_path": "../../src/caffe/detect.caffemodel",
    "super_resolution_prototxt_path": "../../src/caffe/sr.prototxt",
    "super_resolution_caffe_model_path": "../../src/caffe/sr.caffemodel"
}
qrcode = cv2.wechat_qrcode.WeChatQRCode(**param)
qrcode = QRCoder(qrcode)

startTime = time.time()
index = 0
while True:
    index += 1
    # result = has_blue(img)
    QRCoder.Has_Color(img, green['lower'], blue['upper'])
    if index == 100:
        endTime = time.time()
        break
print("所需時間：", endTime - startTime)
