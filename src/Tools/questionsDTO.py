import logging
import re


class QuestionsDTO:
    match_name = None
    data_all_num = None
    curr_num = None
    result: str = None
    logger = logging.getLogger('问题')

    def __init__(self, result):
        self.result = result
        self.logger.info = self.passInfo
        self.identify()

    def passInfo(self, msg):
        pass

    def identify(self):
        try:
            self.match_name = re.search(r'[QACE]\d+', self.result).group()
            self.data_all_num = int(re.search(r'\[[AQCE]\d+_\d+_(\d+)]', self.result).group(1))
            self.curr_num = int(re.search(r'\[[AQCE]\d+_(\d+)_\d+]', self.result).group(1))
            self.logger.info(f'已截取问题编号及片段编号')
        except Exception:
            self.logger.error(self.result)

    @staticmethod
    def splicing(current_data_list: list) -> str:
        sorted_data = sorted(current_data_list, key=lambda x: int(re.search(r'\[[AQCE]\d+_(\d+)_\d+]', x).group(1)))
        return ''.join([d[d.index(']') + 1:] for d in sorted_data])

if __name__ == '__main__':

    text = ['[Q000000032_1_1]{"url": "/question/user/getinfo", "headers": [], "method": "POST", "data": {"address": true}, "action": "transponder"}']
    a = QuestionsDTO.splicing(text)
    print(a)
