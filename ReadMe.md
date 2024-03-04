### 打包
```shell
docker build -t ocr-qrcode-identify .
```

### 启动
```shell
xhost +Local:*
docker run -itd --name test-python -e "DISPLAY=$DISPLAY" --net=host --device=/dev/bus/usb:/dev/bus/usb --privileged -v /home/lougang/python-business/src:/app/src ocr-qrcode-identify
```

### 进入
```shell
docker exec -it test-python bash
```

### 环境变量更改Config 路径
```shell
CONFIG_PATH=/app/src/config.ini
```