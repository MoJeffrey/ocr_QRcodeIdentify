import websocket
import threading
import logging

from Tools.config import config


def on_message(ws, message):
    print("Received: " + message)

def on_error(ws, error):
    print("Error: " + str(error))

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        ws.send("Hello, Server!")
        logging.info("send")
        ws.close()
        print("Thread terminating...")
    threading.Thread(target=run).start()

if __name__ == "__main__":
    config.Init_Logging()
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000/ws/recognizer/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
