import http.client
import json


class HttpUpload:
    def __init__(self, api_url_ip, api_url_port):
        self.api_url_ip = api_url_ip
        self.api_url_port = api_url_port

# http请求代码
    def upload_data(self,api_url, concatenated_data, api_timeout=60):
        try:
            # 创建HTTP连接
            conn = http.client.HTTPConnection(f"{self.api_url_ip}", self.api_url_port, timeout=int(api_timeout))

            # 将数据转换为json格式并编码
            payload = json.dumps(concatenated_data, ensure_ascii=False).encode('utf-8')

            # 设置请求头
            headers = {
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'application/json'
            }

            # 发送POST请求
            conn.request("POST", f"{api_url}", payload, headers)

            # 获取响应
            res = conn.getresponse()
            data = res.read()
            return data

        except Exception as e:
            print(f"在上传数据过程中发生错误：{e}")
            return None
