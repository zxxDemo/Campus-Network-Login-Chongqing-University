import requests
import socket
import logging
import os

# 校园网登录URL
# 注意：请根据实际情况替换为正确的登录URL
LOGIN_URL = "http://YOUR_LOGIN_SERVER"

# 校园网登录的HTTP头部信息
# 注意：请根据实际情况设置正确的User-Agent和Referer
HEADERS = {
    "User-Agent": "YOUR_USER_AGENT",
    "Referer": "YOUR_REFERER"
}

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 从指定文件路径中读取登录凭证
def read_credentials():
    # 注意：请将下面的文件路径替换为实际存储登录凭证的文件路径
    filename = "YOUR_CREDENTIALS_FILE_PATH"
    credentials = {}
    with open(filename, 'r') as file:
        credentials['user_account'] = file.readline().strip()
        credentials['user_password'] = file.readline().strip()
    return credentials

# 登录函数
def login_to_campus_network():
    # 初始化PARAMS字典
    PARAMS = {
        'callback': 'dr1004',
        'login_method': '1',
        'wlan_user_ip': socket.gethostbyname(socket.gethostname()),  # 获取本机IP地址
        'jsVersion': '4.2',
        'terminal_type': '1',
        'lang': 'zh-cn',
        'v': '10002' 
    }

    credentials = read_credentials()
    PARAMS.update(credentials)

    try:
        response = requests.get(LOGIN_URL, params=PARAMS, headers=HEADERS)
        if response.status_code == 200:
            if "Portal协议认证成功！" in response.text:
                logging.info("自动登录成功")
            else:
                logging.warning("自动登录失败，响应内容：" + response.text)
        else:
            logging.error("请求失败，状态码：" + str(response.status_code))
    except requests.RequestException as e:
        logging.error("请求过程中发生错误：" + str(e))

# 程序入口点
if __name__ == "__main__":
    login_to_campus_network()
