import logging
import re

from Tools.config import config
from Tools.HttpUpload import HttpUpload


class QuestionsDTO:
    match_name = None
    data_all_num = None
    curr_num = None
    result: str = None
    logger = logging.getLogger('问题')

    def __init__(self, result):
        self.result = result
        self.logger.info = self.passInfo

    def passInfo(self, msg):
        pass

    def identify(self):
        try:
            # 开始截取问题编号及片段编号
            self.match_name = re.search(r'\[([^]]+)_', self.result).group(1)  # 问题编号
            self.data_all_num = int(re.search(r'\[(.*?)&(\d+)]', self.result).group(2))  # 片段总数
            self.curr_num = int(re.search(r'_(\d+)&', self.result).group(1))  # 当前片段号
            self.logger.info(f'已截取问题编号及片段编号')
            return None

        except Exception as e:
            print(f"未知信息: {e}")
            # http上传请求，将不分段的数据直接上传
            http_upload = HttpUpload(config.API_URL_IP, config.API_URL_PORT)
            response_data = http_upload.upload_data(config.API_URL, self.result)
            self.logger.info(f"不分段上传的请求结果: {response_data}")
            return self.result
