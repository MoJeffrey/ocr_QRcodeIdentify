### 打包
```shell
docker build -t ocr-qrcode-identify .
```

### 启动
```shell
docker run -itd --name test-python --device=/dev/video0:/dev/video0 --privileged -v E:\python\ocr_QRcodeIdentify\src:/app/src ocr-qrcode-identify
```

### 进入
```shell
docker exec -it test-python bash
```