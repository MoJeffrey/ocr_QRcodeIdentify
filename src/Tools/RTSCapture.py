import logging

import cv2
import threading


class RTSCapture(cv2.VideoCapture):
    __url = None
    _cur_frame = None
    _reading = False
    __logger = logging.getLogger('RTSCapture')
    schemes = []
    frame_receiver = None
    read_latest_frame = None

    @staticmethod
    def create(url, *schemes):
        rtscap = RTSCapture(url)
        rtscap.frame_receiver = threading.Thread(target=rtscap.recv_frame, daemon=True)
        rtscap.schemes.extend(schemes)
        if isinstance(url, str) and url.startswith(tuple(rtscap.schemes)):
            rtscap._reading = True
        elif isinstance(url, int):
            pass
        return rtscap

    def isStarted(self):
        ok = self.isOpened()
        if ok and self._reading:
            ok = self.frame_receiver.is_alive()
        return ok

    def recv_frame(self):
        while self._reading and self.isOpened():
            ok, frame = self.read()
            if not ok:
                break
            self._cur_frame = frame
        self._reading = False

    def read2(self):
        frame = self._cur_frame
        self._cur_frame = None
        return frame is not None, frame

    def start_read(self, url: str):
        self.frame_receiver.start()
        self.read_latest_frame = self.read2 if self._reading else self.read

        RTSCapture.__logger.info(f'已初始化摄像头及二维码检测器-通道{url}')

        if not self.isStarted():
            RTSCapture.__logger.error("摄像头未能正确启动！")
            exit(0)

    def stop_read(self):
        self._reading = False
        if self.frame_receiver.is_alive():
            self.frame_receiver.join()
