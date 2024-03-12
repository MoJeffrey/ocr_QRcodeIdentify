# 建兴智能-无线传输-(QRCode 识别端)
## 前言
为了防止黑客或其他人为导致重要数据被篡改或窃取，公司致力研究一款产品能与机房物理隔绝，还能数据交互。
于是这么一款读取二维码数据无线传输的产品就出来了。
该Program是识别端，主要作用于识别二维码，并把数据传给后端。

![AppVeyor](https://img.shields.io/static/v1?label=MoJeffrey&message=OCR-QR-Code-Identify&color=<COLOR>)

## 软件要求
[![Python - < 9.8](https://img.shields.io/badge/python-v9.8-2ea44f?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

## 程序工作流程
1. 读取配置文件
2. 连接后台 Websocket
3. 根据配置的摄像头数量开启相应的线程
4. 开始无线循环读取摄像头的画面
5. 每个画面丢入线程池等待线程池处理
6. 若有新数据则依靠Websocket发送消息去后台

## 开发环境部署
懒

## Docker 启动
### 打包
```shell
# 打包
docker build -t ocr-qrcode-identify .

# 启动
xhost +Local:*
docker run -itd --name test-python -e "DISPLAY=$DISPLAY" --net=host --device=/dev/bus/usb:/dev/bus/usb --privileged -v /home/lougang/python-business/src:/app/src ocr-qrcode-identify

# 进入
docker exec -it test-python bash
```

## 文件結構
```
.
│   .gitignore
│   requirements.txt
│   sources.list
│   README.md
│   Dockerfile
│
├─── frame_img --摄像头截图
│
├───src --程序主代碼
│   │   main.py --程序入口
│   │   config.ini -- 配置文档
│   │   init.sh -- 一键启动脚本
│   ├─── caffe -- 微信二维码模型
│   ├─── Enum -- 所用枚举
│   ├─── Thread -- 线程代码
│   └─── Tools -- 工具代碼
│
└───UnitTest --測試代碼
```