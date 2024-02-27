import cv2

from Tools.ImageProcessing import ImageProcessing


class QRCoder(object):
    coder = None

    def __init__(self):
        param = {
            "detector_prototxt_path": "src/caffe/detect.prototxt",
            "detector_caffe_model_path": "src/caffe/detect.caffemodel",
            "super_resolution_prototxt_path": "src/caffe/sr.prototxt",
            "super_resolution_caffe_model_path": "src/caffe/sr.caffemodel"
        }
        self.coder = cv2.wechat_qrcode.WeChatQRCode(**param)

    def detectAndDecode(self, img):
        return self.coder.detectAndDecode(img)

    def qrRead(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ImageProcessing.save(gray, '测试')
        results = self.coder.detectAndDecode(gray)[0]
        if len(results) == 0:
            return None

        return results[0]
