import cv2

from Tools.QRCoder import QRCoder

if __name__ == '__main__':
    image = cv2.imread('0.jpg')

    param = {
        "detector_prototxt_path": "../caffe/detect.prototxt",
        "detector_caffe_model_path": "../caffe/detect.caffemodel",
        "super_resolution_prototxt_path": "../caffe/sr.prototxt",
        "super_resolution_caffe_model_path": "../caffe/sr.caffemodel"
    }
    coder = cv2.wechat_qrcode.WeChatQRCode(**param)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results, points = coder.detectAndDecode(gray)

    print(results)
    print('长度' + str(len(results[0])))
    print(points)
