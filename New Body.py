#用于自动登录、自动检查并连接，注意修改文件扩展为pyw
import requests
import logging
import time
import socket
# 导入requests库用于发送HTTP请求，logging库用于日志记录，time库用于时间操作，socket库用于网络连接检查。

# 定义登录服务器的URL，请根据实际填写
LOGIN_URL = "http://YOUR_LOGIN_SERVER"
# 定义请求头，请根据实际填写
HEADERS = {
    "User-Agent": "YOUR_USER_AGENT",
    "Referer": "YOUR_REFERER"
}


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义读取用户名和密码的函数
def read_credentials(filename="YOUR_CREDENTIALS_FILE_PATH"):
    credentials = {}
    with open(filename, 'r') as file:
        credentials['user_account'] = file.readline().strip()
        credentials['user_password'] = file.readline().strip()
    return credentials

# 定义检查互联网连接的函数
def is_internet_connected(host="8.8.8.8", port=53, timeout=1, max_retries=3):
    # 尝试连接到指定的服务器和端口，如果连接成功则表示互联网连接正常
    for _ in range(max_retries):
        try:
            socket.create_connection((host, port), timeout=timeout)
            return True
        except socket.error:
            time.sleep(1)
    # 如果尝试连接失败，则返回False
    return False

# 定义登录函数
def login(username: str, password: str):
    params = {
        'callback': 'dr1004',
        'login_method': '1',
        'wlan_user_ip': socket.gethostbyname(socket.gethostname()),
        'jsVersion': '4.2',
        'terminal_type': '1',
        'lang': 'zh-cn',
        'v': '10002'
    }
    params.update({'user_account': username, 'user_password': password})

    try:
        # 发送登录请求
        response = requests.get(LOGIN_URL, params=params, headers=HEADERS)
        # 如果响应状态码为200并且响应文本包含特定的成功信息，则认为登录成功
        if response.status_code == 200 and "Portal协议认证成功！" in response.text:
            return True
        else:
            # 如果登录失败，则记录警告信息
            logging.warning("认证失败，响应内容：" + response.text)
            return False
    except requests.RequestException as e:
        # 如果请求过程中发生错误，则记录错误信息
        logging.error("请求过程中发生错误：" + str(e))
        return False

# 定义主函数
def main():
    # 读取用户名和密码
    credentials = read_credentials()
    # 获取日志记录器
    logger = logging.getLogger()

    try:
        # 无限循环，持续检查网络连接状态并尝试自动登录
        while True:
            if not is_internet_connected():
                # 如果网络未连接，则尝试自动登录
                logger.info("网络未认证，开始尝试自动登录...")
                if not login(credentials['user_account'], credentials['user_password']):
                    # 如果自动登录失败，则记录错误信息
                    logger.error("自动登录失败，请检查用户名和密码是否正确")
            # 每5分钟检查一次网络连接状态
            time.sleep(300)
    except KeyboardInterrupt:
        # 如果用户中断程序，则记录信息
        logger.info("程序被用户中断")

# 程序的入口点
if __name__ == "__main__":
    main()
