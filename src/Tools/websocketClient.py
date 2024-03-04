import json
import logging
import threading
import time

import websocket

from Thread.Ocr_ThreadPoolExecutor import OCR_ThreadPoolExecutor
from Tools.config import config


class websocketClient:

    __client = None
    __IsConnect = False

    @staticmethod
    def Init():
        param = {
            "url": config.API_WEBSOCKET_URL,
            "on_message": websocketClient.on_message,
            "on_error": websocketClient.on_error,
            "on_close": websocketClient.on_close,
            "on_open": websocketClient.on_open,
        }
        websocketClient.__client = websocket.WebSocketApp(**param)

        thread = threading.Thread(target=websocketClient.__client.run_forever, args=())
        thread.start()

        while not websocketClient.__IsConnect:
            time.sleep(1)

    @staticmethod
    def send(msg):
        try:
            websocketClient.__client.send(msg)
        except Exception as E:
            pass

    @staticmethod
    def on_message(ws, message):
        data = json.loads(message)
        code = data["code"]
        if data["action"] == "delete":
            Results = OCR_ThreadPoolExecutor.DeleteResult(code)
            OCR_ThreadPoolExecutor.removeSet(Results)

    @staticmethod
    def on_error(ws, error):
        pass

    @staticmethod
    def on_close(ws, close_status_code, msg):
        OCR_ThreadPoolExecutor.ReSetData()
        websocketClient.Init()

    @staticmethod
    def on_open(ws):
        websocketClient.__IsConnect = True

    @staticmethod
    def Stop():
        websocketClient.__client.keep_running = False
