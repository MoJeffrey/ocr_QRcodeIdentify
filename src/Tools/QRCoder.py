import logging
import traceback

import cv2
from Tools.config import config

from Enum.HSVColorEnum import HSVColorEnum


class QRCoder(object):
    coder = None

    def __init__(self, WeChatQRCode=None):
        if WeChatQRCode is None:
            param = {
                "detector_prototxt_path": f"{config.IMG_QRCODE_MODEL_PATH}detect.prototxt",
                "detector_caffe_model_path": f"{config.IMG_QRCODE_MODEL_PATH}detect.caffemodel",
                "super_resolution_prototxt_path": f"{config.IMG_QRCODE_MODEL_PATH}sr.prototxt",
                "super_resolution_caffe_model_path": f"{config.IMG_QRCODE_MODEL_PATH}sr.caffemodel"
            }
            self.coder = cv2.wechat_qrcode.WeChatQRCode(**param)
        else:
            self.coder = WeChatQRCode

    @staticmethod
    def Has_Color(hsv_img, lower_range, upper_range):
        """
        HSV颜色空间
        判断图片是否有该颜色范围
        :param hsv_img:
        :param lower_range:
        :param upper_range:
        :return:
        """
        green_mask = cv2.inRange(hsv_img, lower_range, upper_range)
        white_pixels = cv2.countNonZero(green_mask)
        threshold = 1000
        return white_pixels > threshold

    def detectAndDecode(self, img):
        return self.coder.detectAndDecode(img)

    def qrRead(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 如果是绿色 则直接退出
        if QRCoder.Has_Color(hsv, HSVColorEnum.Green.value.lower, HSVColorEnum.Green.value.upper):
            return None

        try:
            results = self.coder.detectAndDecode(gray)[0]
        except Exception as e:
            return None

        if len(results) == 0:
            return None

        return results[0]
