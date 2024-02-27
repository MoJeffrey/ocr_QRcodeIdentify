# 使用官方 Python 3.8 镜像作为基础镜像
FROM python:3.8

# 设置工作目录
WORKDIR /app/lib
COPY ./requirements.txt ./

# 安装所需的依赖
RUN pip install -r requirements.txt
RUN pip uninstall -y opencv-python
RUN pip install opencv-python-headless

ENV CONFIG_PATH = /app/src/config.ini

# 设置环境变量
ENV PATH="/app/lib:${PATH}"

WORKDIR /app/src
# 设置容器启动时执行的命令
CMD ["tail", "-f", "/dev/null"]