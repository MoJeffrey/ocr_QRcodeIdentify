import logging
import os
from datetime import datetime

import cv2

from Tools.config import config


class ImageProcessing:
    __img = None
    __partitionList = []

    def __init__(self, img, fileName: str = None):
        self.__img = img

        ImageProcessing.save(self.__img, fileName)

    @staticmethod
    def save(img, fileName: str = None) -> None:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S.%f")

        fileName = f'{"" if fileName is None else fileName}_{current_time}.jpg'
        logging.info(fileName)
        frame_path = os.path.join(config.FRAME_FOLDER_PHAT, fileName)
        if not os.path.exists(frame_path):
            cv2.imwrite(frame_path, img)

    @staticmethod
    def show(partitionList) -> None:
        index = 0
        for partition in partitionList:
            cv2.imshow(str(index), partition)
            index += 1

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def partition(self) -> list:
        height, width = self.__img.shape[:2]
        self.__partitionList = []

        N_height = height // config.IMG_HIGH_QUANTITY
        N_width = width // config.IMG_WIDTH_QUANTITY
        for h in range(config.IMG_HIGH_QUANTITY):
            for w in range(config.IMG_WIDTH_QUANTITY):
                img = self.__img[N_height * h:N_height * (h + 1), N_width * w:N_width * (w + 1)]
                self.__partitionList.append(img)

        ImageProcessing.show(self.__partitionList)

        return self.__partitionList
