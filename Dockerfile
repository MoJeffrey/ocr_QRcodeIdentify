# 使用官方 Python 3.8 镜像作为基础镜像
FROM python:3.8

# 设置工作目录
WORKDIR /app/lib
COPY ./requirements.txt ./
COPY ./requirements.txt /etc/apt/sources.list

# 安装所需的依赖
RUN sed -i 's|http://deb.debian.org/debian|http://mirrors.aliyun.com/debian|g' /etc/apt/sources.list
RUN sed -i 's|http://security.debian.org/debian-security|http://mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip install -r requirements.txt
ENV CONFIG_PATH=/app/src/config.ini

# 设置环境变量
ENV PATH="/app/lib:${PATH}"

WORKDIR /app/src
# 设置容器启动时执行的命令
CMD ["tail", "-f", "/dev/null"]