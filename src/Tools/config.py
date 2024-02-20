import configparser
import logging
import os


class config(object):
    __CONFIG_PATH = None

    """
    Sys
    """
    Sys_IsOK = False
    Sys_MAX_WORKER: int = None
    Sys_LOG_INFO: bool = None

    """
    RTSP
    """
    RTSP_USERNAME: str = None
    RTSP_PASSWORD: str = None
    RTSP_IP: str = None
    RTSP_PORT: int = None
    RTSP_URLS: list = None

    """
    API
    """
    API_URL_IP: str = None
    API_URL: str = None
    API_URL_PORT: int = None
    API_TIMEOUT: str = None
    API_WEBSOCKET_URL: str = None

    """
    OTHER
    """
    OTHER_PAUSE_TIME: float = None
    OTHER_USB_CAM_NUM: str = None
    OTHER_MAX_WORKERS: str = None
    OTHER_STORE_FRAME_ENABLED: str = None

    """
    REDIS
    """
    REDIS_HOST: str = None
    REDIS_PORT: int = None
    REDIS_DB: int = None
    REDIS_PASSWORD: str = None

    """
    PHAT
    """
    FRAME_FOLDER_PHAT: str = None
    SCRIPT_DIR: str = None

    """
    IMG
    """
    IMG_HIGH_QUANTITY: int = None
    IMG_WIDTH_QUANTITY: int = None
    IMG_SHOW: bool = None
    IMG_SAVE: bool = None

    def __init__(self):
        self.__CONFIG_PATH = None

    def Init(self, ConfigFile: str = None) -> None:
        """
        初始化配置文件
        :param ConfigFile:
        :return:
        """
        self.__ReadConfigFile(ConfigFile)
        self.__Analyze()
        self.__Init_PHAT()
        self.Init_Logging()
        self.PrintConfig()

    def __ReadConfigFile(self, ConfigFile: str = None) -> None:
        """
        讀取配置文件

        如果沒有傳入文件路徑
        則在環境變量中獲取
        :param ConfigFile:
        :return:
        """
        if ConfigFile is None:
            if "CONFIG_PATH" not in os.environ:
                raise NoSetCONFIGError()
            else:
                self.__CONFIG_PATH = os.environ['CONFIG_PATH']
        else:
            self.__CONFIG_PATH = ConfigFile

        print(os.getcwd())
        if os.path.exists(self.__CONFIG_PATH):
            self.__File = configparser.ConfigParser()
            self.__File.read(self.__CONFIG_PATH, encoding="utf-8")
            return

        raise FileNotFoundError

    @staticmethod
    def Init_Logging() -> None:
        """

        :return:
        """
        formatStr = '%(asctime)s.%(msecs)03d-%(name)s-%(levelname)s-[日志信息]: %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatStr, datefmt='%Y-%m-%d %H:%M:%S')

    @staticmethod
    def PrintConfig() -> None:
        logger = logging.getLogger('config')
        logger.info(f"摄像头参数: {config.RTSP_USERNAME},{config.RTSP_PASSWORD},{config.RTSP_IP},{config.RTSP_PORT}")
        logger.info(f"接口参数: {config.API_URL_IP},{config.API_URL_PORT},{config.API_URL},{config.API_TIMEOUT}")
        logger.info(f"REDIS参数: {config.REDIS_HOST},{config.REDIS_PORT},{config.REDIS_DB}")
        logger.info(f"其他参数：OTHER_PAUSE_TIME: {config.OTHER_PAUSE_TIME}")
        logger.info(f"其他参数：OTHER_USB_CAM_NUM: {config.OTHER_USB_CAM_NUM}")
        logger.info(f"其他参数：OTHER_MAX_WORKERS: {config.OTHER_MAX_WORKERS}")
        logger.info(f"其他参数：OTHER_STORE_FRAME_ENABLED: {config.OTHER_STORE_FRAME_ENABLED}")
        logger.info("====================================================")

    def __Analyze(self) -> None:
        """
        解析配置文檔
        :return:
        """
        self.__Analyze_RTSP()
        self.__Analyze_API()
        self.__Analyze_OTHER()
        self.__Analyze_REDIS()
        self.__Analyze_IMG()

    def __Analyze_RTSP(self) -> None:
        RTSPConfig = self.__File['RTSP']

        config.RTSP_USERNAME = RTSPConfig['USERNAME']
        config.RTSP_PASSWORD = RTSPConfig['PASSWORD']
        config.RTSP_IP = RTSPConfig['IP']
        config.RTSP_PORT = RTSPConfig.getint('PORT')
        config.RTSP_URLS = RTSPConfig.get('RTSP_URLS')

        config.RTSP_USERNAME = os.environ.get('RTSP_USERNAME', config.RTSP_USERNAME)
        config.RTSP_PASSWORD = os.environ.get('RTSP_PASSWORD', config.RTSP_PASSWORD)
        config.RTSP_IP = os.environ.get('RTSP_IP', config.RTSP_IP)
        config.RTSP_PORT = os.environ.get('RTSP_PORT', config.RTSP_PORT)
        config.RTSP_URLS = str(os.environ.get('RTSP_URLS', config.RTSP_URLS))

        config.RTSP_URLS = config.RTSP_URLS.split(',')

    def __Analyze_API(self) -> None:
        APIConfig = self.__File['API']
        config.API_URL_IP = APIConfig['URL_IP']
        config.API_URL = APIConfig['URL']
        config.API_URL_PORT = APIConfig.getint('URL_PORT')
        config.API_TIMEOUT = APIConfig.getint('TIMEOUT')
        config.API_WEBSOCKET_URL = APIConfig.get('WEBSOCKET_URL')

        config.API_URL_IP = os.environ.get('API_URL_IP', config.API_URL_IP)
        config.API_URL = os.environ.get('API_URL', config.API_URL)
        config.API_URL_PORT = os.environ.get('API_URL_PORT', config.API_URL_PORT)
        config.API_TIMEOUT = os.environ.get('API_TIMEOUT', config.API_TIMEOUT)
        config.API_WEBSOCKET_URL = os.environ.get('API_WEBSOCKET_URL', config.API_WEBSOCKET_URL)

    def __Analyze_OTHER(self) -> None:
        """
        :return:
        """
        OTHERConfig = self.__File['OTHER']
        config.OTHER_PAUSE_TIME = OTHERConfig.getfloat('PAUSE_TIME')
        config.OTHER_USB_CAM_NUM = OTHERConfig['USB_CAM_NUM']
        config.OTHER_MAX_WORKERS = OTHERConfig['MAX_WORKERS']
        config.OTHER_STORE_FRAME_ENABLED = OTHERConfig['STORE_FRAME_ENABLED']

        config.OTHER_PAUSE_TIME = os.environ.get('PAUSE_TIME', config.OTHER_PAUSE_TIME)
        config.OTHER_USB_CAM_NUM = int(os.environ.get('USB_CAM_NUM', config.OTHER_USB_CAM_NUM))
        config.OTHER_MAX_WORKERS = os.environ.get('MAX_WORKERS', config.OTHER_MAX_WORKERS)
        config.OTHER_STORE_FRAME_ENABLED = os.environ.get('STORE_FRAME_ENABLED', config.OTHER_STORE_FRAME_ENABLED)

    def __Analyze_REDIS(self) -> None:
        REDISConfig = self.__File['REDIS']
        config.REDIS_HOST = REDISConfig['HOST']
        config.REDIS_PORT = REDISConfig['PORT']
        config.REDIS_DB = REDISConfig['DB']
        config.REDIS_PASSWORD = REDISConfig['PASSWORD']

        config.REDIS_HOST = os.environ.get('REDIS_HOST', config.REDIS_HOST)
        config.REDIS_PORT = os.environ.get('REDIS_PORT', config.REDIS_PORT)
        config.REDIS_DB = os.environ.get('REDIS_DB', config.REDIS_DB)
        config.REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', config.REDIS_PASSWORD)

    def __Analyze_IMG(self) -> None:
        IMGConfig = self.__File['IMG']
        config.IMG_HIGH_QUANTITY = IMGConfig.getint('HIGH_QUANTITY')
        config.IMG_WIDTH_QUANTITY = IMGConfig.getint('WIDTH_QUANTITY')
        config.IMG_SHOW = IMGConfig.getboolean('SHOW')
        config.IMG_SAVE = IMGConfig.getboolean('SAVE')

        config.IMG_HIGH_Quantity = int(os.environ.get('IMG_HIGH_QUANTITY', config.IMG_HIGH_QUANTITY))
        config.IMG_WIDTH_Quantity = int(os.environ.get('IMG_WIDTH_QUANTITY', config.IMG_WIDTH_QUANTITY))
        config.IMG_SHOW = bool(os.environ.get('IMG_SHOW', config.IMG_SHOW))
        config.IMG_SAVE = bool(os.environ.get('IMG_SAVE', config.IMG_SAVE))

    def __Analyze_Sys(self) -> None:
        SysConfig = self.__File['Sys']
        config.Sys_LOG_INFO = SysConfig.getint('LOG_INFO')
        config.Sys_MAX_WORKER = SysConfig.getint('MAX_WORKER')

        config.Sys_LOG_INFO = bool(os.environ.get('Sys_LOG_INFO', config.Sys_LOG_INFO))
        config.Sys_MAX_WORKER = int(os.environ.get('Sys_MAX_WORKER', config.Sys_MAX_WORKER))

    @staticmethod
    def __Init_PHAT() -> None:
        config.FRAME_FOLDER_PHAT = os.path.join(os.getcwd(), 'frame_img')
        if not os.path.exists(config.FRAME_FOLDER_PHAT):
            os.makedirs(config.FRAME_FOLDER_PHAT)


class NoSetCONFIGError(Exception):

    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return "no environment variables configured : CONFIG_PATH"
